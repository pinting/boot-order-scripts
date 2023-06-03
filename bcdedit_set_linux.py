import subprocess
import re

def get_entries():
    result = subprocess.check_output("bcdedit /enum firmware", shell=True)
    lines = str(result).split("\\r\\n")

    return lines

def filter_id(line):
    matches = re.findall("(\{[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}\})", line)

    if len(matches) > 0:
        return matches[0]
    
    return ""

def is_linux(name):
    return "Ubuntu" in name or "Pop!_OS" in name

def find_linux_id(lines):
    current_entry_id = ""

    for line in lines:
        # identifier is always the first line in each entry
        if "identifier" in line:
            current_entry_id = filter_id(line)
        elif "description" in line and is_linux(line):
           return current_entry_id
    
    return ""

def set_boot_id(new_id):
    return subprocess.check_output("bcdedit /set {fwbootmgr} displayorder " + new_id + " {bootmgr}", shell=True)

def main():
    try:
        if set_boot_id(find_linux_id(get_entries())):
            print("Success, set Linux to boot.")
        else:
            print("Error, failed to find Linux.")
    except:
        print("No permission to access boot order!")

if __name__ == "__main__":
    main()