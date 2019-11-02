from flask import Flask, request, jsonify
import nomis_api_wrapper
import ssl
import pandas as pd
import json

ssl._create_default_https_context = ssl._create_unverified_context

nomis=nomis_api_wrapper.NOMIS_CONFIG()

app = Flask(__name__)

@app.route('/fetchData')
def getData():
	with open('data.json') as f:
		data = json.load(f)
	ladName = request.args.get('lad')
	wardName = request.args.get('ward')
	for i in data['districts']:
		if i['districtName'] == ladName:
			for j in i['wards']:
				if j['ward_name'] == wardName:
					return j

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

@app.route('/highestDistrict')
def getHighestDistrict():
	with open('data.json') as f:
		data = json.load(f)
	districtData = []
	highName = 0
	highValue = 0
	for i in data['districts']:
		total = 0
		for ward in i['wards']:
			for j in ward['age-group']:
				total += j['value']
		if total > highValue:
			highValue = total
			highName = i['districtName']
		print(total)
	return {'name': highName, 'total': highValue}

@app.route('/highestWard')
def getHighestWard():
	with open('data.json') as f:
		data = json.load(f)
	districtData = []
	highName, highValue = 0, 0
	for i in data['districts']:
		for ward in i['wards']:
			total = 0
			for j in ward['age-group']:
				total += j['value']
			if total > highValue:
				highValue = total
				highName = ward['ward_name']
	return {'name': highName, 'total': highValue}

@app.route('/highestWardByAge')
def getHighestWardByAge():
	with open('data.json') as f:
		data = json.load(f)
	highName18, highValue18, highName25, highValue25 = 0,0,0,0
	for i in data['districts']:
		for ward in i['wards']:
			t1, t2 = 0,0
			for j in ward['age-group']:
				if '18' in j['age_name']:
					t1 = j['value']
				else:
					t2 = j['value']
			if t1 > highValue18:
				highValue18 = t1
				highName18 = ward['ward_name']
			if t2 > highValue25:
				highValue25 = t2
				highName25 = ward['ward_name']
	return jsonify([{'Name for 18-24': highName18, 'Total for 18-24': highValue18}, {'Name for 25-29': highName25, 'Total for 25-29': highValue25}])

@app.route('/highestDistrictByAge')
def getHighestDistrictByAge():
	with open('data.json') as f:
		data = json.load(f)
	highName18, highValue18, highName25, highValue25 = 0,0,0,0
	for i in data['districts']:
		t1, t2 = 0,0
		for ward in i['wards']:
			for j in ward['age-group']:
				if '18' in j['age_name']:
					t1 += j['value']
				else:
					t2 += j['value']
		if t1 > highValue18:
			highValue18 = t1
			highName18 = ward['ward_name']
		if t2 > highValue25:
			highValue25 = t2
			highName25 = ward['ward_name']
	return jsonify([{'Name for 18-24': highName18, 'Total for 18-24': highValue18}, {'Name for 25-29': highName25, 'Total for 25-29': highValue25}])

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

@app.route('/lads')
def getAllLads():
	districts = []
	data = {'country':"uk", 'districts': []}
	lads = nomis.get_geo_code(helper='LA_district',value="2092957697TYPE434").values
	rows, cols = lads.shape
	for i in range(rows):
		wards = nomis.get_geo_code(value=str(lads[i][1])+"TYPE236").values
		wardsGeoData = [wards[j][1] for j in range(wards.shape[0])]
		data['districts'].append({'districtName':lads[i][0], 'wards':getWardData(wardsGeoData)})
	return jsonify(data)

def getWardData(wardList):
	df = nomis._nomis_data(geography=wardList, idx="NM_162_1", age="11,12", measures="20100", gender="0").dropna().values
	mods = []
	rows, cols = df.shape
	for i in range(0, rows, 2):
		mods.append({'ward_name': df[i][1], "age-group": [
					{'age_name': df[i][6], 'value': df[i][7]},
					{'age_name': df[i+1][6], 'value': df[i+1][7]}
					]})
	return mods

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
            mods.append({"ward_name ": each[i][1], "age-group" : [
                {"age_name" : each[i][6], "value" :  each[i][7]},
                {"age_name" : each[i+1][6], "value" :  each[i+1][7]}
            ]})

    return jsonify(data)

if __name__== "__main__":
    app.run(port=5005, debug=True)
