from flask import Flask
import requests
app = Flask(__name__)

@app.route("/")
def query():
    try:
        message = requests.get('http://hello-server-service.default.svc.cluster.local', timeout=15).text
    except requests.ConnectTimeout:
        return 'CONNECTION TIMED OUT'
    except Exception as e:
        return e
    return message

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
