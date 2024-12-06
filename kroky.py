from flask import Flask, request
from kroky import Kroky

app = Flask(__name__)

def login(username, password):
    kroky = Kroky(username, password)
    return kroky

@app.route('/kroky', methods=['GET'])
def kroky_command():
    # Get username and password from query parameters
    username = request.args.get('username')
    password = request.args.get('password')
    pos = request.args.get('pos')

    kroky = login(username, password)
    return kroky.get_menu(pos)


@app.route('/select_meal', methods=['GET'])
def select_meal():
    username = request.args.get('username')
    password = request.args.get('password')
    menu = request.args.get('menu')

    kroky = login(username, password)
    return kroky.select_meal(menu)


@app.route('/user_info', methods=['GET'])
def user_info():
    username = request.args.get('username')
    password = request.args.get('password')

    kroky = login(username, password)
    return kroky.user_info()


@app.route('/change_password', methods=['GET'])
def change_password():
    username = request.args.get('username')
    password = request.args.get('password')

    kroky = login(username, password)
    return kroky.change_password(password, password)


if __name__ == '__main__':
    app.run(debug=True, port=5002)
