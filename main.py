import os
import json
import time

import schedule

import telebot

from dotenv import load_dotenv
import urllib3

load_dotenv()

url = os.environ['URL']
telegramToken = os.environ['TELEGRAM_TOKEN']
interval = int(os.environ['INTERVAL'])
channel_id = os.environ['CHANNEL_ID']
http = urllib3.PoolManager()

bot = telebot.TeleBot(telegramToken)


# Получение алертов из Prometheus
def get_alerts():
    try:
        response = http.request(
            'GET',
            f'{url}/api/v1/alerts'
        )
        body = json.loads(response.data)

        if body['status'] == 'success':
            return []

        return body['data']['alerts']
    except:
        return []


def send_message(name: str, value: str, measure_unit: str = ''):
    bot.send_message(channel_id, f'*{name}*\n{value} {measure_unit}', parse_mode="MarkdownV2")


def watch_alerts():
    alerts = get_alerts()

    for alert in alerts:
        annotation = alert['annotations']
        starts_at = alert['startsAt']
        name = annotation['name']
        value = annotation['value']
        measure_unit = ''

        if annotation['measureUnit']:
            measure_unit = annotation['measureUnit']

        send_message(name, value, measure_unit)


def main():
    # Запускаем каждые N секунд получение алертов и отправляем сообщение
    schedule.every(interval).seconds.do(watch_alerts)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
