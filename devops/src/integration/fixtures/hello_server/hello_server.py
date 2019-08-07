from flask import Flask
import requests
app = Flask(__name__)

@app.route("/")
def Hello():
    return 'Test Passed'

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)