from flask import render_template, redirect, jsonify

from config import app
from hashrate_requester import pull_hashrates
from pool_requester import get_pool_data
from models import CoinHashrate, Coin
from graph import get_graph_elements
import api


# routes
@app.route('/')
def home():
    #run_commands()
    #return 'done'
    return redirect('/bitcoin/solar/30')


@app.route('/<string:coin>/<string:scenario>/<int:week>')
def hello_world(coin, scenario, week):
    coin_id = Coin.query.filter_by(name=coin).first().id
    latest_week = CoinHashrate.query.filter_by(coin_id=coin_id).order_by(CoinHashrate.week.desc()).first().week
    graph = get_graph_elements(coin, week, scenario, [3])
    return render_template('index.html',
                           coin=coin,
                           week=latest_week,
                           scenario=scenario,
                           graph_script=graph[0],
                           graph_div=graph[1])


@app.route('/api/hashrate/solar/markers/<string:coin>/<string:week>/<int:solar_lat>')
def marker_solar_data(coin, week, solar_lat):
    return jsonify(api.marker_mining_pool_hashrate(coin, week, solar_lat))


@app.route('/api/hashrate/solar/graph/<string:coin>/<string:week>/<int:solar_lat>')
def graph_solar_data(coin, week, solar_lat):
    return jsonify(api.graph_mining_pool_hashrate(coin, week, solar_lat))


# commands
def run_commands():
    pass
    # pull_hashrates()
    # get_pool_data()


if __name__ == '__main__':
    app.run()
