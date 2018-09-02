import os.path
import sys
from cx_Freeze import setup, Executable

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

options = {
    'build_exe': {
        'include_files':[
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
            'rankings.csv',
            'draftorder.txt',
         ],
        "packages": ["sys", "os", "tkinter", "random", "numpy"],
    },
}

exe = Executable(script="main.py", targetName="pydraft.exe", base="Win32GUI")
base = None
setup( name = "pydraft",
       version = "1.0",
       description = "Pydraft",
       author = "Kyle Overstreet",
       options = options,
       executables = [exe])