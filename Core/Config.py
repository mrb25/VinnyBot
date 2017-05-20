import os

tokens = {}
commands = {}
info = {}
VINNY_COLOR = int('008cba', 16)


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

    with open("config/commands.txt", "r") as f:
        map = str.maketrans('', '', '*\n')
        for line in f:
            if line.startswith('***'):
                name = line.split(' ')[0].lower().translate(map)
                commands[name] = {}
                while True:
                    full = next(f)
                    if full.startswith('***') or full.startswith("END"):
                        break
                    command = full.split(' ')[0].replace('~', '')
                    print(command)
                    commands[name][command] = line


def getToken(tokenName):
    return tokens[tokenName]
