import json
import os
import sys
import shutil
from subprocess import PIPE, run

GAME_DIRS_PATTERN = "game"
GAME_EXTENSION = ".go"
GAME_COMPILE_CMD = ["go", "build"]

def createGameMetadataJson(json_path, game_dirs):
    data = {
        "gameNames": game_dirs,
        "numberOfGames": len(game_dirs)
    }

    with open(json_path, "w") as f:
        json.dump(data, f)


def copyOver(source, dest):
    # If there exist something in the dest, purge everything in it
    if os.path.exists(dest):
        shutil.rmtree(dest)
    
    # Copy over the content(s) from the source path to destination path
    shutil.copytree(source, dest)

def getGamesDirNames(paths, to_strip):
    # Find the name of the game directories without the 'game' part in the names. Store and return the names of the game directories
    # Eg = hello_world_game --> hello_world
    names = []
    for path in paths:
        # In the path, find the dir_name only using the .split() function and then remove the _game section
        _, dir_name = os.path.split(path)
        game_dir_name = dir_name.replace(to_strip, "")
        names.append(game_dir_name)
    
    return names

def createDirectory(dest):
    if not os.path.exists(dest):
        os.mkdir(dest)

def getAllGamePaths(source):
    # Basically get a list of all the paths to the games
    game_path = []

    for root, dirs, files in os.walk(source):
        # source = 'data' directory and since only 'data' directory is concerned, we break through the loop immediately after 1 iteration
        for directory in dirs:
            # check if the directories in (source='data') contains the word 'game' in it, then append to list
            if GAME_DIRS_PATTERN in directory.lower():
                path = os.path.join(source, directory)
                game_path.append(path)
        
        break

    return game_path

def compileGame(path):
    # Find the game file (game.go) and compile it using 'go build game.go' command
    game_file = None

    for root, dirs, files in os.walk(path):
        # source = any game directory (eg. 'hello_world') and since only the files in these directory is concerned, 
        # we break through the loop immediately after 1 iteration
        for file in files:
            if file.endswith(GAME_EXTENSION):
                game_file = file
                break
        
        break

    # Check if we actually found a file
    if game_file is None:
        return
    
    command = GAME_COMPILE_CMD + [game_file]
    runGame(command, path)

def runGame(cmd, path):
    # Change over to the game directory and then run the command
    cwd = os.getcwd()
    os.chdir(path)

    results = run(cmd, stdout=PIPE, stdin=PIPE, universal_newlines=True)
    print(results)

    # Change back to the cwd to avoid any issues
    os.chdir(cwd)

def main(source, dest):
    # Get the current working directory and create the path to source & target
    cwd = os.getcwd()
    source_path = os.path.join(cwd, source)
    dest_path = os.path.join(cwd, dest)

    game_paths = getAllGamePaths(source_path)
    game_dirs_name = getGamesDirNames(game_paths, "_game")

    createDirectory(dest_path)
    
    for source, dest in zip(game_paths, game_dirs_name):
        # You create destination_path = (cwd)/target/hello_world
        # Then you copy the contents from (cwd)/data/hello_world_game to cwd/target/hello_world
        destination_path = os.path.join(dest_path, dest)
        copyOver(source, destination_path)
        compileGame(destination_path)
    
    json_path = os.path.join(dest_path, "gameMetaData.json")
    createGameMetadataJson(json_path, game_dirs_name)


if __name__ == '__main__':
    # Get the command line arguments
    args = sys.argv

    # Since there will be only 2 arguments(src dir, dest dir), check to see if there are only 2 args
    if len(args) != 3:
        raise Exception("Pass source and destination directories only")

    source, dest = args[1:]
    main(source, dest)