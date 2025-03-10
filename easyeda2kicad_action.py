import pcbnew
from pcbnew import ActionPlugin
import wx
import subprocess
import os

class EasyEDA2KiCADPlugin(ActionPlugin):
    def defaults(self):
        self.name = "EasyEDA2KiCAD Plugin"
        self.category = "Import Tools"
        self.description = "Import EasyEDA parts using LCSC Part Number"

    def Run(self):
        print("🔍 EasyEDA2KiCAD Plugin Initialized in Schematic Editor")

        # Identify the correct Schematic Editor window
        schematic_found = False
        for window in wx.GetTopLevelWindows():
            if "Schematic Editor" in window.GetTitle() or "Eeschema" in window.GetTitle():
                panel = window
                print("✅ Found Schematic Editor Panel")
                schematic_found = True
                break

        if not schematic_found:
            wx.MessageBox("Error: Failed to find Schematic Editor panel. Are you in the correct editor?", "Error", wx.ICON_ERROR)
            print("❌ Could not find Schematic Editor Panel")
            return

        print("📋 Creating UI Panel for EasyEDA2KiCAD Plugin")
        new_panel = EasyEDA2KiCADPanel(panel)
        panel.GetSizer().Add(new_panel, 0, wx.EXPAND)
        panel.Layout()
        panel.Refresh()

        wx.MessageBox("EasyEDA2KiCAD Plugin UI added to the Schematic Editor.", "Success", wx.ICON_INFORMATION)

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
