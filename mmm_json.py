import os 
import hashlib 
import pynxm
import shutil
import configparser
import webbrowser
import sys
import patoolib
import json 
# clear = 'cls' if os.name == 'nt' else 'clear'
clear = ''
os.system(clear)
path = r'C:\Users\Austin\Documents\Minimal Mod Manager'
def find_data_file(filename):
    if getattr(sys, "frozen", False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)
    return datadir

def create_data():
    x = {'Settings':
            {
                'api_key':''
            },
            'games':{
                'default':{
                        'name':'',
                        'settings':{
                            'variation':{
                                '':{
                                    'mod_path':'path_to_modding_folder',
                                    'archive_path':'path_to_archive'
                                    }
                                }
                            }
                        }
                    }
            }
    with open(os.path.join(path,'config.json'), 'w') as file:
        json.dump(x,file)

def write_data(load):
    # used for adding to variation
    # load['variation'][list(write)[0]] = write[list(write)[0]]
    with open(os.path.join(path,'config.json'), 'w') as file:
        json.dump(load,file)
        

def load_data():
    x = {'name':'oblivionremastered',
            'variation':{
                'ue4':{
                    'mod_path':'path_to_modding_folder',
                    'archive_path':'f'
                }
            }}
    with open(os.path.join(path,'config.json'), 'r') as file:
        return(json.load(file))

def game_selection():
    global game 
    global archives_dir
    global extract_dir  
    global api_key 

    file_dir = find_data_file(__file__)
    
    # Reads the config file asking for users selection
    try:

        config = load_data()
        print(config['games'])
        if config['Settings']['api_key'] == "":
            config['Settings']['api_key'] = input('No API key set, please provide one here: \n')
            
            write_data(config)
    except:
        create_data()
        config = load_data()
    c = 0
    val = {}
    for k in config['games']:
        if k not in ('settings','variation','default'):
            print(c,')',config['games'][k]['name'])
            val.update({c:k}) 
        c+=1
    print('-------\nInput Number to select game,\n "a" to add game,\n "d" to delete game\n-------')

    question = input()
    os.system(clear)
    if question == 'a':
        game_input = str(input('\nGame Name:\n(Needs to be the name on Nexus)\n'))
        variation = str(input('\nWhat types of mods\n(used for picking between multiple mod formats per game)\n(can be anything):\n'))
        archives_input = str(input('\nWhere archives are stored:\n'))
        extract_input = str(input('\nWhere to extract to:\n(mods folder)\n'))
        try:
            orig_var = config['games'][game_input]['settings']['variation']
        except:
            orig_var = ''

        config['games'][game_input] = {'name':game_input,
                'settings':{
                    'variation':{
                        variation:{
                            'mod_path':extract_input,
                            'archive_path':archives_input
                        }
                    }
                }
            }
        config['games'][game_input]['settings']['variation'].update(orig_var)
        
        # config['games'][game_input]['settings']['variation']
        write_data(config)
        os.system(clear)
        return 'FINISHED'

    elif question == 'd':
        os.system(clear)
        c = -1
        for key in config:
            if key not in ('DEFAULT','Settings'):
                print(c,')',key)
            c+=1
        print('-------')
        question1 = input('game to delete:\n')
        if question1.isnumeric() == True:
            print("REMOVING ",config[config.sections()[int(question1)]]['name'])
            config.remove_section(config[config.sections()[int(question1)]]['name'])
        else:
            config.remove_section(question1)

        with open(os.path.join(file_dir,'mmm_config.ini'),'w') as configfile:
            config.write(configfile)
            configfile.close()
        
        os.system(clear)
        return 'FINISHED'
    else:
        # Run thing using this game
        print(len(config['games'][val[int(question)]]['settings']['variation']))
        
        
        
        
        



        game = config[config.sections()[int(question)]]['name']
        archives_dir = config[config.sections()[int(question)]]['archives_dir']
        extract_dir = config[config.sections()[int(question)]]['extract_dir'] 
        api_key = config['Settings']['api_key'] 
        return 'PASS'

def question(string):
    print()
    print(string)
    print('Continue? [y], n')
    if input().lower() == 'n':
        return(False)
    else:
        return(True)

