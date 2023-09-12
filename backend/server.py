from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

from reader import FileHandler, Reader

app = Flask(__name__)
CORS(app)

handler = FileHandler()
reader = Reader()

@app.route("/")
@cross_origin(origin='*')
def hello_world():
    return "hello"


@app.route("/get-user")
@cross_origin(origin='*')
def get_user():
    req = request.args.get('uuid')
    user = handler.getUser(req)
    return jsonify(user)


@app.route("/scan")
@cross_origin(origin='*')
def scan():
    timeout = request.args.get('timeout')
    return str(reader.listen(timeout))

@app.route("/stop")
@cross_origin(origin='*')
def stop():
    return str(reader.stop())

    
@app.route("/score")
@cross_origin(origin='*')
def score():
    uuid = request.args.get('uuid')
    inc = request.args.get('inc')
    return jsonify(handler.score(uuid, inc))

@app.route("/pay", methods=['POST'])
@cross_origin(origin='*')
def pay():
    uuid = request.args.get('uuid')
    return jsonify(handler.pay(uuid))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, threaded=True)
