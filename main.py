from requests import get
from evdev import InputDevice, categorize, ecodes
import json
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
                command = "python audio.py '{}' '{}'".format(
                    service, prediction['waiting_time'])
                print (command)
                subprocess.call(command, shell=True)
                subprocess.call(
                    ['mpg123', ' Output/{}.mp3'.format(service)])
                break


def easter_egger():
    subprocess.call(
        ['mpg123', ' Audio/Gandalf.mp3'])


def process_keyboard_entry(service, services):
    if service in services:
        process_request(domain, service)
    elif service == '8000':
        easter_egger()


def run_with_keyboard(keyboard, keyboard_mapping, services, callback):
    input_text = ''

    for event in keyboard.read_loop():
        if event.type != ecodes.EV_KEY:
            continue

        key_event = categorize(event)

        if key_event.keystate != ecodes.KEY_UP:
            continue

        pressed_key = keyboard_mapping[key_event.scancode]

        if pressed_key == 'ENTER_KEY':
            callback(input_text, services)
            input_text = ''
        else:
            input_text += pressed_key


if __name__ == '__main__':
    domain = keyboard_statics.DOMAIN
    token = keyboard_statics.SERVICES['token']
    services = keyboard_statics.SERVICES['services']
    keyboard_mapping = keyboard_statics.KEYBOARD_MAPPING
    keyboard = InputDevice('/dev/input/event0')

    if services is None:
        print('No credentials for this stop.')
        exit()

    run_with_keyboard(keyboard, keyboard_mapping, services, process_keyboard_entry)
