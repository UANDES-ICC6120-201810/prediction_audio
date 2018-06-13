import sys
import subprocess
import keyboard_statics
from requests import get
import json


def replace_symbols(code):
    for symbol in keyboard_statics.REPLACING_SYMBOLS:
        code = code.replace(symbol, keyboard_statics.REPLACING_SYMBOLS[symbol])
    return code


if __name__ == '__main__':
    SERVICE_STOP = sys.argv[1]
    token = ''
    services = []
    if SERVICE_STOP == 'PC164':
        token = keyboard_statics.PC164
        services = keyboard_statics.SERVICES_PC164
    elif SERVICE_STOP == 'PC1049':
        token = keyboard_statics.PC1049
        services = keyboard_statics.SERVICES_PC1049
    else:
        print ('No credentials for this stop.')
        exit()
    while True:
        print( 'Waiting for service code...')
        service = sys.stdin.readline().strip().lower()
        service = replace_symbols(service)
        if service in services:
            prediction_request = get(
                'http://proyectozapo.herokuapp.com/api/v1/estimation_of_buses',
                headers={'Authorization': token})
            response = json.loads(prediction_request.text)
            try:
                if response['error'] == 'Not Authorized':
                    print( 'Point Not Authorized')
                    continue
            except TypeError:
                print (response)
                for prediction in response:
                    if prediction['route'].lower() == service:
                        command = "python main.py '{}' '{}'".format(service, prediction['waiting_time'])
                        print (command)
                        subprocess.call(command, shell=True)
                        subprocess.call(['mpg123', ' Output/{}.mp3'.format(service)])
                        break

