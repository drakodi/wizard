import xbmcaddon, xbmcgui, xbmc, xbmcplugin
import urllib.request
import json
import os
import sys

addon_id = 'plugin.program.drakodi'
addon = xbmcaddon.Addon(id=addon_id)
dialog = xbmcgui.Dialog()
base_url = 'https://raw.githubusercontent.com/drakodi/wizard/main/'
builds_file = 'builds.txt'

def get_builds():
    try:
        response = urllib.request.urlopen(base_url + builds_file)
        content = response.read().decode('utf-8')
        return parse_builds(content)
    except:
        dialog.ok("Drakodi Wizard", "Failed to fetch build list.")
        return []

def parse_builds(data):
    lines = data.strip().splitlines()
    builds = []
    build = {}
    for line in lines:
        if '=' not in line:
            continue
        key, val = line.split('=', 1)
        key, val = key.strip().lower(), val.strip()
        if key == 'name':
            if build:
                builds.append(build)
                build = {}
            build['name'] = val
        elif key in ['url', 'icon', 'fanart']:
            build[key] = val
    if build:
        builds.append(build)
    return builds

def install_build(build):
    dialog.ok("Drakodi Wizard", f"To install: {build['name']}\nGo to Downloader and enter:\n{build['url']}")
    # You can enhance this to auto-download and extract if desired

def show_menu():
    builds = get_builds()
    if not builds:
        return
    for i, build in enumerate(builds):
        xbmcplugin.addDirectoryItem(
            handle=int(sys.argv[1]),
            url=f'{sys.argv[0]}?mode=install&index={i}',
            listitem=xbmcgui.ListItem(label=build["name"], thumbnailImage=build.get("icon", ""), iconImage="DefaultProgram.png"),
            isFolder=False
        )
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def route(params):
    import urllib.parse as urlparse
    query = urlparse.parse_qs(params)
    mode = query.get('mode', [None])[0]
    index = int(query.get('index', [0])[0])
    builds = get_builds()
    if mode == 'install':
        install_build(builds[index])

if __name__ == '__main__':
    if '?' in sys.argv[2]:
        route(sys.argv[2][1:])
    else:
        show_menu()
