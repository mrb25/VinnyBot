import os

tokens = {}

def initConfig():
    if not os.path.exists("config"):
        print("Config folder not present. Aborting")
        return None

    with open("config/tokens.txt", "r") as f:
        #Make translation map for removing new lines and *
        map = str.maketrans('', '', '*\n')
        for line in f:
            if line.startswith('***'):
                line = line.translate(map)
                tokens[line] = next(f).translate(map)

def getToken(tokenName):
    return tokens[tokenName]
