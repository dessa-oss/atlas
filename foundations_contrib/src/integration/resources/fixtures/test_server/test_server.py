from flask import Flask
import requests
app = Flask(__name__)

@app.route("/")
def hello():
    return 'Test Passed'

@app.route('/predict')
def predict():
    return 'get on predict'

@app.route('/evaluate')
def evaluate():
    return 'get on evaluate'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)