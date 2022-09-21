from models import PoolHashrate, MiningLocation, MiningPool, SubLocation
from config import db


def get_table_figures():
    '''
    # solar
    mag_40_hashrate = get_solar_hashrate(40)
    mag_45_hashrate = get_solar_hashrate(45)
    mag_50_hashrate = get_solar_hashrate(50)
    mag_60_hashrate = get_solar_hashrate(60)
    average_hashrate_for_coin = get_average_hashrate()
    print(f"Average hashrate: {average_hashrate_for_coin}")
    print(f"Mag 40 hashrate: {mag_40_hashrate}")
    print(f"Mag 40 hashrate: {mag_45_hashrate}")
    print(f"Mag 50 hashrate: {mag_50_hashrate}")
    print(f"Mag 60 hashrate: {mag_60_hashrate}")

    # country
    get_largest_pool_with_missing_country()
'''

    # provider
    run_provider_analysis()


def get_average_hashrate():
    pool_hashrates = PoolHashrate.query.filter(
        PoolHashrate.coin_id == 1,
        PoolHashrate.week != 30).all()
    total_hashrate = 0
    for hashrate in pool_hashrates:
        total_hashrate += float(hashrate.hashrate)

    return total_hashrate / 5


def get_solar_hashrate(solar_lat):
    mining_filters = [PoolHashrate.coin_id == 1, PoolHashrate.week != 30]
    sub_location_filters = []
    if solar_lat == 60:
        mining_filters.append(MiningLocation.above_mag_60 == False)
        sub_location_filters.append(SubLocation.above_mag_60 == False)
    if solar_lat == 50:
        mining_filters.append(MiningLocation.above_mag_50 == False)
        sub_location_filters.append(SubLocation.above_mag_50 == False)
    if solar_lat == 40:
        mining_filters.append(MiningLocation.above_mag_40 == False)
        sub_location_filters.append(SubLocation.above_mag_40 == False)
    if solar_lat == 45:
        mining_filters.append(MiningLocation.above_mag_45 == False)
        sub_location_filters.append(SubLocation.above_mag_45 == False)

    query = db.session.query(PoolHashrate, MiningLocation, MiningPool) \
        .join(MiningPool, PoolHashrate.mining_pool_id == MiningPool.id) \
        .join(MiningLocation, MiningPool.id == MiningLocation.mining_pool_id) \
        .filter(*mining_filters) \
        .all()

    print('\n\n***********solar lat: ' + str(solar_lat))
    print('query length: ', len(query))

    leftover_mining_pools = {}
    total_hashrate = 0
    for row in query:
        if row[1].country == 'sub_locations':
            total_sub_locations = len(SubLocation.query.filter(SubLocation.mining_location_id == row[1].id).all())
            sub_location_filters_for_loop = sub_location_filters.copy()
            sub_location_filters_for_loop.append(SubLocation.mining_location_id == row[1].id)
            sub_locations_unaffected = len(SubLocation.query.filter(*sub_location_filters_for_loop).all())

            averaged_mining_pool_hashrate = float(
                row[0].hashrate) * (sub_locations_unaffected / total_sub_locations) / 5

            total_hashrate += averaged_mining_pool_hashrate
            if row[2].url in leftover_mining_pools:
                leftover_mining_pools[row[2].url] += averaged_mining_pool_hashrate
            else:
                leftover_mining_pools[row[2].url] = averaged_mining_pool_hashrate
        else:
            averaged_mining_pool_hashrate = float(row[0].hashrate) / 5
            total_hashrate += averaged_mining_pool_hashrate
            if row[2].url in leftover_mining_pools:
                leftover_mining_pools[row[2].url] += averaged_mining_pool_hashrate
            else:
                leftover_mining_pools[row[2].url] = averaged_mining_pool_hashrate

    print('leftover mining pools: ', '(', len(leftover_mining_pools), ') ', leftover_mining_pools)
    # sort by largest hashrate
    sorted_leftover_mining_pools = dict(sorted(leftover_mining_pools.items(), key=lambda x: x[1]))
    # largest divided by the rest
    largest_hashrate = sorted_leftover_mining_pools.popitem()
    print('largest mining pool: ', largest_hashrate)
    print('total hashrate: ', total_hashrate)
    print('largest % share: ', largest_hashrate[1] / total_hashrate)
    accumulated_hashrate = largest_hashrate[1]
    for i in range(0, 10):
        next_largest_mining_pool = sorted_leftover_mining_pools.popitem()
        print('next largest mining pool: ', next_largest_mining_pool)
        accumulated_hashrate += next_largest_mining_pool[1]
        largest_share = accumulated_hashrate / total_hashrate
        print('largest % share: ', largest_share)
        if largest_share > 0.5:
            print('number needed to collude: ', i + 2)
            break

    return total_hashrate


