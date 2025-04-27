import os
import time
import colorama
import subprocess
import json
colorama.init()

print(colorama.Fore.GREEN + "Welcome To The Reader Utility")
inp = input("What is the file name and extension you want to get the contents of?\n(Must Provide a Relative or Absolute Path): ")

try:
    stat = os.stat(inp)
    
    if stat:
        print("Stats:")
        print(colorama.Fore.CYAN + f"Size: {stat.st_size} bytes")
        print(colorama.Fore.CYAN + f"Created: {time.ctime(stat.st_ctime)}")
        print(colorama.Fore.CYAN + f"Modified: {time.ctime(stat.st_mtime)}")
        print(colorama.Fore.CYAN + f"Accessed: {time.ctime(stat.st_atime)}")
        var = subprocess.getoutput(f"""powershell -command "Get-ItemProperty '{inp}' | Format-List *""")
        print(var)
        inp1 = input("Would You Like To Write This To A file?(True=File_name,False=Enter)")
        if inp1:
            properties = {}
            for p in var.split("\n"):
                if ":" in p:
                    key,val = p.strip(" ").split(":", 1)
                    properties[key.strip()] = val.strip()
                    
            obj = open(f"metadata-reader\\{inp1}", "w")
            json.dump(properties, obj, indent=4)
            print(colorama.Fore.YELLOW + "saved to metadata-reader as" + inp1 if ".json" in inp1 else inp1 + ".json")
            print("\033c")
        else:
            print("\033c")
    else:
        print(colorama.Fore.RED + "This file doesnt have any attributes")
        print("\033c")

except Exception as e:
    print(colorama.Fore.RED + f"Error: {e}")