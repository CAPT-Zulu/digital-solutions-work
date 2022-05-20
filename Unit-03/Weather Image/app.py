#!/usr/bin/env python  #step 1 import library
import json  # Step1 import libraries
import requests
from flask import Flask, render_template, request

# Step2 - create instance of Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'myverysectretkey'

url = "https://api.rainviewer.com/public/weather-maps.json"

@app.route('/', methods=['GET'])
def index():
    if request.args.get('c'):
        search_request = request.args.get('c')
        req2 = requests.get("https://nominatim.openstreetmap.org/search.php?format=json&q=" + search_request)
        data2 = json.loads(req2.content)
        weather_Location_Lat = data2[0]['lat']
        weather_Location_Lon = data2[0]['lon']
    else:
        weather_Location_Lat = "-27.4689682"
        weather_Location_Lon = "153.0234991"
        data2 = [{'place_id': 284015778, 'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright', 'osm_type': 'relation', 'osm_id': 11677792, 'boundingbox': ['-27.660219', '-27.022014', '152.679693', '153.468275'], 'lat': '-27.4689682', 'lon': '153.0234991', 'display_name': 'Brisbane City, Queensland, Australia', 'class': 'boundary', 'type': 'administrative', 'importance': 0.7694082277592821, 'icon': 'https://nominatim.openstreetmap.org/ui/mapicons//poi_boundary_administrative.p.20.png'}, {'place_id': 282737101, 'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright', 'osm_type': 'relation', 'osm_id': 2834528, 'boundingbox': ['37.6714255', '37.7082836', '-122.4265591', '-122.2501059'], 'lat': '37.687165', 'lon': '-122.402794', 'display_name': 'Brisbane, San Mateo County, California, 94005, United States', 'class': 'boundary', 'type': 'administrative', 'importance': 0.5264767185651252, 'icon': 'https://nominatim.openstreetmap.org/ui/mapicons//poi_boundary_administrative.p.20.png'}, {'place_id': 341367, 'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright', 'osm_type': 'node', 'osm_id': 153757063, 'boundingbox': ['41.4725319', '41.5125319', '-87.9778313', '-87.9378313'], 'lat': '41.4925319', 'lon': '-87.9578313', 'display_name': 'Brisbane, Will County, Illinois, 60451, United States', 'class': 'place', 'type': 'hamlet', 'importance': 0.35, 'icon': 'https://nominatim.openstreetmap.org/ui/mapicons//poi_place_village.p.20.png'}, {'place_id': 3681073, 'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright', 'osm_type': 'node', 'osm_id': 479696118, 'boundingbox': ['43.7245681', '43.7645681', '-80.0967202', '-80.0567202'], 'lat': '43.7445681', 'lon': '-80.0767202', 'display_name': 'Brisbane, Erin, Wellington County, Southwestern Ontario, Ontario, N0B 1T0, Canada', 'class': 'place', 'type': 'hamlet', 'importance': 0.35, 'icon': 'https://nominatim.openstreetmap.org/ui/mapicons//poi_place_village.p.20.png'}, {'place_id': 290873, 'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright', 'osm_type': 'node', 'osm_id': 151341877, 'boundingbox': ['46.322505', '46.362505', '-101.5109733', '-101.4709733'], 'lat': '46.342505', 'lon': '-101.4909733', 'display_name': 'Brisbane, Grant County, North Dakota, United States', 'class': 'place', 'type': 'hamlet', 'importance': 0.35, 'icon': 'https://nominatim.openstreetmap.org/ui/mapicons//poi_place_village.p.20.png'}, {'place_id': 139936719, 'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright', 'osm_type': 'way', 'osm_id': 165271232, 'boundingbox': ['14.6743782', '14.6754821', '121.1028229', '121.1039685'], 'lat': '14.6750175', 'lon': '121.1033015', 'display_name': 'Brisbane, Vista Real Classica, 2nd District, Quezon City, Eastern Manila District, Metro Manila, 2, Philippines', 'class': 'highway', 'type': 'residential', 'importance': 0.19999999999999998}, {'place_id': 109738803, 'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright', 'osm_type': 'way', 'osm_id': 32600274, 'boundingbox': ['51.7556893', '51.7558652', '-2.2851379', '-2.2824819'], 'lat': '51.7557531', 'lon': '-2.284014', 'display_name': 'Brisbane, Stonehouse, Stroud, Gloucestershire, South West England, England, GL10 2, United Kingdom', 'class': 'highway', 'type': 'residential', 'importance': 0.19999999999999998}, {'place_id': 102206520, 'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright', 'osm_type': 'way', 'osm_id': 16853534, 'boundingbox': ['14.6078033', '14.6125106', '121.0994766', '121.0999852'], 'lat': '14.6100681', 'lon': '121.0997168', 'display_name': 'Brisbane, Pasig Green Park Village, Pasig, Eastern Manila District, Metro Manila, 1612, Philippines', 'class': 'highway', 'type': 'residential', 'importance': 0.19999999999999998}, {'place_id': 143087946, 'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright', 'osm_type': 'way', 'osm_id': 173549451, 'boundingbox': ['14.4634029', '14.4656029', '121.0066356', '121.0080918'], 'lat': '14.464591', 'lon': '121.0074296', 'display_name': 'Brisbane, BF Homes, Parañaque, Southern Manila District, Metro Manila, 1718, Philippines', 'class': 'highway', 'type': 'residential', 'importance': 0.19999999999999998}, {'place_id': 101255181, 'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright', 'osm_type': 'way', 'osm_id': 15133733, 'boundingbox': ['29.502884', '29.5046873', '-98.323102', '-98.318654'], 'lat': '29.5046729', 'lon': '-98.3216781', 'display_name': 'Brisbane, Converse, Bexar County, Texas, 78109, United States', 'class': 'highway', 'type': 'residential', 'importance': 0.19999999999999998}]

    req = requests.get(url)
    data = json.loads(req.content)
    host = data['host']
    radarpath = data['radar']['nowcast'][0]['path']
    radarurl = (host + radarpath + "/512/1/" + weather_Location_Lat + "/" + weather_Location_Lon + "/3/0_0.png")

    return render_template('index.html', radarurl=radarurl, locations=data2)

if __name__ == '__main__':
    # host = '0.0.0.0'
    # port = 8080
    app.run(debug=True)
