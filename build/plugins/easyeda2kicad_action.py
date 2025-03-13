import wx
import os
import subprocess

# Global dict to track injected panels
injected_panels = {}

def inject_plugin_panel():
    # Debug: print out the titles of all top-level windows
    print("Debug: Listing top-level window titles:")
    for window in wx.GetTopLevelWindows():
        try:
            title = window.GetTitle()
            print("Window title:", title)
        except Exception as e:
            print("Error getting window title:", e)
    
    # Iterate over windows looking for a schematic editor window.
    for window in wx.GetTopLevelWindows():
        try:
            title = window.GetTitle()
        except Exception as e:
            continue
        # Skip any window that is the PCB editor.
        if "PCB" in title:
            continue
        # Check if this window appears to be the schematic editor.
        if ("Schematic" in title) or ("Eeschema" in title) or ("schematic" in title):
            if window.GetId() not in injected_panels:
                plugin_panel = EasyEDA2KiCADPanel(window)
                if window.GetSizer() is not None:
                    window.GetSizer().Add(plugin_panel, 0, wx.EXPAND)
                    window.Layout()
                    window.Refresh()
                    injected_panels[window.GetId()] = plugin_panel
                    print("Injected plugin panel into window:", title)
    # Clean up injected_panels for windows that no longer exist.
    current_ids = {w.GetId() for w in wx.GetTopLevelWindows()}
    for win_id in list(injected_panels.keys()):
        if win_id not in current_ids:
            del injected_panels[win_id]

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
        easyeda2kicad_path = "/home/onur-karakoc/.local/bin/easyeda2kicad"
        if not os.path.exists(easyeda2kicad_path):
            wx.MessageBox("Error: 'easyeda2kicad' command not found.\nCheck if pipx is installed and added to PATH.", "Error", wx.ICON_ERROR)
            return
        command = [easyeda2kicad_path, "--overwrite", "--full", f"--lcsc_id={part_number}"]
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode != 0:
                wx.MessageBox(f"Failed to import part:\n{result.stderr}", "Import Error", wx.ICON_ERROR)
            else:
                wx.MessageBox(f"Part {part_number} imported successfully!", "Success", wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(f"Unexpected error: {str(e)}", "Error", wx.ICON_ERROR)

class PluginInjector(wx.Timer):
    def __init__(self):
        super().__init__()
    def Notify(self):
        inject_plugin_panel()
