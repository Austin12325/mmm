import os 
import hashlib 
import pynxm
import shutil
import configparser
import webbrowser
import sys

clear = 'cls' if os.name == 'nt' else 'clear'
os.system(clear)

def find_data_file(filename):
    if getattr(sys, "frozen", False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)
    return datadir
 
def game_selection():
    global game 
    global archives_dir
    global extract_dir  
    global api_key 

    file_dir = find_data_file(__file__)
    config = configparser.ConfigParser()
    config.read(os.path.join(file_dir,'mmm_config.ini'))

    # Reads the config file asking for users selection
    if config['Settings']['api_key'] == '':
        config['Settings']['api_key'] = input('No API key set, please provide one here: \n')
        with open(os.path.join(file_dir,'mmm_config.ini'),'w') as configfile:
            config.write(configfile)
            configfile.close()

    c = -1
    for key in config:
        if key not in ('DEFAULT','Settings'):
            print(c,')',key)
        c+=1
    print('-------\nInput Number to select game,\n "a" to add game,\n "d" to delete game\n-------')

    question = input()
    os.system(clear)
    if question == 'a':
        game_input = str(input('\nGame Name:\n'))
        archives_input = str(input('\nWhere archives are stored:\n'))
        extract_input = str(input('\nWhere to extract to:\n'))
        config[game_input] = {'name':game_input,
                            'archives_dir':archives_input,
                            'extract_dir':extract_input}
        with open(os.path.join(file_dir,'mmm_config.ini'),'w') as configfile:
            config.write(configfile)
            configfile.close()
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
                fixed_name = f"{file.split('.')[0]}({file_dict[file]}).{file.split('.')[1]}" if file_dict[file] != 0 else f"{file}"
                shutil.unpack_archive(os.path.join(user_downloads,fixed_name),sources_dir if extract_dir == '' else extract_dir,fixed_name.split('.')[-1])
                shutil.move(os.path.join(user_downloads,fixed_name),os.path.join(extract_dir,fixed_name))
                print(f'MOVED FILE!',os.path.join(user_downloads,fixed_name),os.path.join(sources_dir if extract_dir == '' else extract_dir,fixed_name))

            if question(f'Would you like to delete the old archives from mods folder? \n{delete_files}') == True:
                for file in delete_files:
                    os.remove(os.path.join(sources_dir,file)) 
    os.system(clear)
    print('\nFinished tasks!')

while game_selection() == 'FINISHED':
    pass

main()
