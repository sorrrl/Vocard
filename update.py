import requests, zipfile, os, sys, shutil

root_dir = "./"
filename = root_dir + "Vocard.zip"
__version__ = "v2.5.1"

def checkVersion(withMsg = False):
    resp = requests.get("https://api.github.com/repos/ChocoMeow/Vocard/releases/latest")
    version = resp.json().get("name", __version__)
    if withMsg:
        if version == __version__:
            print(f"Your bot is up-to-date! - {version}")
        else:
            print(f"Your bot is not up-to-date! This latest version is {version} and you are currently running version {__version__}\n. Run `python update --start` to update your bot!")
    return version
    
def downloadFile(version:str = None):
    if not version:
        version = checkVersion()
    response = requests.get("https://github.com/ChocoMeow/Vocard/archive/" + version + ".zip")
    open(filename, 'wb').write(response.content)
    unZip(filename, version)

def unZip(path: str, version: str):
    with zipfile.ZipFile(path,"r") as f:
        f.extractall()

    version = version.replace("v", "")
    source_dir = root_dir + "Vocard-" + version
    if os.path.exists(source_dir):
        for filename in os.listdir(root_dir):
            if filename in ["settings.json", ".env", "Vocard-" + version]:
                continue
            if os.path.isdir(os.path.join(root_dir, filename)):
                shutil.rmtree(filename)
            else:
                os.remove(filename)
        for filename in os.listdir(source_dir):
            shutil.move(os.path.join(source_dir, filename), os.path.join(root_dir, filename))
        os.rmdir(source_dir)

def start():
    try:
        downloadFile()
        if os.path.exists(filename):
            os.remove(filename)
        print("Update Successfully! Run `python main.py` to start your bot")
    except Exception as e:
        print(f"Error: {e}")

if "--start" in sys.argv:
    start()

if "--check" in sys.argv:
    checkVersion(withMsg = True)