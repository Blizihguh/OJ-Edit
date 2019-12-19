# -*- coding: utf-8 -*-

# A simple setup script to create an executable using Tkinter. This also
# demonstrates the method for creating a Windows executable that does not have
# an associated console.
#
# SimpleTkApp.py is a very simple type of Tkinter application
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application

import sys
from cx_Freeze import setup, Executable

base = None
icon = "src/favicon.ico"
if sys.platform == 'win32':
    base = 'Win32GUI'

if len(sys.argv) > 2:
	if sys.argv[2] == "c":
		base = ""
	sys.argv.remove("c")

includefiles = ["src/favicon.ico","src/Readme.txt","src/ProgramFiles","src/OfficialFiles","src/Examples","src/OJ Palette.png"]
packages = ["Tkinter", "tkFileDialog"]
executables = [
    Executable('src/OJEdit.py', base=base, icon=icon)
]

build_exe_options = {"packages": ["numpy"], "include_files": includefiles}

setup(name='OJ Edit',
      version='2.0',
      description='OJ Editing Tool',
      executables=executables,
      options = {"build_exe": build_exe_options},
      )
