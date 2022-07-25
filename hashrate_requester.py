from datetime import datetime
import requests as requests

from config import db
from models import Coin, CoinHashrate


def pull_hashrates():
    coins = Coin.query.all()

    coin_symbols = ','.join([coin.symbol for coin in coins])
    hashrates = get_hashrate(coin_symbols)
    print('hashrate: ' + str(hashrates))

    for coin_symbol, hashrate in hashrates.items():
        week = int(datetime.now().strftime("%W"))
        coin = Coin.query.filter_by(symbol=coin_symbol).first()
        if not CoinHashrate.query.filter_by(coin_id=coin.id, week=week).first():
            coin_hashrate = CoinHashrate(
                coin_id=coin.id,
                hashrate=hashrate,
                week=week)
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
