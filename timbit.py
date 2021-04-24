# import click
#
# @click.group()
# @click.pass_context
# def timbit(self):
#     pass
#
# @timbit.command()
# @timbit.option('--name', prompt='Your name', help='The help')
# def test(name):
#     print(f"My name is {name}")
#
# cli = click.CommandCollection(sources=[timbit])

import argparse

def timbit():
    parser = argparse.ArgumentParser(description="What da program do")

    parser.add_argument("arg1", help="advice on arg1")
    parser.add_argument("arg2", help="advice on arg2")

    args = parser.parse_args()
    print(args)

if __name__ == '__main__':
    timbit()




