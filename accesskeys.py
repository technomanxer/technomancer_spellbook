#to do -- figure out how to adjust the path name based on OS (Windows/*nix path names are different)
with open(os.path.dirname(os.getcwd()) + '\\access_keys.txt') as json_file:
    keys = json.load(json_file)