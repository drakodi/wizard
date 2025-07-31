import xbmc
import xbmcgui
import xbmcplugin
import xbmcvfs
import urllib.request
import zipfile
import os
import sys
from urllib.parse import parse_qsl

ADDON_ID = 'plugin.program.drakodi'
BASE_URL = 'https://github.com/drakodi/wizard/releases/download/v1.0.0/draKodi_Lite.zip'
BUILD_DIR = xbmcvfs.translatePath('special://home/userdata/addon_data/plugin.program.drakodi/builds/')

def main_menu():
    xbmcplugin.setPluginCategory(int(sys.argv[1]), 'draKodi Wizard')
    xbmcplugin.setContent(int(sys.argv[1]), 'addons')
    
    add_menu_item('Install draKodi Lite Build', 'install_build', 'draKodi_Lite.zip')
    add_menu_item('Install draKodi Pro Build', 'install_build', 'draKodi_Pro.zip')
    add_menu_item('Clear Cache', 'clear_cache')
    add_menu_item('Fresh Start (Wipes Kodi)', 'fresh_start')
    
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def add_menu_item(title, action, param=''):
    list_item = xbmcgui.ListItem(label=title)
    url = f'{sys.argv[0]}?action={action}&param={param}'
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), url, list_item, isFolder=False)

def install_build(build_zip):
    try:
        if not xbmcvfs.exists(BUILD_DIR):
            xbmcvfs.mkdirs(BUILD_DIR)

        build_url = BASE_URL + build_zip
        local_zip = os.path.join(BUILD_DIR, build_zip)

        dialog = xbmcgui.DialogProgress()
        dialog.create('draKodi Wizard', f'Downloading {build_zip}...')
        urllib.request.urlretrieve(build_url, local_zip)
        dialog.update(100, 'Extracting build...')

        with zipfile.ZipFile(local_zip, 'r') as zip_ref:
            zip_ref.extractall(xbmcvfs.translatePath('special://home/'))

        dialog.close()
        xbmcgui.Dialog().ok('draKodi Wizard', f'{build_zip} installed.\nKodi will now close.')
        xbmc.executebuiltin('ForceClose()')
    except Exception as e:
        xbmcgui.Dialog().ok('Error', f'Failed to install build: {e}')

def clear_cache():
    cache_paths = [
        xbmcvfs.translatePath('special://home/cache/'),
        xbmcvfs.translatePath('special://temp/')
    ]
    for path in cache_paths:
        if xbmcvfs.exists(path):
            for root, dirs, files in os.walk(path, topdown=False):
                for name in files:
                    try: os.remove(os.path.join(root, name))
                    except: pass
                for name in dirs:
                    try: os.rmdir(os.path.join(root, name))
                    except: pass
    xbmc.executebuiltin('Notification(draKodi Wizard,Cache Cleared!,5000)')

def fresh_start():
    userdata = xbmcvfs.translatePath('special://home/userdata/')
    keep = ['plugin.program.drakodi', 'repository.drakodi']
    for item in xbmcvfs.listdir(userdata)[1]:
        full_path = os.path.join(userdata, item)
        if item not in keep:
            if os.path.isdir(full_path):
                shutil.rmtree(full_path, ignore_errors=True)
            else:
                try: os.remove(full_path)
                except: pass
    xbmcgui.Dialog().ok("draKodi Wizard", "Fresh Start Complete.\nKodi will now close.")
    xbmc.executebuiltin('ForceClose()')

def router():
    params = dict(parse_qsl(sys.argv[2][1:]))
    action = params.get('action')
    param = params.get('param')

    if action == 'install_build':
        install_build(param)
    elif action == 'clear_cache':
        clear_cache()
    elif action == 'fresh_start':
        fresh_start()
    else:
        main_menu()

if __name__ == '__main__':
    router()
