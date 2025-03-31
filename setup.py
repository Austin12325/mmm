from cx_Freeze import setup, Executable
build_exe_options = {'include_files':['mmm_config.ini']}

setup(name='mmm.py',
    options = {'build_exe':build_exe_options},
    executables=[{'script':'mmm.py'}])