from datetime import datetime
import requests as requests

from config import db
from models import Coin, CoinHashrate


def pull_hashrates():
    coins = Coin.query.all()
    coin_ids = [coin.id for coin in coins]

    coin_symbols = ','.join([coin.symbol for coin in coins])
    hashrates = get_hashrate(coin_symbols)
    print('hashrate: ' + str(hashrates))

    for coin_symbol, hashrate in hashrates.items():
        coin = Coin.query.filter_by(symbol=coin_symbol).first()
        coin_id = coin.id
        week = int(datetime.now().strftime("%W"))
        coin_hashrate = CoinHashrate(coin_id=coin_id, hashrate=hashrate, week=week)
        db.session.add(coin_hashrate)

    db.session.commit()


def get_hashrate(coin_symbols):
    hashrates = {}

    print(coin_symbols)
    response = requests.get('https://api.minerstat.com/v2/coins?list=' + coin_symbols)
    response = response.json()
    print(response)

    for coin in response:
        hashrates[coin['coin']] = coin['network_hashrate']

    return hashrates
