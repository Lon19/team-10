from flask import Flask, request, jsonify
import nomis_api_wrapper
import ssl
import pandas as pd

ssl._create_default_https_context = ssl._create_unverified_context

nomis=nomis_api_wrapper.NOMIS_CONFIG()

app = Flask(__name__)

@app.route("/ward")
def wardTotal():
    print("request accepted")
    headers = request.headers
    value = headers['ward']
    result = getjsafor(ward)
    return jsonify({"ward_name : ":value, "total_jsa": result})

@app.route('/wards')
def getWards():
    df = pd.read_csv("bulk.csv")
    geos = df['geography code']
    print(geos[0])
    model = []
    jsa = nomis._nomis_data(geography=wards,sex='7',item=1,measures=20100)
    jsa.fillna(0)
    return jsonify(model)

def getwards(wards):
    jsa = nomis._nomis_data(geography=wards,sex='7',item=1,measures=20100)
    pass
def getjsafor(ward):
    dd = nomis.get_geo_code(helper ='LA_district', search = ward)
    print(dd[dd.description == ward]['geog'].values)
    geo = dd[dd.description == ward]['geog'].values
    if geo:
        jsa = nomis._nomis_data(geography=geo,sex='7',item=1,measures=20100)
        result = int(jsa['OBS_VALUE'])
    else:
        result = 0
    return result

if __name__== "__main__":
    app.run(port=5005, debug=True)
