from .easyeda2kicad_action import PluginInjector

## @brief Initializes and starts the EasyEDA2KiCAD Plugin Injector.
#  
#  The injector checks for KiCad schematic windows every **2 seconds** (2000ms).
#  This ensures the plugin panel is injected into KiCad's UI automatically
#  when a schematic window is detected.
#
#  @note This approach avoids manual plugin initialization.
injector = PluginInjector()

## @brief Starts the injector timer.
#  @param interval Time interval in milliseconds (2000ms = 2 seconds).
injector.Start(2000)  # 2000 milliseconds = 2 seconds

print("✅ EasyEDA2KiCAD Plugin Auto Injector Started")
