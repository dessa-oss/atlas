<h1>Authentication</h1>
---

Atlas utilizes an authentication proxy and [Keycloak](https://www.keycloak.org/) to enable user access and management within the system.

All you need to do is run `atlas-server start -p` and you're ready to go.

###How to launch jobs in an authenticated world

Firstly, you will need to login using the [foundations login](https://www.docs.atlas.dessa.com/en/latest/cli/#foundations-login) command. Once you are logged in through the CLI, you can submit any job the way that you normally would (e.g. [foundations submit](https://www.docs.atlas.dessa.com/en/latest/cli/#foundations-clear-queue) and [foundations.submit()](https://www.docs.atlas.dessa.com/en/latest/sdk-reference/SDK/#job-submission)).

!!! note "Configuration"
    For the configuration file used by `foundations submit` and `<host>` in `foundations login <host>`, you need to use the address and port of the authentication proxy.

_Example:_

 1. `atlas-server start -p`
 2. `foundations login http://0.0.0.0:5558` (Username: test, Password: test)
 3. Create a config file under `~/.foundations/config/submission` called `atlas.config.yaml` with `scheduler_url: http://0.0.0.0:5558`
 4. `foundations submit atlas . main.py`
 5. Open the [Atlas UI](http://0.0.0.0:5555) (Username: test, Password: test)

###How to manage accounts?

Since Atlas uses Keycloak, you can use their [documentation](https://www.keycloak.org/docs/latest/server_admin/index.html#overview) for information on how to use the Keycloak Console. The console itself will be located at `https://<machine_address>:8443`.

Atlas comes with 2 default accounts that should be changed after testing is done.

**Keycloak admin account** (used only for accessing the Keycloak admin console):

Username: `admin`

Password: `admin`

**Atlas test account** (used to log into Atlas from the terminal and Atlas Dashboard):

Username: `test`

Password: `test`

**Useful first steps**:

1. Login to Keycloak via the admin console: `https://<machine_address>:8443`

2. Change the admin password using the Keycloak console ("Master" realm > Users > View all users > Edit)

3. Update the token lifespan to something reasonable for your organization ("Atlas" realm > Realm Settings > Tokens > Access Token Lifespan)

4. Provision Atlas users ("Atlas" realm > Users > View all users)