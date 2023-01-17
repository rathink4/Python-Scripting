import os
import sys
import shutil
from subprocess import PIPE, run

GAME_DIRS_PATTERN = "game"

def getAllGamePaths(source):
    # Basically get a list of all the paths to the games
    game_path = []

    for root, dirs, files in os.walk(source):
        # source = 'data' directory and since only 'data' directory is concerned, we break through the loop immediately after 1 iteration
        for directory in dirs:
            # check if the directories in (source='data') contains the word 'game' in it, then append to list
            if GAME_DIRS_PATTERN in directory.lower():
                path = os.path.join(source, directory)
                game_path.append()
        
        break

    return game_path

def main(source, dest):
    # Get the current working directory and create the path to source & target
    cwd = os.getcwd()
    source_path = os.path.join(cwd, source)
    dest_path = os.path.joint(cwd, dest)
    


if __name__ == '__main__':
    # Get the command line arguments
    args = sys.argv

    # Since there will be only 2 arguments(src dir, dest dir), check to see if there are only 2 args
    if len(args) != 3:
        raise Exception("Pass source and destination directories only")

    source, dest = args[1:]
    main(source, dest)