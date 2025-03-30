
# Minimal Mod Manager 

Minimal Mod Manager (MMM) is a script/program used to make the process of updating mods from NexusMods. It works by reading the hash of an archive downloaded from Nexusmods, checks if an update is available, and extracts it to a specified folder.  

# Requirements 
https://pypi.org/project/patool/

https://pypi.org/project/pynxm/


# Setup

## mmm_settings.py
This is where you'll be setting your game specific settings.

---
#### game
--- 
The name of the game, when on nexusmods under the games mod page the game name will be in the URL. 

Ex.) The mods we want to install are from https://www.nexusmods.com/games/warhammer40kdarktide/mods, our games line would read as: game = 'warhammer40kdarktide'

---
#### api_key
--- 
Where your personal API key is stored, or it can be input durning each run of the script. The API key can be found here https://next.nexusmods.com/settings/api-keys

---
#### archives_dir
---
Where your zip/rar/7z files from Nexusmods are stored. If empty it will assume the same directory the script is being ran from. Personally I leave the zip files in the mods folder. 

---
#### extract_dir
---
Where we want to extract our zip file contents to. If empty it will assume the same directory the script is being ran from.
