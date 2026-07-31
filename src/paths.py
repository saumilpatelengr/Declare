#paths.py: Contains functions relating to file paths for the game
#Imports
import os
import sys



#Returns the absolute path to a file both before and after packaging
def resource_path(relative):
    #Check if the program is running as a packaged executable
    if getattr(sys, "frozen", False):
        #Uses temporary folder
        base = sys._MEIPASS
    else:
        #Uses the project's root folder
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    #Returns the full path to the file
    return os.path.join(base, relative)