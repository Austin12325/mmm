import os 
import hashlib 
import pynxm
import shutil
import webbrowser
import sys
import patoolib
import json 
from difflib import SequenceMatcher as sm
clear = 'cls' if os.name == 'nt' else 'clear'

os.system(clear)

def question(string):
    print()
    print(string)
    print('Continue? [y], n')
    if input().lower() == 'n':
        return(False)
    else:
        return(True)
    
def find_data_file(filename):
    if getattr(sys, "frozen", False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)
    return datadir

def create_data(path):
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
    with open(path, 'w') as file:
        json.dump(x,file)

def write_data(path,load):
    # used for adding to variation
    # load['variation'][list(write)[0]] = write[list(write)[0]]
    with open(path, 'w') as file:
        json.dump(load,file)
        
def load_data(path):
    x = {'name':'oblivionremastered',
            'variation':{
                'ue4':{
                    'mod_path':'path_to_modding_folder',
                    'archive_path':'f'
                }
            }}
    with open(path, 'r') as file:
        return(json.load(file))

def game_selection():
    global game 
    global archives_dir
    global extract_dir  
    global api_key 

    file_dir = find_data_file(__file__)
    path = os.path.join(file_dir,'config.json')
    # Reads the config file asking for users selection
    config = load_data(path)
    print('config loaded')
    if config['Settings']['api_key'] == "":
        config['Settings']['api_key'] = input('No API key set, please provide one here: \n')
        
        write_data(path,config)
        os.system(clear)

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
        
        if game_input not in config['games']:
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
        
        # modify data based on our choices
        config['games'][game_input]['name'] = game_input
        config['games'][game_input]['settings']['variation'][variation] = {
                            'mod_path':extract_input,
                            'archive_path':archives_input
                        }
        
        write_data(path,config)
        os.system(clear)
        return 'FINISHED'

    elif question == 'd':
        os.system(clear)
        c = 0
        game_val = {}
        print('-------')
        print('1 ) Variation for a game')
        print('2 ) Game from Manager')
        question = input('thing to delete:\n')
        os.system(clear)
        if question == '2':
            # list games for deletion
            for var in config['games']:
                if var not in ('default','Settings'):
                    print(f'{c} ) {var}')
                    game_val.update({c:var})
                c+=1
            print('-------')
            question = input('game to delete:\n')

            print("REMOVING ",config['games'][game_val[int(question)]])
            config['games'].pop(game_val[int(question)])
        else:
            var_val = {}
            c = 0
            # list games for deletion
            for var in config['games']:
                if var not in ('default','Settings'):
                    print(f'{c} ) {var}')
                    game_val.update({c:var})
                c+=1
            print('-------')
            print('SET VAR')
            question1 = input('Select Game:\n')
            c = 1
            for var in config['games'][game_val[int(question1)]]['settings']['variation']:
                if var not in ('default','Settings'):
                    print(f'{c} ) {var}')
                    var_val.update({c:var})
                c+=1
            question2 = input('Variation to delete:\n')
            config['games'][game_val[int(question1)]]['settings']['variation'].pop(var_val[int(question2)])
        write_data(path,config)

        return 'FINISHED'
    else:
        game = config['games'][val[int(question)]]['name']
        # Run thing using this game
        var_val = {}
        # As the question of which variation if greater than 1 
        if len(config['games'][val[int(question)]]['settings']['variation']) >= 1:
            clear
            c = 1
            for var in config['games'][val[int(question)]]['settings']['variation']:
                print(f'{c} ) {var}')
                var_val.update({c:var})
                c+=1
            print(var_val)
        
            var_pick = input('Which variation would you like to manage?:\n')
        archives_dir = config['games'][val[int(question)]]['settings']['variation'][var_val[int(var_pick)]]['archive_path']
        extract_dir = config['games'][val[int(question)]]['settings']['variation'][var_val[int(var_pick)]]['mod_path'] 
        api_key = config['Settings']['api_key'] 
        return 'PASS'

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
                mod_dict = {}
                our_file = dict(nxm.mod_search(game,file_hash)[0])

                for mod in nxm.mod_file_list(game,dict(nxm.mod_search(game,file_hash)[0])['mod']['mod_id'])['files']:
                    if mod['category_name'] in ('OPTIONAL','MAIN'):
                        if len(mod_dict) == 0:
                            mod_dict.update({our_file['file_details']['name']:{'float':0.0,'file_id':'','file_name':''}})
                        
                        if sm(None,our_file['file_details']['name'],our_file['file_details']['name']).ratio() > mod_dict[our_file['file_details']['name']]['float']:
                            print('True',our_file['file_details']['name'],' is larger than existing dict')
                            mod_dict.update({our_file['file_details']['name']:{'float':float(sm(None,our_file['file_details']['name'],mod['name']).ratio()),'file_id':mod['file_id'],'file_name':mod['file_name']}})
 
                        # compare uid
                        if mod['uid'] == our_file['file_details']['uid']:
                            print('our_file UID not archived, up to date')
                            update = False
                            break
                        else:
                            update = True

                if update == False:
                    print(f"\n{file.split('-')[0]} is at the newest version :)")
                else:
                    webbrowser.open(f"https://www.nexusmods.com/{game}/mods/{our_file['mod']['mod_id']}?tab=files&file_id={mod_dict[our_file['file_details']['name']]['file_id']}")
                    print(f"\n{file} website found... opening: \n     https://www.nexusmods.com/{game}/mods/{our_file['mod']['mod_id']}?tab=files&file_id={mod_dict[our_file['file_details']['name']]['file_id']}")

                    delete_files.append(file)
                    downloading_files.append(mod_dict[our_file['file_details']['name']]['file_name']) # Append the newest file name as thats probably the one we want, if not, shoot. 


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
                shutil.move(os.path.join(user_downloads,fixed_name),os.path.join(archives_dir,fixed_name))
                print(f'MOVED FILE!',os.path.join(user_downloads,fixed_name),os.path.join(sources_dir if archives_dir == '' else archives_dir,fixed_name))

            if question(f'Would you like to delete the old archives from mods folder? \n{delete_files}') == True:
                for file in delete_files:
                    os.remove(os.path.join(sources_dir,file)) 
                    
    print('\nFinished tasks!')
    input()


if 'config.json' not in os.listdir(find_data_file(__file__)):
    create_data(os.path.join(find_data_file(__file__),'config.json'))

while game_selection() == 'FINISHED':
    pass

main()
