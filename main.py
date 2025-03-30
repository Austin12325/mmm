import os 
import hashlib 
import patoolib 
import pynxm
import shutil
from mmm_settings import game,api_key,archives_dir,extract_dir

sources_dir = archives_dir if len(archives_dir)>3 else os.getcwd() # Where all your zip/rar files are.
nxm = pynxm.Nexus(api_key)
user = nxm.user_details()['name']
file_hash = []
downloading_files = []
delete_files = []
file_dict = {}

# downloads folder to move downloaded files to our mods folder 
# https://github.com/Nexus-Mods/node-nexus-api/blob/master/docs/classes/_nexus_.nexus.md#getdownloadurls
user_downloads = os.path.join('C:\\','Users',os.getlogin(),'Downloads') if os.name == 'nt' else os.path.join('home',os.getlogin(),'Downloads')

def question(string):
    print()
    print(string)
    print('Continue? [y], n')
    if input().lower() == 'n':
        return(False)
    else:
        return(True)

def main():
    print(f'Welcome {user}')
    if len(os.listdir(sources_dir)) > 50:
        if question('This directory has alot of files, I think you should be using a diffrent mod manager.') == False:
            quit()

    for file in os.listdir(sources_dir):
        if os.path.isdir(os.path.join(sources_dir,file)) == False:
            if patoolib.is_archive(os.path.join(sources_dir,file)):
                file_hash = hashlib.md5(open(os.path.join(sources_dir,file), 'rb').read()).hexdigest()
                try:
                    our_file = dict(nxm.mod_search(game,file_hash)[0])
                    nexus_file = nxm.mod_file_list(game,dict(nxm.mod_search(game,file_hash)[0])['mod']['mod_id'])['files'][-1]
                    if our_file['file_details']['uid'] == nexus_file['uid']:
                        print(f'\n{file} is at the newest version :)')
                    else:
                        os.system(f"start https://www.nexusmods.com/{game}/mods/{our_file['mod']['mod_id']}?tab=files")
                        print(f"\n{file} website found... opening: \n     https://www.nexusmods.com/{game}/mods/{our_file['mod']['mod_id']}?tab=files")

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
                patoolib.extract_archive(os.path.join(user_downloads,fixed_name),-1,sources_dir if extract_dir == '' else extract_dir)
                shutil.move(os.path.join(user_downloads,fixed_name),os.path.join(extract_dir,fixed_name))
                print(f'MOVED FILE!',os.path.join(user_downloads,fixed_name),os.path.join(sources_dir if extract_dir == '' else extract_dir,fixed_name))

            if question(f'Would you like to delete the old archives from mods folder? \n{delete_files}') == True:
                for file in delete_files:
                    os.remove(os.path.join(sources_dir,file)) 

    print('\nFinished tasks')

if game == '':
    game = input('Which game is this for? Please supply the name of the game in the URL bar of Nexusmods:\n')
if api_key == '':
    api_key = input('No API key provided, provide one now or add it to the mmm_settings.py file:\n')

main()