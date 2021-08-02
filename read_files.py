import pandas as pd
import os
import webIO as io
from pywebio.input import file_upload


def read_filenames(path):
    return os.listdir(path)


def create_filepath(path, filename):
    return path + filename


def read_xlsx(file, sheet_name=''):
    if sheet_name:
        read = pd.read_excel(file['content'], header=[0])
    else:
        read = pd.read_excel(file['content'])
    return read


def read_NCRT_files(cols):
    list_files = io.userXLSXUpload()

    dfs = []

    for files in list_files:
        read_file = pd.read_excel(files['content'])

        df = pd.DataFrame(read_file)
        df = df.rename(columns=df.iloc[0]).drop(df.index[0])
        df = df[cols].dropna()

        dfs.append(df)

    return pd.concat(dfs)