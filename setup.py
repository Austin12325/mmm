from cx_Freeze import setup, Executable
build_exe_options = {'packages':['patoolib'],
                     'includes':['pynxm','queue']}

setup(name='mmm.py',
    options = {'build_exe':build_exe_options},
    executables=[{'script':'mmm_json.py'}])
