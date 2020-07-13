from flask import Flask, jsonify, render_template, Response, g, current_app as app, make_response
import os
import os.path
from bs4 import BeautifulSoup
import requests
import time
import json
app = Flask(__name__)



app = Flask(__name__)
india = {
    'active': 0,
    'confirmed': 0,
    'deceased': 0,
    'recovered': 0
    }

mah = {
    'active': 0,
    'confirmed': 0,
    'deceased': 0,
    'recovered': 0
    }
mah_dist = {
    "Mumnai": {
        'Total Cases': 0,
        'Active Cases': 0,
        'Cured': 0,
        'Deaths': 0,
        "delta":{
            "Total Cases": 0,
            'Cured': 0,
            'Deaths': 0
            }
        },
    "Pune": {
        'Total Cases': 0,
        'Active Cases': 0,
        'Cured': 0,
        'Deaths': 0,
        "delta":{
            "Total Cases": 0,
            'Cured': 0,
            'Deaths': 0
            }
        },
    "Thane": {
        'Total Cases': 0,
        'Active Cases': 0,
        'Cured': 0,
        'Deaths': 0,
        "delta":{
            "Total Cases": 0,
            'Cured': 0,
            'Deaths': 0
            }
        }
    }
allstate_data = {}
source = requests.get('https://www.mohfw.gov.in/').text
soup = BeautifulSoup(source,'lxml')
active = soup.find('li', class_ = 'bg-blue')
cured = soup.find('li', class_ = 'bg-green')
deaths = soup.find('li', class_ = 'bg-red')
migrated = soup.find('li', class_ = 'bg-orange')
india['active'] = active.strong.text
india['recovered'] = cured.strong.text
india['deceased'] = deaths.strong.text

extract_contents = lambda row: [x.text.replace('\n','') for x in row]
stats = []
all_rows = soup.find_all('tr')

for row in all_rows:
    stat = extract_contents(row.find_all('td'))
    if len(stat) == 6:
        stats.append(stat)

for item in stats:
    allstate_data[item[1]] = {'active':'', 'recovered':'', 'deaths':'', 'confirmed':''} 
    allstate_data[item[1]]['active']= item[2]
    allstate_data[item[1]]['recovered'] = item[3]
    allstate_data[item[1]]['deaths'] = item[4]
    allstate_data[item[1]]['confirmed'] = item[5]
    #del state_data[item[0]][item[1]]
    
for item in stats:
    india['confirmed'] += int(item[5])
    if item[1] == "Maharashtra":
        mah['confirmed'] = item[5]
        mah['active'] = int(item[2])
        mah['recovered'] = item[3]
        mah['deceased'] = item[4]
    #print(item[0] + ". " + item[1] + " - " + item[2] + ", " + item[3] + ", " + item[4]) 
#print(india)
india['confirmed'] //= 2
state = soup.find('table', class_ = 'table table-striped')
#print(state.tbody.text)



response = requests.get("https://api.covid19india.org/state_district_wise.json")
#time.sleep(1)
state_data = response.json()
#time.sleep(1)
#print(state_data)
all_in_one={}
all_in_one["India"] = india
all_in_one["Maharashtra"] = mah
district = ["Mumbai", "Pune", "Thane"]
for d in district:
    if d in state_data["Maharashtra"]["districtData"]:
        mah_dist[d] = state_data["Maharashtra"]["districtData"][d]
        del mah_dist[d]['notes']
        del mah_dist[d]['delta']
##        print(d + ": ")
##        print(mah_dist[d])
        all_in_one[d] = mah_dist[d] 
       
##for key, values in all_in_one.items():
##    print(key)
##    print(values)


@app.route('/india')
def india():
   return jsonify(all_in_one["India"])

@app.route('/maharashtra')
def maharashtra():
   return jsonify(all_in_one["Maharashtra"])

@app.route('/mumbai')
def mumbai():
   return jsonify(all_in_one["Mumbai"])

@app.route('/pune')
def pune():
   return jsonify(all_in_one["Pune"])

@app.route('/thane')
def thane():
   return jsonify(all_in_one["Thane"])

@app.route('/data')
def all():
   return jsonify(all_in_one)

@app.route('/state_data')
def all_states():
   return jsonify(allstate_data)


@app.route('/')
def ok():
   return "API for numbers of covid19 cases in India, Maharashtra, Mumbai, Pune and Thane."



if __name__ == '__main__':
    app.run(debug=True)


