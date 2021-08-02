import read_files as reader
import date_files as datefile

from pywebio.platform.flask import webio_view
from pywebio.output import *
from pywebio import start_server
from flask import Flask

import argparse

app = Flask(__name__)


def main():

    cols = ['VISN', 'DoDAAC', 'EXPECTED_DATE_OF_NEED']

    results = reader.read_NCRT_files(cols)

    date_col = 'EXPECTED_DATE_OF_NEED'
    visn_col = 'VISN'
    dodaac_col = 'DoDAAC'
    jul_col = 'julian'

    results[date_col] = datefile.object_datetime(results[date_col])
    results[jul_col] = datefile.datetime_julian(results[date_col]).astype('str')
    results['requisition'] = results[visn_col].astype('str')+\
                             results[dodaac_col].astype('str')+\
                             results[jul_col].astype('str')

    cols = ['A', 'B', 'C']
    a = results['requisition']
    b = results[visn_col]
    c = results[date_col]

    rows = [a, b, c]

    put_html('<h3>Edited Data Goes Here</h3>')
    put_table([
        cols,
        rows
    ])


app.add_url_rule('/', 'webio_view', webio_view(main),
                 methods=['GET', 'POST', 'OPTIONS'])

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    args = parser.parse_args()

    start_server(main, port=args.port, auto_open_webbrowser=True)