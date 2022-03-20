from flask import Flask
from flask import request

app = Flask(__name__)


# the minimal Flask application
@app.route('/')
def index():
    return '<h1>Hello, World!</h1>'


# bind multiple URL for one view function
@app.route('/hi')
@app.route('/hello')
def say_hello():
    return '<h1>Hello, Flask!</h1>'


# dynamic route, URL variable default
@app.route('/greet', defaults={'name': 'Programmer'})
@app.route('/greet/<name>')
def greet(name):
    ret_json = '{ "name": "' + name + '"}'
    print(ret_json)
    return ret_json

@app.route('/my_resource', methods=['POST', 'PUT'])
def post_example():
    inputs = request.args.get('res_name')
    print(inputs)
    return('You passed in res_name = ' + inputs)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)
