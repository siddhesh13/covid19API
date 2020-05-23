from bs4 import BeautifulSoup
import requests
import time
import json
from pprint import pprint
##with open('sample.html') as html_file:
##    soup = BeautifulSoup(html_file, 'lxml')
##
##for article in soup.find_all('div', class_ ='article'):
##    ##print(article)
##
##    headline = article.h2.a.text
##    print(headline)
##    summary = article.p.text
##    print(summary)


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
    if len(stat) == 5:
        stats.append(stat)
india['confirmed'] = 0
for item in stats:
    india['confirmed'] += int(item[2]) 
    if item[1] == "Maharashtra":
        mah['confirmed'] = item[2]
        mah['active'] = int(item[2]) - int(item[3]) - int(item[4])
        mah['recovered'] = item[3]
        mah['deceased'] = item[4]
    #print(item[0] + ". " + item[1] + " - " + item[2] + ", " + item[3] + ", " + item[4]) 
#print(india)
india['confirmed'] //= 2
state = soup.find('table', class_ = 'table table-striped')
#print(state.tbody.text)



response = requests.get("https://api.covid19india.org/state_district_wise.json")
time.sleep(2)
state_data = response.json()
time.sleep(2)

all_in_one={}
all_in_one["India"] = india
all_in_one["Maharashra"] = mah
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

pprint(all_in_one)






