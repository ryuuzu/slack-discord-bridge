import os
import json

def setup():
    needed_files = ['channels.json']
    files = [x for x in os.listdir() if os.path.isfile(x)]

    for x in needed_files:
        if x not in files:
            with open(x, "w") as f:
                json.dump({}, f)