def main():
    os.system(clear)
    file_hash = []
    downloading_files = []
    delete_files = []
    file_dict = {}
    nxm = pynxm.Nexus(api_key)
    user = nxm.user_details()['name']
    sources_dir = archives_dir if len(archives_dir)>3 else os.getcwd() # Where all your zip/rar files are.
    user_downloads = os.path.join('C:\\','Users',os.getlogin(),'Downloads') if os.name == 'nt' else os.path.join('home',os.getlogin(),'Downloads')

    print(f'Welcome {user}')
    if len(os.listdir(sources_dir)) > 50:
        if question('This directory has alot of files, I think you should be using a diffrent mod manager.') == False:
            quit()
    for file in os.listdir(sources_dir):
        if os.path.isdir(os.path.join(sources_dir,file)) == False:
            if file.split('.')[-1] in ('zip','rar','7z'):
                file_hash = hashlib.md5(open(os.path.join(sources_dir,file), 'rb').read()).hexdigest()
                try:
                    our_file = dict(nxm.mod_search(game,file_hash)[0])
                    nexus_file = nxm.mod_file_list(game,dict(nxm.mod_search(game,file_hash)[0])['mod']['mod_id'])['files'][-1]
                    if our_file['file_details']['uid'] == nexus_file['uid']:
                        print(f"\n{file.split('-')[0]} is at the newest version :)")
                    else:
                        webbrowser.open(f"https://www.nexusmods.com/{game}/mods/{our_file['mod']['mod_id']}?tab=files&file_id={nexus_file['file_id']}")
                        print(f"\n{file} website found... opening: \n     https://www.nexusmods.com/{game}/mods/{our_file['mod']['mod_id']}?tab=files&file_id={nexus_file['file_id']}")

                        delete_files.append(file)
                        downloading_files.append(nexus_file['file_name']) # Append the newest file name as thats probably the one we want, if not, shoot. 
                except:
                    
                    print(f'\nfailed to find mods website {file}')
                

    if len(downloading_files) != 0:
        if question('Are you finished downloading the mods? Would you like to extract them to your current directory or override folder?') == False:
            print("We're done here.")
            quit()
        else:
            print('Extracting stuff :)')
            for i in downloading_files:
                # Goal is to get the most recently downloaded file
                c = 0
                for file in os.listdir(user_downloads):
                        if f"{file.split('(')[0]}.{file.split('.')[-1]}" == i:
                            # Add file to dict and give it its number 
                            c+=1
                            file_dict[i] = c
                        else:
                            file_dict[i] = c

            for file in file_dict:
                
                # Add the number we get above to the folders name
                
                suffix_len = len(file.split('.')[-1])+1 #remove the period 
                
                fixed_name = f"{file[:-suffix_len]}({c}){file[-suffix_len:]}" if file_dict[file] != 0 else f"{file}"
                patoolib.extract_archive(os.path.join(user_downloads,fixed_name),-1,sources_dir if extract_dir == '' else extract_dir,fixed_name.split('.')[-1])
                # shutil.unpack_archive(os.path.join(user_downloads,fixed_name),sources_dir if extract_dir == '' else extract_dir,fixed_name.split('.')[-1])
                shutil.move(os.path.join(user_downloads,fixed_name),os.path.join(extract_dir,fixed_name))
                print(f'MOVED FILE!',os.path.join(user_downloads,fixed_name),os.path.join(sources_dir if extract_dir == '' else extract_dir,fixed_name))

            if question(f'Would you like to delete the old archives from mods folder? \n{delete_files}') == True:
                for file in delete_files:
                    os.remove(os.path.join(sources_dir,file)) 
                    
    print('\nFinished tasks!')
    input()
    
x = {'name':'oblivionremastered',
        'variation':{
            'ue6':{
                'mod_path':'path_to_modding_folder',
                'archive_path':'f'
            }
        }}
y = { 'ue4':{
                'mod_path':'path_to_modding_folder',
                'archive_path':'f'
            }
        }

game_selection()
# while game_selection() == 'FINISHED':
#     pass
