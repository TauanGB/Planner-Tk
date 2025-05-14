##python setup.py build

import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages":
    	["customtkinter",
        "tkinter",
        "os",
        "json",
        "time"],
        "include_files":[("icons", "icons")]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"
    
    

setup(
    name="Planner Tk",
    version="1.1",
    description="Planner de organizacao apartir de listas",
    options={"build_exe": build_exe_options},
    executables=[Executable("Planner.py", base=base,icon="icons/icon.ico")],    
)