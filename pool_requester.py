from datetime import datetime

from config import db
from models import Coin, MiningPool, PoolHashrate, PoolCoin

import requests
from requests.structures import CaseInsensitiveDict


def get_pool_data():
    coins = Coin.query.all()
    for coin in coins:
        response = send_request(coin.name)
        if response.status_code == 200:
            pool_data = response.json()
            for pool in pool_data['data']:
                # add to mining_pool if it doesn't exist
                mining_pool = MiningPool.query.filter_by(url=pool['url'], country=pool['country']).first()
                if not mining_pool:
                    # check if the mining pool is already in the database just with a url
                    mining_pool_by_url = MiningPool.query.filter_by(url=pool['url']).first()
                    if mining_pool_by_url:
                        mining_pool = mining_pool_by_url
                        mining_pool_by_url.country = pool['country']
                        db.session.commit()
                    else:
                        mining_pool = MiningPool(url=pool['url'], country=pool['country'])
                        db.session.add(mining_pool)
                        db.session.commit()

                # add to PoolHashrate if that week doesn't exist
                week = int(datetime.now().strftime("%W"))

                # see if there is hashrate data, and skip any pools that don't have any
                if pool['hashrate_average_7d_count'] == 0 or pool['hashrate_average_7d'] == 0:
                    continue

                if not PoolHashrate.query.filter_by(mining_pool_id=mining_pool.id, week=week).first():
                    pool_hashrate = PoolHashrate(
                        hashrate=pool['hashrate_average_7d'],
                        week=week,
                        mining_pool_id=mining_pool.id,
                        coin_id=coin.id)
                    db.session.add(pool_hashrate)
                    db.session.commit()

                if not PoolCoin.query.filter_by(coin_id=coin.id, mining_pool_id=mining_pool.id).first():
                    pool_coin = PoolCoin(
                        coin_id=coin.id,
                        mining_pool_id=mining_pool.id)
                    db.session.add(pool_coin)
                    db.session.commit()
        else:
            print("Error: " + str(response.status_code))


def send_request(coin_name):
    base_url = "https://data.miningpoolstats.stream/data/"
    param_t = get_website_last_update_time()
    if param_t is None:
        print("Error: Could not get website last update time")
        exit(1)

    url = base_url + coin_name.lower().replace(' ', '') + ".js?t=" + param_t
    print(url)

    headers = CaseInsensitiveDict()
    headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0"
    headers["Accept"] = "application/json"
    headers["Accept-Language"] = "en-GB,en;q=0.5"
    headers["Accept-Encoding"] = ""
    headers["Origin"] = "https://miningpoolstats.stream"
    headers["DNT"] = "1"
    headers["Connection"] = "keep-alive"
    headers["Referer"] = "https://miningpoolstats.stream/"
    headers["Sec-Fetch-Dest"] = "empty"
    headers["Sec-Fetch-Mode"] = "cors"
    headers["Sec-Fetch-Site"] = "same-site"
    headers["Pragma"] = "no-cache"
    headers["Cache-Control"] = "no-cache"

    return requests.get(url, headers=headers)


# this website only allows requests made from specific times
def get_website_last_update_time():
    current_unix_time = str(int(datetime.now().timestamp()))
    time_url = "https://miningpoolstats.stream/data/time"

    response = requests.get(time_url, params={"t": current_unix_time})
    if response.status_code == 200:
        print(str(response.text))
        return str(response.text)
    else:
        print("Error: " + str(response.status_code))
        return None
