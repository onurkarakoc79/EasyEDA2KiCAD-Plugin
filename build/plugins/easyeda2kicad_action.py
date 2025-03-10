#!/usr/bin/env python
import pcbnew
from pcbnew import ActionPlugin
import wx
import subprocess

class EasyEDA2KiCADPlugin(ActionPlugin):
    def defaults(self):
        self.name = "EasyEDA2KiCAD Plugin"
        self.category = "Utilities"
        self.description = "Imports parts from LCSC using easyeda2kicad"
    
    def Run(self):
        # Create GUI for Part Number Input
        dialog = wx.TextEntryDialog(None, "Enter LCSC Part Number:", "EasyEDA2KiCAD Importer", "")
        if dialog.ShowModal() == wx.ID_OK:
            part_number = dialog.GetValue().strip()
            if part_number:
                self.import_part(part_number)
            else:
                wx.MessageBox("Please enter a valid LCSC part number.", "Error", wx.ICON_ERROR)
        dialog.Destroy()

    def import_part(self, part_number):
        try:
            command = f"easyeda2kicad --overwrite --full {part_number}"
            result = subprocess.run(command, shell=True, capture_output=True, text=True)

            if result.returncode != 0:
                wx.MessageBox(f"Failed to import part:\n{result.stderr}", "Import Error", wx.ICON_ERROR)
            else:
                wx.MessageBox(f"Part {part_number} imported successfully!", "Success", wx.ICON_INFORMATION)

        except Exception as e:
            wx.MessageBox(f"Unexpected error: {str(e)}", "Error", wx.ICON_ERROR)
