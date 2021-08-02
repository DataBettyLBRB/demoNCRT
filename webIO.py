from pywebio.input import file_upload
from pywebio.output import put_html, put_loading
from pywebio import start_server
import re
import pandas as pd


def userXLSXUpload():
    files = file_upload(label="Upload your file", multiple=True, accept='.xlsx')

    for file in files:
        return pd.read_excel(file['content'])