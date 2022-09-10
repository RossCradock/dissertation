import json


def churn_between_weeks(week_a_filename, week_b_filename):
    week_a_file = open(week_a_filename, 'r')
    week_b_file = open(week_b_filename, 'r')
    json_week_a = json.loads(week_a_file.read())
    json_week_b = json.loads(week_b_file.read())

    week_a_set = set()
    week_b_set = set()

    # get nodes from json and add to sets
    for node in json_week_a:
        week_a_set.add(node)
    for node in json_week_b:
        week_b_set.add(node)

    week_a_size = len(week_a_set)
    week_b_size = len(week_b_set)
    lost = len(week_a_set - week_b_set)
    gained = len(week_b_set - week_a_set)
    print('week a size: ' + str(week_a_size))
    print('week b size: ' + str(week_b_size))
    print('amount lost: ' + str(lost))
    print('lost %: ' + str(lost / week_a_size))
    print('amount gained: ' + str(gained))
    print('gained %: ' + str(gained / week_b_size))


# change file names for different all.json files
churn_between_weeks('all_25_7.json', 'all_1_8.json')
