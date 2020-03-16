## Some Notes
# Start the Auth Server
To start the server, simply execute the `launch.sh` script.

# Configure the Auth Server
To reconfigure the auth server, use the launch script then go to 
localhost:8080/auth and login with `user: admin` `pass: admin`. Make the 
necessary changes and then use the export script to write these changes to the
`keycloak/atlas.json` file which get consumed when launching a server.