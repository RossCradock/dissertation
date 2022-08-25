# https://wdc.kugi.kyoto-u.ac.jp/igrf/
import requests

from models import MiningLocation
from config import db

'''
solar_lat = 0: geomagnetic latitude = 0
solar_lat = 1: geomagnetic latitude = 60
solar_lat = 2: geomagnetic latitude = 50
solar_lat = 3: geomagnetic latitude = 40
'''


def geographic_to_geomagnetic(lat, long):
    url = 'https://omniweb.gsfc.nasa.gov/cgi/vitmo/cgm_model.cgi'
    # default values for post request
    post_data = {
        'model': 'cgm',
        'format': '0',  # list
        'geo_flag': '1',  # Geocentric
        'height': '0',  # height
        'profile': '1',  # height profile
        'start': '0.',
        'stop': '1.',
        'step': '2.',
        'year': '2022',
        'latitude': lat,
        'longitude': long,
        'vars': ['04']  # variables to return (04 = geomagnetic latitude)
    }

    response = requests.post(url, data=post_data)
    mag_lat = response.text[response.text.find('SP_CGM_Latitude') + 33:response.text.find('<hr></pre>')]
    return float(mag_lat)


def run_on_database():
    mining_pool_locations = MiningLocation.query.filter(MiningLocation.id > 32).all()
    for mining_pool_location in mining_pool_locations:
        if mining_pool_location.latitude is None or mining_pool_location.longitude is None:
            continue
        if -20.0 < mining_pool_location.latitude < 20.0:
            mining_pool_location.above_mag_40 = False
            mining_pool_location.above_mag_50 = False
            mining_pool_location.above_mag_60 = False
            mag_lat = mining_pool_location.latitude
        else:
            mag_lat = geographic_to_geomagnetic(mining_pool_location.latitude, mining_pool_location.longitude)
            mining_pool_location.above_mag_40 = mag_lat > 40
            mining_pool_location.above_mag_50 = mag_lat > 50
            mining_pool_location.above_mag_60 = mag_lat > 60

        print(mining_pool_location.id, ', ', mining_pool_location.country, ', ', mag_lat)
        db.session.add(mining_pool_location)
        db.session.commit()


run_on_database()

''' 
Test data
japan geograpic coordinates
lat: 35.4696, long: 137.613

japan returned geomagnetic coordinates according to http://dep1.iszf.irk.ru/en/examples/geo2gm
lat: 28.644508 

inside_blackout(35.4696, 137.613, 3)
'''
