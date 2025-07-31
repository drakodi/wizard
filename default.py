import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
import os
import shutil
import zipfile
import urllib.request

ADDON = xbmcaddon.Addon()
ADDON_NAME = "draKodi Wizard"
HOME = xbmc.translatePath("special://home/")
BUILD_URL = "https://github.com/drakodi/wizard/releases/download/v1.0.0/draKodi_build.zip"
GUISETTINGS_URL = "https://github.com/drakodi/wizard/releases/download/v1.0.0/draKodi_guisettings.zip"

def download_and_extract(url, extract_path):
    zip_path = os.path.join(HOME, "temp.zip")
    urllib.request.urlretrieve(url, zip_path)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    os.remove(zip_path)

def apply_build():
    xbmcgui.Dialog().ok(ADDON_NAME, "Downloading and installing draKodi Build...")
    download_and_extract(BUILD_URL, HOME)
    xbmcgui.Dialog().ok(ADDON_NAME, "draKodi Build installed. Kodi will now close.")
    xbmc.executebuiltin("Quit()")

def apply_guisettings():
    xbmcgui.Dialog().ok(ADDON_NAME, "Applying GUI settings...")
    download_and_extract(GUISETTINGS_URL, os.path.join(HOME, "userdata"))
    xbmc.executebuiltin("ReloadSkin()")

def run():
    apply_build()
    apply_guisettings()

if __name__ == "__main__":
    run()