import pandas as pd
import fmrest
import requests
import json

from flask import Flask, render_template
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

FLUTTER_WEB_APP = 'templates'


@app.route('/')
def render_page():
    return render_template('index.html')

@app.route('/web/')
def render_page_web():
    return render_template('index.html')

@app.route("/api/getAllRecords", methods=["GET"])
def getAllRecords():
    fms = fmrest.Server(
        url='https://fm.cineklee.com',
        user='Admin',
        password='1234',
        database='contentManage',
        layout='contentDetailPdf'
    )
    fms.login()
    find_query = [{'createdby':'admin'}]
    fnds = fms.find(find_query)
    fms.logout()

    df = fnds.to_df()
    
    dfOk = df.drop(['modId','CreatedBy'], axis=1)
    df.set_index('recordId')
    dfOkOk = dfOk.rename(columns={"File Container": "link"})
    return dfOkOk.to_json(orient="records")

@app.route('/web/<path:name>')
def return_flutter_doc(name):

    datalist = str(name).split('/')
    DIR_NAME = FLUTTER_WEB_APP

    if len(datalist) > 1:
        for i in range(0, len(datalist) - 1):
            DIR_NAME += '/' + datalist[i]

    return send_from_directory(DIR_NAME, datalist[-1])