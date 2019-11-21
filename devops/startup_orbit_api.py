from .docker.run_orbit_api_server import app

app.run(host='127.0.0.1', port=37222, debug=True)
