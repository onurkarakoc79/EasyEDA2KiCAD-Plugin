import wx
import os
import subprocess
import shutil  # For cross-platform command lookup
import json  # For modifying KiCad config

KICAD_PATH = os.path.join(os.path.expanduser("~"), "Documents", "KiCAD", "EASYEDA2KICAD")

def get_easyeda2kicad_path():
    try:
        result = subprocess.run(
            ["pipx", "environment"],
            capture_output=True,
            text=True
        )
        for line in result.stdout.splitlines():
            if "easyeda2kicad" in line:
                env_path = line.split()[-1]
                easyeda2kicad_path = os.path.join(env_path, "bin", "easyeda2kicad")
                if os.path.exists(easyeda2kicad_path):
                    return easyeda2kicad_path
    except FileNotFoundError:
        pass

    fallback_path = os.path.expanduser("~/.local/share/pipx/venvs/easyeda2kicad/bin/easyeda2kicad")
    if os.path.exists(fallback_path):
        return fallback_path

    easyeda2kicad_path = shutil.which("easyeda2kicad")
    if not easyeda2kicad_path:
        raise FileNotFoundError(
            "❗ Error: 'easyeda2kicad' command not found.\n"
            "Ensure `pipx` is installed and the `easyeda2kicad` command is available in PATH."
        )

    return easyeda2kicad_path

def inject_plugin_panel():
    for window in wx.GetTopLevelWindows():
        try:
            title = window.GetTitle()
        except Exception:
            continue
        if "PCB" in title:
            continue

        if ("Schematic" in title) or ("Eeschema" in title) or ("schematic" in title):
            # Check if the panel already exists
            if window.FindWindowByName("EasyEDA2KiCADPanel"):
                continue

            plugin_panel = EasyEDA2KiCADPanel(window)
            plugin_panel.SetName("EasyEDA2KiCADPanel")  # Assign a unique name to track it

            if window.GetSizer() is not None:
                window.GetSizer().Add(plugin_panel, 0, wx.EXPAND)
                window.Layout()
                window.Refresh()
                print("Injected plugin panel into window:", title)

class EasyEDA2KiCADPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.text_box = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.text_box.SetHint("Enter LCSC Part Number...")
        self.run_button = wx.Button(self, label="Import")
        self.run_button.Bind(wx.EVT_BUTTON, self.on_import)
        sizer.Add(self.text_box, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.run_button, 0, wx.ALL, 5)
        self.SetSizer(sizer)

    def on_import(self, event):
        part_number = self.text_box.GetValue().strip()
        if not part_number:
            wx.MessageBox("Please enter a valid LCSC part number.", "Error", wx.ICON_ERROR)
            return

        try:
            easyeda2kicad_path = get_easyeda2kicad_path()
        except FileNotFoundError:
            wx.MessageBox("❗ Error: 'easyeda2kicad' command not found.\nEnsure `pipx` is installed and the `easyeda2kicad` command is available in PATH.", "Error", wx.ICON_ERROR)
            return

        command_symbol = [
            easyeda2kicad_path, "--overwrite", "--full",
            f"--lcsc_id={part_number}", "--output", os.path.join(KICAD_PATH, "easyeda2kicad")
        ]

        try:
            result_symbol = subprocess.run(command_symbol, capture_output=True, text=True)
            if result_symbol.returncode != 0:
                wx.MessageBox(f"Failed to import symbol:\n{result_symbol.stderr}", "Import Error", wx.ICON_ERROR)
                return

            wx.MessageBox(f"Part {part_number} imported successfully to EasyEDA2KiCAD!", "Success", wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(f"Unexpected error: {str(e)}", "Error", wx.ICON_ERROR)

class PluginInjector(wx.Timer):
    def __init__(self):
        super().__init__()
    def Notify(self):
        inject_plugin_panel()
