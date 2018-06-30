from requests import get
import json
import sys
import subprocess
import keyboard_statics


def replace_symbols(code):
    for symbol in keyboard_statics.REPLACING_SYMBOLS:
        code = code.replace(symbol, keyboard_statics.REPLACING_SYMBOLS[symbol])
    return code


def process_request(domain, service):
    prediction_request = get(
        '{}/api/v1/estimation_of_buses/{}'.format(domain, service),
        headers={'Authorization': token})
    response = json.loads(prediction_request.text)
    try:
        if response['error'] == 'Not Authorized':
            print('Point Not Authorized')
    except TypeError:
        print (response)
        for prediction in response:
            if prediction['route'].lower() == service:
                command = "python main.py '{}' '{}'".format(
                    service, prediction['waiting_time'])
                print (command)
                subprocess.call(command, shell=True)
                subprocess.call(
                    ['mpg123', ' Output/{}.mp3'.format(service)])
                break


def easter_egger():
    subprocess.call(
        ['mpg123', ' Audio/Gandalf.mp3'])


if __name__ == '__main__':
    domain = keyboard_statics.DOMAIN
    token = keyboard_statics.SERVICES['token']
    services = keyboard_statics.SERVICES['services']
    if services is None:
        print('No credentials for this stop.')
        exit()
    while True:
        print('Waiting for service code...')
        service = sys.stdin.readline().strip().lower()
        service = replace_symbols(service)
        if service in services:
            process_request(domain, service)
        elif service == '8000':
            easter_egger()
