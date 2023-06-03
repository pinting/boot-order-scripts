import subprocess
import re

def get_entries():
    result = subprocess.check_output("efibootmgr", shell=True)
    lines = str(result).split("\\n")

    return lines

def filter_id(line):
    matches = re.findall("(Boot[0-9]{4})", line)

    if len(matches) > 0:
        return matches[0][4:]
    
    return ""
    
def is_windows(name):
    return "Windows Boot Manager" in name

def find_windows_id(lines):
    for line in lines:
        if is_windows(line):
            return filter_id(line)
    
    return ""

def set_boot_entry(new_id):
    return subprocess.check_output("efibootmgr -o " + new_id, shell=True)

def main():
    try:
        if set_boot_entry(find_windows_id(get_entries())):
            print("Success, set Windows to boot.")
        else:
            print("Error, failed to find Windows.")
    except:
        print("No permission to access boot order!")

if __name__ == "__main__":
    main()
