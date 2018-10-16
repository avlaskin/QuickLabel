try:
    from tkinter import *
    from tkinter import messagebox as tkMessageBox
    import queue
except ImportError:
    from Tkinter import *
    import tkMessageBox
    import Queue as queue

import click
import pathlib
import os

from .ui.tkinter import Labeler


@click.command()
@click.option('--file-name', '-f', help='Name of .csv file')
@click.option('--input-dir', '-i', help='Location of the images.')
@click.option('--output-dir', '-o', help='Location to output .csv file.')
def main(output_dir, input_dir, file_name):
    """{{ cookiecutter.project_short_description }}"""
    if not input_dir:
        input_dir = '.'

    if not output_dir:
        output_dir = '.'

    if not file_name:
        file_name = 'labels.csv'

    if file_name[-4:] != '.csv':
        file_name += '.csv'

    input_dir = pathlib.Path(input_dir).resolve()
    output_dir = pathlib.Path(output_dir).resolve()

    click.echo(f'Input dir {input_dir}')
    click.echo(f'Output dir {output_dir}')

    output_path = str(output_dir) + os.sep + str(file_name)

    root = Tk()
    tool = Labeler(root, input_dir, output_path)
    root.resizable(width=True, height=True)
    root.mainloop()
