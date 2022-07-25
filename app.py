from config import app
from hashrate_requester import pull_hashrates
from pool_requester import get_pool_data


# routes
@app.route('/')
def hello_world():  # put application's code here
    run_commands()
    return 'Hello World!'


# commands
def run_commands():
    pass
    pull_hashrates()
    get_pool_data()


if __name__ == '__main__':
    app.run()
