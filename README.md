
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
|  Where archives are stored:        |
|                                    |
|  Where to extract to:              |
|                                    |
x------------------------------------x
```

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




  
