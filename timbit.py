import sys
import os
import click

@click.group()
@click.pass_context
def timbit(self):
    pass

@timbit.command()
def test():
    print("working")

cli = click.CommandCollection(sources=[timbit])

if __name__ == '__main__':
    timbit()


