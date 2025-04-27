import colorama
import json
import time
import pefile
import os

def writemetadata():
    colorama.init()

    print(colorama.Fore.GREEN + "Welcome To The Writer Utility" + "\n------------------------------------------")
    inp = input(colorama.Fore.RED + "What Would You Like To Do? [1.WriteMetaFromJson,2.Exit]: ").lower()
    
    ext_keys = {
        "CompanyName",
        "FileDescription",
        "FileVersion",
        "LegalCopyright",
        "ProductName",
        "ProductVersion",
        "Comments",
        "LegalTrademarks",
    }

    normal_keys = {
        "CompanyName",
        "FileVersion",
        "LegalCopyright",
        "ProductName",
        "ProductVersion",
    }

    match inp:
        case "1":
            try:
                file = input("Enter Your Json File(Ext included): ")
                with open(file, "r") as obj:
                    properties = json.load(obj)
                
                file_t = input("Enter Your file path and name: ")
                
                with open("config.json", 'r') as cfg:
                    config = json.load(cfg)
                    main_keys = ext_keys if bool(config["Extensive"]) else normal_keys
                
                for key in list(properties.keys()):
                    if key in main_keys:
                        pass
                    else:
                        properties.pop(key)
                        
            
                pe = pefile.PE(file_t)
                pe.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_RESOURCE"]])
                
                if not hasattr(pe, 'FileInfo'):
                    raise ValueError("no version information found in the executable")
                
                for fileinfo in pe.FileInfo:
                    for entry in fileinfo:
                        if entry.Key == b'StringFileInfo':
                            for st in entry.StringTable:
                                for key, value in properties.items():
                                    b_key = key.encode('utf-8')
                                    b_value = value.encode('utf-8')
                                    if b_key in st.entries:
                                        print(colorama.Fore.YELLOW + f"Updating {key} from {st.entries[b_key].decode('utf-8')} to {value}")
                                    else:
                                        print(f"Adding new property {key} = {value}")
                                    st.entries[b_key] = b_value
                
                output_path = os.path.join("metadata-writer", os.path.basename(file_t))
                pe.write(output_path)
                print(f"Process finished, find your new exe in {output_path}")
                
            except Exception as e:
                print(f"Error Occurred: {e}")
            finally:
                time.sleep(2)
                print("\033c")
                exit(1)
                
        case "2":
            exit(1)

