# easee-fjordkraft
Python script for sending fjordkraft spot price to easee charger.


## Installation

First clone this repository, and setup your .env file.

```
git clone git@github.com:JoakimLien/easee-fjordkraft.git
cp .env.example .env
```

Login to Easee Cloud to access the bearer token

```

https://easee.cloud/external/login-devportal?redirect=%2Freference%2Fpost_api-accounts-login
```

Install the required python libraries

```
pip3 install requests
pip3 install moment
pip3 install dotenv
```

Run the main.py file

```
python3 main.py
```
