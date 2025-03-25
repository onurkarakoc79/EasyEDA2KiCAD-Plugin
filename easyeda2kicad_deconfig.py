import os
import json

def get_kicad_config_path():
    if os.name == 'nt':
        base_path = os.path.join(os.environ.get('APPDATA', ''), "kicad")
    else:
        base_path = os.path.join(os.path.expanduser("~"), ".config", "kicad")

    if base_path and os.path.exists(base_path):
        versions = [d for d in os.listdir(base_path) if d[0].isdigit() and os.path.isdir(os.path.join(base_path, d))]
        if versions:
            return [os.path.join(base_path, v) for v in versions]

    return []

def remove_easyeda2kicad_entries(config_path):
    # Clean kicad_common.json
    config_file = os.path.join(config_path, "kicad_common.json")
    if os.path.exists(config_file):
        with open(config_file, 'r') as file:
            config_data = json.load(file)

        if 'environment' in config_data and 'vars' in config_data['environment']:
            env_vars = config_data['environment']['vars']            
            if isinstance(env_vars, dict) and 'EASYEDA2KICAD' in env_vars:
                del env_vars['EASYEDA2KICAD']

        with open(config_file, 'w') as file:
            json.dump(config_data, file, indent=4)
        print("✅ EASYEDA2KICAD path removed from kicad_common.json")

    # Clean sym-lib-table
    sym_lib_table = os.path.join(config_path, 'sym-lib-table')
    if os.path.exists(sym_lib_table):
        with open(sym_lib_table, 'r') as file:
            lines = file.readlines()
        with open(sym_lib_table, 'w') as file:
            file.writelines([line for line in lines if 'easyeda2kicad.kicad_sym' not in line])
        print("✅ EasyEDA2KiCAD Symbol Library removed from sym-lib-table")

    # Clean fp-lib-table
    fp_lib_table = os.path.join(config_path, 'fp-lib-table')
    if os.path.exists(fp_lib_table):
        with open(fp_lib_table, 'r') as file:
            lines = file.readlines()
        with open(fp_lib_table, 'w') as file:
            file.writelines([line for line in lines if 'easyeda2kicad.pretty' not in line])
        print("✅ EasyEDA2KiCAD Footprint Library removed from fp-lib-table")

if __name__ == "__main__":
    config_paths = get_kicad_config_path()
    if not config_paths:
        print("❗ KiCad configuration file not found. Ensure KiCad has been run at least once.")
    else:
        for path in config_paths:
            remove_easyeda2kicad_entries(path)
