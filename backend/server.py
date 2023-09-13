import os
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

from reader import Reader
from data_handler import DataHandler

app = Flask(__name__, static_folder='../dist/', static_url_path='/')
CORS(app)

dh = DataHandler()
rd = Reader()

@app.route("/")
@cross_origin(origin='*')
def index():
    return app.send_static_file('index.html')

@app.route("/api/user")
@cross_origin(origin='*')
def get_user():
    uid = request.args.get('uid')
    print(type(uid))
    user = dh.get_user(uid)
    if user["paid"] == "TRUE":
        user["paid"] = True
    else:
        user["paid"] = False
    user["score"] = int(user["score"])
    return jsonify(user)

@app.route("/api/card")
@cross_origin(origin='*')
def scan():
    timeout = request.args.get('timeout', 6)
    uid = str(rd.listen(timeout))
    stop()
    return uid

@app.route("/api/exists")
@cross_origin(origin='*')
def exists():
    uid = request.args.get('uid')
    exists = dh.exists(uid)
    if exists:
        return jsonify('true')
    return jsonify('false')

@app.route("/api/cardstop")
@cross_origin(origin='*')
def stop():
    return str(rd.stop())

@app.route("/api/redeploy")
@cross_origin(origin='*')
def redeploy():
    print("REDEPLOYING!")
    os.system("/bin/bash /home/pi/zkkscore/redeploy.sh")

@app.route("/api/updateuser", methods=["POST"])
@cross_origin(origin='*')
def update_user():
    uid = request.get_json().get('uid')
    data = request.get_json().get('data')
    return jsonify(dh.update_user(str(uid), data))

@app.route("/api/adduser", methods=['POST'])
@cross_origin(origin='*')
def add_user():
    uid = request.get_json().get('uid')
    data = request.get_json().get('data')
    return jsonify(dh.add_user(uid, data))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3080, threaded=True)
