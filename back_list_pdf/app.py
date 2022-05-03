import pandas as pd
import fmrest
import requests
import json

from flask import Flask, render_template
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
@app.route('/')
def hello():
    return 'Hello, World!'


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
