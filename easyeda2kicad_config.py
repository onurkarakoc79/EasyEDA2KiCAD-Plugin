import os
import json

## @brief Retrieves the path to the KiCad configuration file.
#  @return The path to the KiCad configuration file, or None if not found.
def get_kicad_config_path():
    # Check for platform-specific KiCad config paths
    if os.name == 'nt':  # Windows
        base_path = os.path.join(os.environ.get('APPDATA', ''), "kicad")
    else:  # Linux and macOS
        base_path = os.path.join(os.path.expanduser("~"), ".config", "kicad")

    # Search for versioned KiCad folders (e.g., v7, v8)
    if base_path and os.path.exists(base_path):
        versions = [d for d in os.listdir(base_path) if d[0].isdigit() and os.path.isdir(os.path.join(base_path, d))]
        if versions:
            latest_version = max(versions, key=lambda v: float(v.split('.')[0]))
            latest_config_path = os.path.join(base_path, latest_version, "kicad_common.json")
            if os.path.exists(latest_config_path):
                return latest_config_path

        # Fallback to checking the standard KiCad path
        fallback_path = os.path.join(base_path, "kicad_common.json")
        if os.path.exists(fallback_path):
            return fallback_path

    # macOS-specific path for KiCad configuration
    possible_paths = [
        os.path.join(os.path.expanduser("~"), "Library", "Preferences", "kicad", "kicad_common.json")
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path

    return None

## @brief Configures KiCad paths for EasyEDA2KiCad plugin usage.
def configure_kicad_paths():
    ## @brief Defines the custom KiCad path for EasyEDA2KiCad libraries.
    KICAD_PATH = os.path.join(os.path.expanduser("~"), "Documents", "KiCAD", "EASYEDA2KICAD")

    # Create directories for symbols, footprints, and the base path
    os.makedirs(KICAD_PATH, exist_ok=True)
    os.makedirs(os.path.join(KICAD_PATH, "easyeda2kicad.pretty"), exist_ok=True)
    os.makedirs(os.path.join(KICAD_PATH, "easyeda2kicad.3dshapes"), exist_ok=True)

    # Get KiCad configuration path
    config_path = get_kicad_config_path()

    if config_path:
        # Load KiCad configuration
        with open(config_path, 'r') as file:
            try:
                config_data = json.load(file)
            except json.JSONDecodeError:
                print("❗ KiCad configuration file exists but is corrupted or invalid.")
                return

        # Add environment variable entries for custom paths
        if 'environment' not in config_data:
            config_data['environment'] = {}
        if 'vars' not in config_data['environment']:
            config_data['environment']['vars'] = {}

        env_vars = config_data['environment']['vars']
        if env_vars is None:
            env_vars = {}

        # Set the EASYEDA2KICAD path in KiCad's environment variables
        env_vars['EASYEDA2KICAD'] = KICAD_PATH
        config_data['environment']['vars'] = env_vars

        # Save the modified configuration file
        with open(config_path, 'w') as file:
            json.dump(config_data, file, indent=4)

        print("✅ EASYEDA2KICAD path configured successfully.")

        ## @brief Adds the EasyEDA2KiCad symbol library entry to the `sym-lib-table`.
        sym_lib_table_path = os.path.join(os.path.dirname(config_path), 'sym-lib-table')
        sym_entry = f'  (lib (name easyeda2kicad)(type KiCad)(uri ${{EASYEDA2KICAD}}/easyeda2kicad.kicad_sym)(options "")(descr "EasyEDA2KiCAD Symbol Library"))'

        if os.path.exists(sym_lib_table_path):
            with open(sym_lib_table_path, 'r+') as file:
                content = file.read().strip()
                if sym_entry not in content:
                    content = content.rstrip(')') + sym_entry + "\n)"
                    file.seek(0)
                    file.write(content)
                    print("✅ EasyEDA2KiCAD Symbol Library added to sym-lib-table.")
                else:
                    print("✅ EasyEDA2KiCAD Symbol Library already exists in sym-lib-table.")

        ## @brief Adds the EasyEDA2KiCad footprint library entry to the `fp-lib-table`.
        fp_lib_table_path = os.path.join(os.path.dirname(config_path), 'fp-lib-table')
        fp_entry = f'  (lib (name easyeda2kicad)(type KiCad)(uri ${{EASYEDA2KICAD}}/easyeda2kicad.pretty)(options "")(descr "EasyEDA2KiCAD Footprint Library"))'

        if os.path.exists(fp_lib_table_path):
            with open(fp_lib_table_path, 'r+') as file:
                content = file.read().strip()
                if fp_entry not in content:
                    content = content.rstrip(')') + fp_entry + "\n)"
                    file.seek(0)
                    file.write(content)
                    print("✅ EasyEDA2KiCAD Footprint Library added to fp-lib-table.")
                else:
                    print("✅ EasyEDA2KiCAD Footprint Library already exists in fp-lib-table.")

    else:
        print("❗ KiCad configuration file not found. Please open KiCad, go to Preferences → Configure Paths, click OK, then rerun this script.")
        print("🔍 If you have already launched KiCad, ensure your config is located in:")
        print("   → Linux: ~/.config/kicad/")
        print("   → macOS: ~/Library/Preferences/kicad/")
        print("   → Windows: %APPDATA%\\kicad\\")

## @brief Main function to initiate the configuration process.
if __name__ == "__main__":
    configure_kicad_paths()
