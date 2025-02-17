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
    #df = pd.read_csv("bulk.csv")
    #geos = df['geography code']
    #print(geos[0])
    #model = []
    #jsa = nomis._nomis_data(geography=wards,sex='7',item=1,measures=20100)
    #jsa.fillna(0)
    return getAllWards()

def getwards(wards):
    jsa = nomis._nomis_data(geography=wards,sex='7',item=1,measures=20100)
    print(jsa)
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

def getAllWards():
    # description : name
    # value : geo code
    df = nomis.nomis_codes_geog(geography='2092957697TYPE236')

    columns = ['description',"value"]
    df = pd.DataFrame(df, columns=columns)
    val = df['value'].values.tolist()

    val1 = val[0: 1000]
    val2 = val[1000:2000]
    val3 = val[2000:3000]
    val4 = val[3000:4000]
    val5 = val[4000:5000]
    val6 = val[5000:6000]
    val7 = val[6000:7000]
    val8 = val[8000:9000]
    val9 = val[9000: len(val)]

    vals = [val2, val3, val4, val5, val5, val6, val7, val8, val9]
    df = nomis._nomis_data(geography=val1,idx = "NM_162_1", age='11,12', measures='20100', gender="0").dropna()
    dfs = [df.values]
    for i in range(1, len(vals)):
        each = nomis._nomis_data(geography=vals[i],idx = "NM_162_1", age='11,12', measures='20100', gender="0").dropna()
        dfs.append(each.values)
    values = df.values
    mods = []
    data = {"claimant count data for 18-29 year olds ": mods}

    for each in dfs:
        rows, cols = each.shape
        for i in range(0, rows, 2):
            mods.append({"Geo_name ": each[i][1], "age-group" : {
                "age_name" : each[i][6], "value" :  each[i][7],
                "age_name" : each[i+1][6], "value" :  each[i+1][7]
            }})
        
    return jsonify(data)

if __name__== "__main__":
    app.run(port=5005, debug=True)
