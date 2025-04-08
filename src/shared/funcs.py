import json
import sys
import os

def load_json_data(src: str) -> dict:
    """Load the data from a json file source directory as a dictionary."""
    with open(path(src), mode = "r", encoding = "utf-8") as file:
        json_data = json.load(file)
    
    return json_data

def update_json_data(
        src: str,
        data: dict
):
    """Update the data of a json file using its source dictionary."""
    with open(path(src), mode = "w", encoding = "utf-8") as file:
        json.dump(data, file, indent = 4)

def path(src: str) -> str:
    """Get the path of a file with fixed format for pyinstaller."""
    if src[0] == "/": # Remove / from beginning of string.
        src = src[1:]
    
    try:
        if hasattr(sys, "_MEIPASS"): # If meipass is present (it's packaged.)
            return os.path.join(sys._MEIPASS, src)
        
        else:
            # Returning normal non one-file but still packaged.
            return os.path.join(os.path.abspath("."), src)
    
    except:
        return src