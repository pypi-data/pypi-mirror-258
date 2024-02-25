# flask-ngrok-CART
An offshoot of [flask-ngrok](https://github.com/gstaff/flask-ngrok) (see also [flask-ngrok2](https://github.com/MohamedAliRashad/flask-ngrok2), [flask-ngrok3](https://github.com/Partycode/flask-ngrok3)) for making demo Flask apps from a personal machine.

## Installation

```bash
pip install ngrok-flask-cart
...
from ngrok_flask_cart import run_with_ngrok
...
run_with_ngrok(app=app, domain='--domain=<YOUR_STATIC_DOMAIN>', auth_token='<YOUR_AUTH_TOKEN>')
```

- app is the Flask app 
- domain is the static domain provided by `ngrok` 
- auth_token is the authentication token provided by `ngrok` 



