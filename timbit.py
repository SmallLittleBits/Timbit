# TODO:
#   - set root dir for storage
#   - add snippet / text
#   - add snippet / file
#   - search snippet
#   - edit snippet
#   - delete snippet
#   - write bio/help
#   - add user object
#   - add settings
#   -
#   -
#   -
#   - verbose
#   - set api key


import argparse
import sys
import os
import configparser
from tkinter import Tk


config = configparser.ConfigParser()
config.read('Config.ini')
print(config.sections())

parser = argparse.ArgumentParser(prog="Timbit", description="Timbit is a snippet tool")
group = parser.add_mutually_exclusive_group()
parser.add_argument("-r", "--root", help="Set root directory", default=config.get('Paths', 'root_dir'))
parser.add_argument("-c", "--clip", help="Add snippet from clipboard")
parser.add_argument("-f", "--file", help="Add snippet from path")
parser.add_argument("-o", "-options", help="Show setting options", type=int, choices=[0, 1, 2])
parser.add_argument("-v", "--verbose", help="Show more output", default=config.getboolean('Settings', 'verbose'))
parser.add_argument("-t", "--testing", help="Show better errors information", default=config.getboolean('Settings', 'testing'))


def pathIsValid(pathname: str) -> bool:

    try:
        # is valid str
        if not isinstance(pathname, str) or not pathname:
            return False

        if os.path.exists(pathname):
            if os.path.isdir(pathname):
                if os.access(pathname, os.W_OK):
                    return True
                else: return False
            else: return False
        # can create path
        elif os.access(pathname, os.W_OK):
            return True

    except Exception as e:
        if config.getboolean('Settings', 'testing'):
            print(e)
        return False

def getFromClipBoard() -> str:
    try:
        clipBoard = Tk()
        clip = clipBoard.withdraw()
        clipBoard.destroy()
        return clip
    except Exception as e:
        if config.getboolean('Settings', 'testing'):
            print(e)


def timbit():

    try:
        args = parser.parse_args()
        if args.testing:
            print("testing is on")
            print(args)
        if args.verbose:
            print("verbosity turned on")
            print(parser.parse_args())

        # set root path
        # todo: when dir not empty copy to new dir
        if args.root:
            path = args.root
            if pathIsValid(pathname=path):
                config.set('Paths', 'root_dir', value=args.root)
                with open('Config.ini', 'w') as configfile:
                    config.write(configfile)
                return
            else: print("Error: Path is not valid for root directory")


        # if args.root:
            # if not os.path.isdir(args.root):
            #     print('The path is not right')
            #     sys.exit()
            # print('\n'.join(os.listdir(args.root)))

        if args.a:
            print(f"a = {args.a}")
            return

        print(args) # for development
    # i don't think this is working but better to have it.
    except argparse.ArgumentError:
        print('Argument Error')
        print(parser.print_help())










if __name__ == '__main__':
    timbit()