# Prometheus BOT
Telegram bot for alerting prometheus 

## Configuring alert manager

```
- name: 'admins'
  webhook_configs:
  - send_resolved: True
    url: http://127.0.0.1:5000/alert
```

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