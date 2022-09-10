from models import Coin, MiningPool, MiningLocation, PoolHashrate, CoinHashrate
from config import db
from util import hashrate_normalizer


def marker_mining_pool_hashrate(coin, week, solar_lat):
    query_data = get_hashrates_from_database(coin, week, solar_lat)
    markers_data = []
    for row in query_data:
        already_added = False
        latitude = row[1].latitude
        latitude = 0 if latitude is None else latitude
        longitude = row[1].longitude
        longitude = 0 if longitude is None else longitude
        hashrate_normalized = hashrate_normalizer.normalize_hashrate(coin, row[0].hashrate)
        if len(markers_data) == 0:
            row_list = [latitude, longitude, hashrate_normalized]
            markers_data.append(row_list)
            continue

        for previous_row in markers_data:
            if previous_row[0] == latitude and previous_row[1] == longitude:
                markers_data[markers_data.index(previous_row)][2] += hashrate_normalized
                already_added = True

        if already_added:
            continue
        else:
            row_list = [latitude, longitude, hashrate_normalized]
            markers_data.append(row_list)

    return markers_data


def graph_mining_pool_hashrate(coin, week, solar_lat):
    query_data = get_hashrates_from_database(coin, week, solar_lat)
    coin_id = query_data[0][0].coin_id
    total_coin_hashrate = float(CoinHashrate.query.filter_by(coin_id=coin_id, week=week).first().hashrate)
    if solar_lat != 0:
        total_coin_hashrate = 0
        for row in query_data:
            total_coin_hashrate += float(row[0].hashrate)

    graph_data = {}
    other_exists = False
    for row in query_data:
        mining_pool_url = row[2].url

        # remove unneccecary parts of the url
        if 'www' in mining_pool_url:
            mining_pool_display_url = mining_pool_url[mining_pool_url.find('www') + 4:]
        else:
            mining_pool_display_url = mining_pool_url[mining_pool_url.find('//') + 2:]
        if '/' in mining_pool_display_url:
            mining_pool_display_url = mining_pool_display_url[:mining_pool_display_url.find('/')]

        # create percentages
        mining_pool_hashrate = float(row[0].hashrate)
        mining_pool_percentage = round(mining_pool_hashrate / float(total_coin_hashrate) * 100, 4)

        # if percentage is less than 1% add to other
        if mining_pool_percentage < 1:
            # no other entry exists yet
            if not other_exists:
                other_exists = True
                graph_data['Other'] = [mining_pool_hashrate, mining_pool_percentage]
            # other entry exists, add to other
            else:
                graph_data['Other'][0] += mining_pool_hashrate
                graph_data['Other'][1] += mining_pool_percentage

        else:
            graph_data[mining_pool_display_url] = [mining_pool_hashrate, mining_pool_percentage]

    # Sort by hashrate %
    graph_data = {key: val for key, val in sorted(graph_data.items(), key=lambda ele: ele[1][1], reverse=True)}
    return graph_data


def get_hashrates_from_database(coin, week, solar_lat):
    coin_id = Coin.query.filter_by(name=coin).first().id
    filters = [PoolHashrate.coin_id == coin_id,
               PoolHashrate.week == week]
    if solar_lat == 1:
        filters.append(MiningLocation.above_mag_60 == False)
    if solar_lat == 2:
        filters.append(MiningLocation.above_mag_50 == False)
    if solar_lat == 3:
        filters.append(MiningLocation.above_mag_40 == False)
    return db.session.query(PoolHashrate, MiningLocation, MiningPool) \
        .join(MiningPool, PoolHashrate.mining_pool_id == MiningPool.id) \
        .join(MiningLocation, MiningPool.id == MiningLocation.mining_pool_id) \
        .filter(*filters) \
        .all()
