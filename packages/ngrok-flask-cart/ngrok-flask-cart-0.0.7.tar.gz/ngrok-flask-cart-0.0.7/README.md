# flask-ngrok-CART
An offshoot of [flask-ngrok](https://github.com/gstaff/flask-ngrok) (see also [flask-ngrok2](https://github.com/MohamedAliRashad/flask-ngrok2), [flask-ngrok3](https://github.com/Partycode/flask-ngrok3)) for making demo Flask apps from a personal machine.

## Installation

```bash
pip install ngrok-flask-cart
```

- app is the Flask app 
- domain is the static domain provided by `ngrok` 
- auth_token is the authentication token provided by `ngrok` 



## Example

```
from flask import Flask
from ngrok_flask_cart import run_with_ngrok

app = Flask(__name__)
run_with_ngrok(app=app, domain='--domain=<domain here>', auth_token='<token here>')

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run()
```

### will run 

```
ngrok                                                           (Ctrl+C to quit)

Session Status                online                                            
Account                       <your account> (Plan: Free)                              
Version                       3.6.0                                             
Region                        United States (us)                                
Latency                       -                                                 
Web Interface                 http://127.0.0.1:4040                             
Forwarding                    <domain here> -> 
                                                                                
Connections                   ttl     opn     rt1     rt5     p50     p90       
                              0       0       0.00    0.00    0.00    0.00     * Running on http://<your domain>                       
 * Traffic stats available on http://127.0.0.1:4040
```

