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

sizes = ['Kb', 'Mb', 'Gb', 'Tb', 'Pb', 'Eb', 'Zb', 'Yb']
scales = ['K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y']


# Форматирование единиц измерения
def format_measure_unit(measure_unit: str, value: str) -> str:
    result = ''
    initial = 0
    splitted_measure_unit = measure_unit.strip(' ').split('|')

    if len(splitted_measure_unit) > 2:
        initial = int(splitted_measure_unit[2])

    unit = splitted_measure_unit[0]

    match unit:
        case 'kb':
            result += format_byte(value, initial)
        case 's':
            result += format_scale(value, initial)
        case 'f':
            result += format_float(value)
        case 'i':
            result += format_int(value)
        case _:
            result += format_int(value)

    if len(splitted_measure_unit) > 1:
        result += splitted_measure_unit[1]

    return result


def format_byte(value: str, initial: int = 0) -> str:
    float_value = float(value)
    size = sizes[initial]
    return f'{float_value} {size}'


def format_scale(value: str, initial: int = 0) -> str:
    float_value = float(value)
    scale = scales[initial]
    return f'{float_value} {scale}'


def format_int(value: str) -> str:
    return f'{int(float(value))}'


def format_float(value: str) -> str:
    return f'{round(float(value), 2):.10f}'


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
    bot.send_message(channel_id, f'*{name}*\n{format_measure_unit(measure_unit, value)}', parse_mode="MarkdownV2")


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
