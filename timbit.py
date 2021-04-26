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
import clipboard
import pathlib


config = configparser.ConfigParser()
config.read('Config.ini')
config.BOOLEAN_STATES = {'t': True, 'true': True, 'f': False, 'false': False,}


parser = argparse.ArgumentParser(prog="Timbit", description="Timbit is a snippet tool")
group = parser.add_mutually_exclusive_group()
group.add_argument("-r", "--root", help="Set root directory")
group.add_argument("-c", "--clip", help="Add snippet from clipboard")
group.add_argument("-f", "--file", help="Add snippet from path")
group.add_argument("-o", "-options", help="Show setting options", type=int, choices=[0, 1, 2])
group.add_argument("-v", "--verbose", help="Show more output", type=str)
group.add_argument("-t", "--testing", help="Show better errors information", type=str)


def pathIsValid(pathname: str) -> bool:
    try:
        # is valid str
        if not isinstance(pathname, str) or not pathname:
            return False
        try:
            boo = os.path.exists(pathname)
            if boo:

                if os.path.isdir(pathname):
                    if os.access(pathname, os.W_OK):
                        return True
                    else: return False
                else: return False
            else:
                os.access(pathname, os.W_OK)
                ans = validateForBool(input("This directory doesn't exist. \nCreate new directory? "))
                if ans == 'True':
                    os.mkdir(pathname)
                    return True
                else:
                    print("Directory not made, Root directory not set.")
                    return True
        except Exception as e:
            if config.getboolean('Settings', 'testing'):
                print(e)
            return False
    except Exception as e:
        if config.getboolean('Settings', 'testing'):
            print(e)
        return False

def getFromClipBoard() -> str:
    try:
        clip = clipboard.paste()
        return clip
    except Exception as e:
        if config.getboolean('Settings', 'testing'):
            print(e)

def writeToConfig():
    with open('Config.ini', 'w') as configfile:
        config.write(configfile)

def validateForBool(arg: str) -> str:
    if arg.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'yep', 'certainly', 'uh-huh']:
        return 'True'
    elif arg.lower() in ['false', '0', 'f', 'n', 'no', 'nope', 'no-way', 'hell-no']:
        return 'False'
    else:
        print(f"Invalid entry: {arg}, please enter something nice ex [True, False, t, f, 1, 0]")
        sys.exit()

def timbit():

    try:
        # get args from cl
        args = parser.parse_args()

        # testing and verbose
        if args.testing:
            t = validateForBool(args.testing)
            config.set('Settings', 'testing', value=t)
            writeToConfig()
            print(f"testing is {config.get('Settings', 'testing')}")

        if args.verbose:
            v = validateForBool(args.verbose)
            config.set('Settings', 'verbose', value=v)
            writeToConfig()
            print(f"verbosity turned {config.get('Settings', 'verbose')}")


        # set root path
        # todo: when dir not empty copy to new dir
        if args.root:
            path = args.root

            if path == config.get('Paths', 'root_dir'):
                print('This is already the root directory')
                return

            if pathIsValid(pathname=path):
                config.set('Paths', 'root_dir', value=args.root)
                writeToConfig()
                return
            else:
                print("Error: Path is not valid for root directory")
                sys.exit()


        if args.clip:
            print("===============================")
            print(f"{getFromClipBoard()}")
            print("===============================")
            ans = validateForBool(input("Is this what you want to save ? "))
            # todo: set for columns
            if ans == 'True':
                title = input("What's the snippet name? ")
                extension = input("File extension? .")
                # i made some dumb mistakes so this is kinda spread apart and gross
                fileName = title + '.' + extension
                fileName = os.path.join(config.get('Paths', 'root_dir'), fileName)
                print(fileName)
                file = open(fileName, 'x')
                file.write(getFromClipBoard())
                file.close()
            else:
                print('Please retry copying your entry')
            return


        # todo
        if args.file:
            print(f"file = {args.file}")
            return

        # todo
        if args.options:
            print(f"options = {args.options}")
            return

        # No inputs -> print help
        parser.print_help()
        print("end: ", args) # for development


    # i don't think this is working but better to have it.
    except argparse.ArgumentError:
        print('Argument Error')
        print(parser.print_help())



if __name__ == '__main__':
    timbit()