def get_missing_country_hashrate():
    query = db.session.query(PoolHashrate, MiningLocation, MiningPool) \
        .join(MiningPool, PoolHashrate.mining_pool_id == MiningPool.id) \
        .join(MiningLocation, MiningPool.id == MiningLocation.mining_pool_id) \
        .filter(PoolHashrate.coin_id == 1, PoolHashrate.week != 30) \
        .all()
    country_hashrate = {}
    for row in query:
        if row[1].country == 'sub_locations':
            sub_locations = SubLocation.query.filter(SubLocation.mining_location_id == row[1].id).all()
            number_of_sub_locations = len(sub_locations)
            for sub_location in sub_locations:
                if sub_location.country in country_hashrate:
                    country_hashrate[sub_location.country] += \
                        float(row[0].hashrate) / (number_of_sub_locations * 5)
                else:
                    country_hashrate[sub_location.country] = \
                        float(row[0].hashrate) / (number_of_sub_locations * 5)
        else:
            if row[1].country in country_hashrate:
                country_hashrate[row[1].country] += float(row[0].hashrate) / 5
            else:
                country_hashrate[row[1].country] = float(row[0].hashrate) / 5

    # sort by largest hashrate
    sorted_country_hashrate = dict(sorted(country_hashrate.items(), key=lambda x: x[1]))
    # remove largest
    removed_country = sorted_country_hashrate.popitem()
    remaining_hashrate = 0
    for hashrate in sorted_country_hashrate.values():
        remaining_hashrate += hashrate

    print('sorted countries dict: ', sorted_country_hashrate)
    print('missing country: ', removed_country[0])
    print('hashrate of missing country: ', removed_country[1] / 5)
    print('remaining hashrate: ', remaining_hashrate / 5)

    return [((remaining_hashrate / 5) + removed_country[1] / 5), removed_country]


def get_largest_pool_with_missing_country():
    removed_country, total_hashrate_after_removed = get_missing_country_hashrate()[1]
    query = db.session.query(PoolHashrate, MiningLocation, MiningPool) \
        .join(MiningPool, PoolHashrate.mining_pool_id == MiningPool.id) \
        .join(MiningLocation, MiningPool.id == MiningLocation.mining_pool_id) \
        .filter(
            PoolHashrate.coin_id == 1,
            PoolHashrate.week != 30,
            MiningLocation.country != removed_country,
            MiningLocation.country != 'Singapore') \
        .all()

    mining_pool_hashrate = {}
    for row in query:
        if row[1].country == 'sub_locations':
            sub_locations = SubLocation.query.filter(SubLocation.mining_location_id == row[1].id).all()
            number_of_sub_locations = len(sub_locations)
            for sub_location in sub_locations:
                if sub_location.country == removed_country or sub_location.country == 'Singapore':
                    continue
                else:
                    if row[2].url in mining_pool_hashrate:
                        mining_pool_hashrate[row[2].url] += float(row[0].hashrate) / (number_of_sub_locations * 5)
                    else:
                        mining_pool_hashrate[row[2].url] = float(row[0].hashrate) / (number_of_sub_locations * 5)
        else:
            if row[2].url in mining_pool_hashrate:
                mining_pool_hashrate[row[2].url] += float(row[0].hashrate) / 5
            else:
                mining_pool_hashrate[row[2].url] = float(row[0].hashrate) / 5

    # sort by largest hashrate
    sorted_mining_pool_hashrate = sorted(mining_pool_hashrate.items(), key=lambda x: x[1], reverse=True)
    print('sorted mining pool dict: ', sorted_mining_pool_hashrate)
    # find largest percentage of total
    print('total hashrate: ' + str(total_hashrate_after_removed))
    print('largest % share: ' + str(sorted_mining_pool_hashrate[0][1] / total_hashrate_after_removed))
    return sorted_mining_pool_hashrate[0][1] / float(total_hashrate_after_removed)


