# TODO:
#   - update root dir ✓
#   - move existing files when updating root dir ✓
#   - add snippet / clipboard ✓
#   - add snippet / text ✓
#   - add snippet / file ✓
#   - add snippet / dir ✓
#   - duplicate file name exception handling
#   - add columns / default options and custom
#   - add custom column
#   - search snippet / search will be very important later on / apparently this is the best and baddest in the game / https://www.elastic.co/
#   - edit snippet
#   - delete snippet
#   - write bio/help
#   - add settings ✓
#   - add setting menu
#   - make start up script to set files and such
#   - add title & description to files that are saved
#   - verbose
#   - set api key
#   - Should look at adding terminal menu / 2 quick options / https://github.com/IngoMeyer441/simple-term-menu / https://github.com/aegirhall/console-menu


import argparse
import sys
import os
import configparser
import clipboard
import shutil
from pathlib import Path
from distutils.dir_util import copy_tree


config = configparser.ConfigParser()
config.read('Config.ini')
config.BOOLEAN_STATES = {'t': True, 'true': True, 'f': False, 'false': False,}


parser = argparse.ArgumentParser(prog="Timbit", description="Timbit is a snippet tool")
group = parser.add_mutually_exclusive_group()
group.add_argument('-r', '--root', help="Set root directory", metavar='Directory Path')
group.add_argument('-c', '--clip', help="Add snippet from clipboard", action='store_true')
group.add_argument('-t', '--text', help="Add snippet from input", action='store_true')
group.add_argument('-f', '--file', help="Add snippet from path", type=str, metavar='File Path')
group.add_argument('-d', '--dir', help="Add directory as snippet", type=str, metavar='Dir Path')
group.add_argument('-s', '--search', help="Search snippets", type=str)
group.add_argument('-e', '--edit', help="Edit snippet", type=str)
group.add_argument('-del', '--delete', help="Delete snippet", type=str)
parser.add_argument('-o', '--options', help="Show setting options", action='store_true')
parser.add_argument('-v', '--verbose', help="Show more output", type=str, metavar='True/False')
parser.add_argument('-test', '--testing', help="Show better error information", type=str, metavar='True/False')

def pathIsValidRoot(pathname: str) -> bool:
    # file name cleaning
    pathname = pathname.replace('"', '')
    pathname = pathname.replace("'", "")
    try:
        # is valid str
        if not isinstance(pathname, str) or not pathname:
            return False
        try:
            boo = os.path.exists(pathname)
            if boo:
                if os.path.isdir(pathname):
                    if os.access(pathname, os.W_OK):
                        old = config.get('Paths', 'root_dir')
                        if os.path.isdir(old):
                            copy_tree(old, pathname)
                            # probably should happen default set not to in settings
                            ans = validateForBool(input("Delete old directory? "))
                            if ans == 'True':
                                shutil.rmtree(old)
                        return True
                    else: return False
                else: return False
            else:
                os.access(pathname, os.W_OK)
                ans = validateForBool(input("This directory doesn't exist. \nCreate new directory? "))
                if ans == 'True':
                    # if existing files, move now
                    old = config.get('Paths', 'root_dir')
                    print('here')
                    if os.path.exists(old):
                        shutil.move(old, pathname)
                    # else make new (shouldn't happen unless user deletes directory manually
                    else:
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
        if args.root:
            path = args.root
            if path == config.get('Paths', 'root_dir'):
                print('This is already the root directory')
                return

            if pathIsValidRoot(pathname=path):
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
                file = open(fileName, 'x')
                file.write(getFromClipBoard())
                file.close()
            else:
                print('Please retry copying your entry, the last copied item will be saved')
            return


        # todo / first version seems to be working / fix for abs or not
        if args.file:
            p = args.file
            try:
                # path = Path(os.getcwd() + '\\' + p)
                path = os.path.abspath(p)
                if not os.path.isfile(path):
                    print(f"{path} is not a file, Please try again")
                    return
                f = open(path)
                if os.path.exists(path):
                    print(f"From File: {path}")
                    print("===============================")
                    print(f"{f.read()}")
                    print("===============================")
                ans = validateForBool(input("Is this what you want to save ? "))
                # todo: set for columns
                if ans == 'True':
                    defName, defSuffix = os.path.splitext(path)
                    title = input(f"Snippet name [default = {os.path.basename(os.path.normpath(defName))}]: ")
                    if title is None or title == '':
                        fileName = os.path.basename(os.path.normpath(path))  # gets only the last path name
                    else:
                        extension = input(f"Snippet suffix [default = {defSuffix}]:")
                        if extension is None or extension == '':
                            extension = defSuffix
                        fileName = title + extension
                    fileName = os.path.join(config.get('Paths', 'root_dir'), fileName)
                    shutil.copy(path, fileName)
            except Exception as e:
                # todo: improve later
                print(e)
            return

        if args.text:
            print("Please enter the text you'd like to save, Press Ctrl + Z to end: ")
            content = []
            # multiline adding
            while True:
                try:
                    line = input()
                except EOFError:
                    break
                content.append(line)
            fullText = ' '.join([str(elem + '\n') for elem in content]).replace('\n ', '\n') # replace a bit of a hack rn
            ans = validateForBool(input(f"\n===============================\n{fullText}\n===============================\nIs this correct ? "))
            if ans == 'True':
                title = input("What's the snippet name? ")
                extension = input("File extension? .")
                fileName = title + '.' + extension
                fileName = os.path.join(config.get('Paths', 'root_dir'), fileName)
                file = open(fileName, 'x')
                file.write(fullText)
                file.close()
            else:
                print("Please try again")

        if args.dir:
            p = args.dir
            try:
                path = os.path.abspath(p)
                if not os.path.isdir(p):
                    print(f"{path} is not a directory, Please try again")
                    return

                ans = validateForBool(input("Save entire directory recursively ?"))
                if ans == 'True':
                    title = input(f"Directory name [default = {path}]: ")
                    if title is None or title == '':
                        title = os.path.basename(os.path.normpath(path)) # gets only the last path name
                    shutil.copytree(path, os.path.join(config.get('Paths', 'root_dir'), title))
                    print('Done')

            except Exception as e:
                print(e)

        # todo: make actual menu not just print out
        if args.options:
            # primitive but works for now
            print(f"Version: {config.get('Timbit', 'version')}")
            print(f"Testing: {config.get('Settings', 'testing')}")
            print(f"Verbose: {config.get('Settings', 'verbose')}")
            print(f"Root Dir: {config.get('Paths', 'root_dir')}")
            return

        # No inputs -> print help
        # parser.print_help()
        # print("end: ", args) # for development


    # i don't think this is working but better to have it.
    except argparse.ArgumentError:
        print('Argument Error')
        print(parser.print_help())



if __name__ == '__main__':
    timbit()