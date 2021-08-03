import read_files as reader
import date_files as datefile

from pywebio.platform.flask import webio_view
from pywebio.output import *
from pywebio import start_server
from flask import Flask

import argparse

app = Flask(__name__)


def main():
    cols = ['VISN', 'DoDAAC', 'EXPECTED_DATE_OF_NEED', 'EACH', 'CASE']

    results = reader.read_NCRT_files(cols)

    date_col = 'EXPECTED_DATE_OF_NEED'
    visn_col = 'VISN'
    dodaac_col = 'DoDAAC'
    jul_col = 'julian'
    each_col = 'EACH'
    case_col = 'CASE'

    results[date_col] = datefile.object_datetime(results[date_col])
    results[jul_col] = datefile.datetime_julian(results[date_col]).astype('str')
    results['requisition'] = results[visn_col].astype('str') + \
                             results[dodaac_col].astype('str') + \
                             results[jul_col].astype('str')

    final_results = results.groupby(['requisition', 'VISN', 'DoDAAC']).agg({each_col: sum,
                                                                            case_col: sum}).reset_index()

    data_cols = ['Requisition', 'VISN', 'DoDAAC', 'Count of EACH', 'Count of CASE']

    req = results['requisition']
    visn = results[visn_col]
    dodaac = results[dodaac_col]
    each = results[each_col]
    case = results[case_col]

    req_f = final_results['requisition']
    visn_f = final_results[visn_col]
    dodaac_f = final_results[dodaac_col]
    each_f = final_results[each_col]
    case_f = final_results[case_col]

    rows_1 = [req, visn, dodaac, each, case]
    rows_2 = [req_f, visn_f, dodaac_f, each_f, case_f]

    put_html('<h3>Original Data</h3>')
    put_table([
        data_cols,
        rows_1
    ])

    put_html('<h3>Summarized Data</h3>')
    put_table([
        data_cols,
        rows_2
    ])


app.add_url_rule('/', 'webio_view', webio_view(main),
                 methods=['GET', 'POST', 'OPTIONS'])

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    args = parser.parse_args()

    start_server(main, port=args.port, auto_open_webbrowser=True)
