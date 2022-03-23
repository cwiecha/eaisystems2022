from flask import Flask
from flask import request
from flask import Response
from flask import abort

app = Flask(__name__)


# the minimal Flask application
@app.route('/')
def index():
    return Response( '<h1>Hello, World!</h1>', status=201 )


# bind multiple URL for one view function
@app.route('/hi')
@app.route('/hello')
def say_hello():
    return Response('<h1>Hello, Flask!</h1>', status=201)


# dynamic route, URL variable default
@app.route('/greet', defaults={'name': 'Programmer'})
@app.route('/greet/<name>')
def greet(name):
    ret = 'Hello ' + name
    print(ret)
    return Response(ret, status=201)

@app.route('/my_resource', methods=['POST', 'PUT'])
def post_example():
    inputs = request.args.get('res_name')
    print(inputs)
    if ( inputs != 'credit'):
        abort(404)
        return("quitting")
    else:
        return Response('You passed in res_name = ' + inputs, status=201 )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)
