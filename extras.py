import json

def loadfile(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def writefile(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f)