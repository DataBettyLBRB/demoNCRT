from pywebio.input import file_upload
from pywebio.output import *
from pywebio.output import put_html, put_loading
from pywebio import start_server
import re
import pandas as pd


def userXLSXUpload():
    return file_upload(label="Upload your file", multiple=True, accept='.xlsx')


def createTable(cols, rows):
    return put_table([
        cols,
        rows
    ])