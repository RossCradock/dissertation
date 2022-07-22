from config import app
from hashrate_requester import pull_hashrates


# routes
@app.route('/')
def hello_world():  # put application's code here
    run_commands()
    return 'Hello World!'


# commands
def run_commands():
    pull_hashrates()


if __name__ == '__main__':
    app.run()
