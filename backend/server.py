from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

#from reader import Reader
from data_handler import DataHandler

app = Flask(__name__, static_folder='../dist/', static_url_path='/')
CORS(app)

dh = DataHandler()
rd = Reader()
rd = None

@app.route("/")
@cross_origin(origin='*')
def index():
    return app.send_static_file('index.html')

@app.route("/api/getuser")
@cross_origin(origin='*')
def get_user():
    req = request.args.get('uid')
    user = dh.get_user(req)
    return jsonify(user)

@app.route("/api/card")
@cross_origin(origin='*')
def scan():
    timeout = request.args.get('timeout')
    return str(rd.listen(timeout))

@app.route("/api/cardstop")
@cross_origin(origin='*')
def stop():
    return str(rd.stop())

@app.route("/api/updateuser", methods=["POST"])
@cross_origin(origin='*')
def update_user():
    uid = request.form.get('uid')
    data = request.form.get('data')
    return jsonify(dh.update_user(uid, data))

@app.route("/api/adduser", methods=['POST'])
@cross_origin(origin='*')
def add_user():
    uid = request.form.get('uid')
    data = request.form.get('data')
    return jsonify(dh.add_user(uid, data))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3080, threaded=True)
