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
    pc1049 = 'eyJhbGciOiJIUzI1NiJ9.eyJhY2Nlc3NfcG9pbnRfaWQiOjcsImV4cCI6MTUyODgyOTcwOH0.Jy25PkIiDkLjvDuCBoW0alXxZ1xO3qt_T7MOqJTiMKg'
    pc164 = 'eyJhbGciOiJIUzI1NiJ9.eyJhY2Nlc3NfcG9pbnRfaWQiOjgsImV4cCI6MTUyODgzODE2MX0.z6bvQ5K8wv2PtRXznMfFAETQzXl5Q3FJb_Zu_cVN2Q0'
    while True:
        service = sys.stdin.readline().strip()
        service = replace_symbols(service)
        if service in keyboard_statics.SERVICES:
            prediction_request = get(
                'http://proyectozapo.herokuapp.com/api/v1/estimation_of_buses',
                headers={
                    'Authorization': pc164})
            response = json.loads(prediction_request.text)
            for prediction in response:
                if prediction['route'].lower() == service:
                    command = "python main.py '{}' '{}'".format(service, prediction['waiting_time'])
                    print command
                    subprocess.call(command, shell=True)
                    break
