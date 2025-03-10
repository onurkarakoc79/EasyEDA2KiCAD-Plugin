from .easyeda2kicad_action import PluginInjector

# Start the injector timer to check for schematic windows every 2 seconds.
injector = PluginInjector()
injector.Start(2000)  # 2000 milliseconds = 2 seconds

print("✅ EasyEDA2KiCAD Plugin Auto Injector Started")
