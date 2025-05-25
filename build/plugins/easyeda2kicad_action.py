import wx
import os
import subprocess
import shutil  # For cross-platform command lookup
import json  # For modifying KiCad config

## @brief Path where KiCad plugin data will be stored.
KICAD_PATH = os.path.join(os.path.expanduser("~"), "Documents", "KiCAD", "EASYEDA2KICAD")

## @brief Retrieves the path of the `easyeda2kicad` command using pipx environment or fallback paths.
#  @return The full path to the `easyeda2kicad` executable.
#  @throws FileNotFoundError if `easyeda2kicad` command is not found.
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

    # Fallback path for Linux systems
    fallback_path = os.path.expanduser("~/.local/share/pipx/venvs/easyeda2kicad/bin/easyeda2kicad")
    if os.path.exists(fallback_path):
        return fallback_path

    # Cross-platform lookup for the command in system PATH
    easyeda2kicad_path = shutil.which("easyeda2kicad")
    if not easyeda2kicad_path:
        raise FileNotFoundError(
            "❗ Error: 'easyeda2kicad' command not found.\n"
            "Ensure `pipx` is installed and the `easyeda2kicad` command is available in PATH."
        )

    return easyeda2kicad_path

## @brief Injects the EasyEDA2KiCAD plugin panel into the KiCad UI.
def inject_plugin_panel():
    for window in wx.GetTopLevelWindows():
        try:
            title = window.GetTitle()
        except Exception:
            continue
        
        # Skip PCB windows; apply only for schematic windows
        if "PCB" in title:
            continue

        if ("Schematic" in title) or ("Eeschema" in title) or ("schematic" in title):
            # Prevent duplicate panel injection
            if window.FindWindowByName("EasyEDA2KiCADPanel"):
                continue

            plugin_panel = EasyEDA2KiCADPanel(window)
            plugin_panel.SetName("EasyEDA2KiCADPanel")  # Assign unique name for tracking

            # Attach the panel to the KiCad UI
            if window.GetSizer() is not None:
                window.GetSizer().Add(plugin_panel, 0, wx.EXPAND)
                window.Layout()
                window.Refresh()
                print("Injected plugin panel into window:", title)

## @brief Custom panel for EasyEDA2KiCAD plugin within KiCad.
class EasyEDA2KiCADPanel(wx.Panel):
    ## @brief Initializes the panel UI elements.
    #  @param parent The parent window in which the panel will be added.
    def __init__(self, parent):
        super().__init__(parent)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # Textbox for entering LCSC part numbers
        self.text_box = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.text_box.SetHint("Enter LCSC Part Number...")

        # Import button to start the EasyEDA2KiCAD process
        self.run_button = wx.Button(self, label="Import")
        self.run_button.Bind(wx.EVT_BUTTON, self.on_import)

        # Add UI elements to the panel layout
        sizer.Add(self.text_box, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.run_button, 0, wx.ALL, 5)
        self.SetSizer(sizer)

    ## @brief Handles the import button click event.
    #  @param event The button click event.
    def on_import(self, event):
        part_number = self.text_box.GetValue().strip()
        if not part_number:
            wx.MessageBox("Please enter a valid LCSC part number.", "Error", wx.ICON_ERROR)
            return

        # Verify `easyeda2kicad` command availability
        try:
            easyeda2kicad_path = get_easyeda2kicad_path()
        except FileNotFoundError:
            wx.MessageBox(
                "❗ Error: 'easyeda2kicad' command not found.\n"
                "Ensure `pipx` is installed and the `easyeda2kicad` command is available in PATH.",
                "Error",
                wx.ICON_ERROR
            )
            return

        # Construct command for importing parts
        command_symbol = [
            easyeda2kicad_path, "--overwrite", "--full",
            f"--lcsc_id={part_number}", "--output", os.path.join(KICAD_PATH, "easyeda2kicad")
        ]

        # Execute the import command
        try:
            result_symbol = subprocess.run(command_symbol, capture_output=True, text=True)
            if result_symbol.returncode != 0:
                wx.MessageBox(f"Failed to import symbol:\n{result_symbol.stderr}", "Import Error", wx.ICON_ERROR)
                return

            wx.MessageBox(f"Part {part_number} imported successfully to EasyEDA2KiCAD!", "Success", wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(f"Unexpected error: {str(e)}", "Error", wx.ICON_ERROR)

## @brief Timer-based plugin injector that periodically checks for active KiCad windows.
class PluginInjector(wx.Timer):
    ## @brief Initializes the plugin injector timer.
    def __init__(self):
        super().__init__()

    ## @brief Invokes the panel injection logic upon timer notification.
    def Notify(self):
        inject_plugin_panel()