def run_provider_analysis():
    query = db.session.query(PoolHashrate, MiningLocation, MiningPool) \
        .join(MiningPool, PoolHashrate.mining_pool_id == MiningPool.id) \
        .join(MiningLocation, MiningPool.id == MiningLocation.mining_pool_id) \
        .filter(
        PoolHashrate.coin_id == 1,
        PoolHashrate.week != 30) \
        .all()
    # get hashrates per provider
    provider_hashrate = {}
    for row in query:
        if row[1].country == 'sub_locations':
            sub_locations = SubLocation.query.filter(SubLocation.mining_location_id == row[1].id).all()

            number_of_sub_locations = len(sub_locations)
            for sub_location in sub_locations:
                if sub_location.provider is None:
                    provider = row[1].provider
                else:
                    provider = sub_location.provider

                if provider in provider_hashrate:
                    provider_hashrate[provider] += float(row[0].hashrate) / (number_of_sub_locations * 5)
                else:
                    provider_hashrate[provider] = float(row[0].hashrate) / (number_of_sub_locations * 5)
        else:
            if row[1].provider in provider_hashrate:
                provider_hashrate[row[1].provider] += float(row[0].hashrate) / 5
            else:
                provider_hashrate[row[1].provider] = float(row[0].hashrate) / 5

    # sort by largest hashrate
    sorted_provider_hashrate = dict(sorted(provider_hashrate.items(), key=lambda x: x[1]))
    print('sorted providers dict: ', sorted_provider_hashrate)
    # remove largest
    removed_provider = sorted_provider_hashrate.popitem()
    remaining_hashrate = 0
    for hashrate in sorted_provider_hashrate.values():
        remaining_hashrate += hashrate

    print('sorted providers dict: ', sorted_provider_hashrate)
    print('missing provider: ', removed_provider[0])

    # get mining pools for after removing top 3 providers
    get_mining_pools_after_removing_top_providers(query, removed_provider[0])


def get_mining_pools_after_removing_top_providers(query, removed_provider):
    mining_pool_hashrate = {}
    removed_provider = [removed_provider, 'OVH', 'Amazon']
    for row in query:
        if row[1].country == 'sub_locations':
            sub_locations = SubLocation.query.filter(SubLocation.mining_location_id == row[1].id).all()
            number_of_sub_locations = len(sub_locations)
            for sub_location in sub_locations:
                if sub_location.provider is None:
                    provider = row[1].provider
                else:
                    provider = sub_location.provider

                if provider in removed_provider:
                    print('removed_provider')
                    continue
                else:
                    if row[2].url in mining_pool_hashrate:
                        mining_pool_hashrate[row[2].url] += float(row[0].hashrate) / (number_of_sub_locations * 5)
                    else:
                        mining_pool_hashrate[row[2].url] = float(row[0].hashrate) / (number_of_sub_locations * 5)
        else:
            if row[1].provider in removed_provider:
                print('removed_provider')
                continue
            if row[2].url in mining_pool_hashrate:
                mining_pool_hashrate[row[2].url] += float(row[0].hashrate) / 5
            else:
                mining_pool_hashrate[row[2].url] = float(row[0].hashrate) / 5

    # find total remaining hashrate
    remaining_hashrate = 0
    for hashrate in mining_pool_hashrate.values():
        remaining_hashrate += hashrate

    # sort by largest hashrate
    sorted_mining_pool_hashrate = sorted(mining_pool_hashrate.items(), key=lambda x: x[1], reverse=True)
    print('sorted mining pool dict: ', sorted_mining_pool_hashrate)

    # find largest percentage of total
    print('remaining hashrate: ' + str(remaining_hashrate))
    print('largest % share: ' + str(sorted_mining_pool_hashrate[0][1] / remaining_hashrate))
    return






get_table_figures()
