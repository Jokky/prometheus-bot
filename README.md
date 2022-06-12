# Prometheus BOT
Telegram bot for alerting prometheus 


## Install dependencies
```
$ pip install virtualenv 
$ virtualenv -p python3 venv
$ pip install -r requirements.txt
```

## Copy environment config
```
$ cp .env.example .env
```

## Run project in background
```
$ python main.py &
```

## Envs
| Env            | Description                        |
|----------------|------------------------------------|
| TELEGRAM_TOKEN | Telegram bot token                 |
| URL            | Prometheus url                     |
| CHANNEL_ID     | Telegram channel for send messages |
| INTERVAL       | Interval get alerts                |