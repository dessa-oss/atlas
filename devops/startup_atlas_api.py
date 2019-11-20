from .docker.run_api_server import app

app.run(host='127.0.0.1', port=37722, debug=True)
