from flask import Flask
import requests
app = Flask(__name__)

@app.route("/")
def query():
    return requests.get('http://frontend.default.svc.cluster.local').text

if __name__ == "__main__":
    app.run(host='0.0.0.0')
