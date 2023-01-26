from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [], 'excludes': []}

base = 'console'

executables = [
    Executable('queue_item.py', base=base)
]

setup(name='Queue Item',
      version = '1.0',
      description = '',
      options = {'build_exe': build_options},
      executables = executables)
