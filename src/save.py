#Imports
import os
import sys
import json



#Creates and returns where the save file should be stored
def get_save_path():
    #Checks which operating system is being used
    if sys.platform == "darwin":
        base = os.path.expanduser("~/Library/Application Support/Declare")
    else:
        base = os.path.join(os.path.expanduser("~"), ".declare")

    #Creates a folder if it does not already exist
    os.makedirs(base, exist_ok = True)

    #Returns save path
    return os.path.join(base, "save.json")



#Loads data from the save file
def load_save():
    #Gets save path
    path = get_save_path()

    #If no file exists, an empty dictionary is returned
    if not os.path.exists(path):
        return {}

    #Opens file, converts from JSON to Python object, and returns it
    with open(path, "r") as f:
        return json.load(f)



#Writes save data with a key-value pair 
def write_value(key, value):
    #Loads data and key
    data = load_save()
    data[key] = value

    #Saves the key-value pair as JSON
    with open(get_save_path(), "w") as f:
        json.dump(data, f)



#Reads save data with a key-value pair
def read_value(key, default=None):
    #Loads data and returns requested value
    data = load_save()
    return data.get(key, default)