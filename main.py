import gdown
import configparser
import zipfile
import os
import requests
import sys
import shutil

def debug(text):
    global arguments
    if arguments.get("debug") == True:
        print(text)
    return
#LOADING
arg = sys.argv
del arg[0]
arguments = dict(debug=False, fsset=False, folderclear=False)
for n in range(len(arg)):
    if arg[n] == "-debug":
        arguments["debug"] = True
    elif arg[n] == "-fs":
        arguments["fsset"] = True
    elif arg[n] == "-folderclear":
        arguments["folderclear"] = True
debug(f"-debug -fs -folderclear \n {arguments} \n")
if os.path.exists("config.ini") == False:
    debug("create config.ini")
    config = configparser.ConfigParser()
    config.add_section("main")
    config.set("main", "fs", 'True')
    config.set("main", "path", 'None')
    config["main"]["fs"] = 'True'
    with open('config.ini', 'w') as configfile:
            config.write(configfile)
if os.path.exists("data_cache") == False:
    os.mkdir("data_cache")
#LOADING

config = configparser.ConfigParser()
config.read("config.ini")
fs = config["main"]["fs"]
if fs == "True" or fs == True or arguments.get("fsset") == True:
    xxx = input("Write the path to the root folder of minecraft (minecraft. or some folder in the version): ")
    config["main"]["path"] = xxx
    config["main"]["fs"] = "False"
    with open('config.ini', 'w') as configfile:
            config.write(configfile)
    debug(f"path = {xxx}, fs = True")
else:
    xxx = config["main"]["path"]
    debug(f"path = {xxx}, fs = False")

r = requests.get('https://raw.githubusercontent.com/igorir3/histormodpackdata/main/modpackdata.dt')
debug(f"get RawGit")
f = open("data_cache\\data.dt",'w+')
r = r.text
debug(f"Git = {r}")
f.write(r)
debug(f"data create and close")
f.close()

file = open("data_cache\\data.dt", "r")
text_list = file.readlines()
url = text_list[0].rstrip(text_list[0][-1])
del text_list[0]
add_remove = text_list
for t in range(len(add_remove)):
    if add_remove[t][len(add_remove[t])-1] == '\n':
        s = list(add_remove[t]) # конвертируем в список
        del s[len(s)-1] # удаляем элемент с индексом index
        add_remove[t] = "".join(s)
debug(f"add_remove = {add_remove}")
#url = 'https://drive.google.com/uc?id=1QPBP7Ju07wvJ4Rs78D3tj76w8hBHaJBQ'
output = 'mods.zip'
file.close()
gdown.download(url, f"data_cache\\{output}", quiet=False)

with zipfile.ZipFile(f"data_cache\\{output}", 'r') as zip_file:
    print("Remove old files")
    if arguments.get("folderclear") == False:
        lii = zip_file.namelist()
        #add_remove = []
        for y in range(len(add_remove)):
            if add_remove[y] != '':
                lii.append(add_remove[y])
        debug(f"lii = {lii}")
        for x in range(len(lii)):
            print(f"Scaning {lii[x]}", end='\r')
            if os.path.exists(f"{xxx}\\{lii[x]}"):
                print(f"Removing {lii[x]}", end='\r')
                if os.path.isdir(f"{xxx}\\{lii[x]}") == True:
                    shutil.rmtree(f"{xxx}\\{lii[x]}")
                elif os.path.isfile(f"{xxx}\\{lii[x]}") == True:
                    os.remove(f"{xxx}\\{lii[x]}")
            else:
                print("Nope", end='\r')
    elif arguments.get("folderclear") == True:
        lii = zip_file.namelist()
        folders = []
        for t in range(len(lii)):
            word = ''
            for f in range(len(lii[t])):
                if lii[t][f] != "/":
                    word = word + lii[t][f]
                else:
                    break
            if len(folders) == 0:
                folders.append(word)
            else:
                error = False
                for o in range(len(folders)):
                    if folders[o] == word:
                        error = True
                if error == False:
                    folders.append(word)
        debug(folders)
        for x in range(len(folders)):
            print(f"Scaning {folders[x]}", end='\r')
            if os.path.exists(f"{xxx}\\{folders[x]}"):
                print(f"Removing {folders[x]}", end='\r')
                if os.path.isdir(f"{xxx}\\{folders[x]}") == True:
                    shutil.rmtree(f"{xxx}\\{folders[x]}")
                elif os.path.isfile(f"{xxx}\\{folders[x]}") == True:
                    os.remove(f"{xxx}\\{folders[x]}")
            else:
                print("Nope", end='\r')
    print("Extracting                                                                                             ")
    zip_file.extractall(f"{xxx}\\")

print("Remove trash")
os.remove(f"data_cache\\{output}")
os.remove("data_cache\\data.dt")

print("done!")
xxx = input("Press button for close installer")