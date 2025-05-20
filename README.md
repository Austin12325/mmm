
# Minimal Mod Manager 

Minimal Mod Manager (MMM) is a script/program used to make the process of updating mods from NexusMods. It works by reading the hash of an archive downloaded from Nexusmods, checks if an update is available, and extracts it to a specified folder.  
![Example](https://github.com/Austin12325/mmm/blob/main/docs/example.gif)

# Requirements 
https://pypi.org/project/pynxm/

https://pypi.org/project/patool/

# Getting Started

If a terminal window doesn't open when executing the appimage or exe try executing it through a terminal window. 
When first opening the program you'll be met with a screen asking for your personal Nexusmods API key, which can be found [here](https://next.nexusmods.com/settings/api-keys) 
After that has been entered it will store they key in mmm_config.ini, this config file also stores your game information when you add a game. 

# Outline 

### Main Menu 
```
x------------------------------------x
|  1.)Game One                       |
|  2.)Game Two                       |
|  ____________                      |
|  Input number to select game       |
|  "a" to add game                   |
|  "d" to delete game                |
|  ____________                      |
x------------------------------------x
```

### Add Game Menu
```
x------------------------------------x
|                                    | 
|  Game Name:                        |
|                                    |
|  Variation:                        |
|                                    |
|  Where archives are stored:        |
|                                    |
|  Where to extract to:              |
|                                    |
x------------------------------------x
```
**Game Name**: The name found in your URL bar when browsing nexusmods, ex.) Darktide would be 'warhammer40kdarktide'

**Variation**: Can be anything, its used for games that have multiple different mod folders like in the case of Oblivion Remastered (ue4ss, pak mods, script extenders) this it will let you chose later which variation you would like to run the update operation on.

**Where Archives are stored**: For this program to work you need to store your zip files to check againt the zip files hosted on Nexusmods, personally I keep my zip files in my mods folder.

**Where to extract to**: This is where your mod files are stored, a drawback is that if the mods folders structure differ it might be challenging to manage and multiple variations will need to be made.

### Selected Game Menu
```
x------------------------------------------x
|                                          | 
|  Welcome User!                           |
|  no_update is at the newest version :)   |
|  mod_to_update  website found... opening:|
|      opening (website)                   |
|                                          |
|  Finished tasks!                         |
x------------------------------------------x
```




  
