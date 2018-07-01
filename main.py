import json
import subprocess
from requests import get
from evdev import InputDevice, categorize, ecodes
import keyboard_statics


def process_request(domain, service):
    prediction_request = get(
        '{}/api/v1/estimation_of_buses/{}'.format(domain, service),
        headers={'Authorization': TOKEN})
    response = json.loads(prediction_request.text)
    print(response)
    if 'error' in response:
        if response['error'] == 'Not Authorized':
            print('Point Not Authorized')
    elif 'result' in response:
        print('Service not assigned to this stop')
        not_assigned()
    else:
        for prediction in response:
            print (prediction, service)
            if prediction['route'] == service:
                command = "python3 audio.py '{}' '{}'".format(
                    service, prediction['waiting_time'])
                print (command)
                subprocess.call(command, shell=True)
                subprocess.call(
                    ['mpg123', 'Output/{}.mp3'.format(service)])
                break


def easter_egger():
    subprocess.call(
        ['mpg123', 'Audio/Gandalf.mp3'])


def not_assigned():
    subprocess.call(
        ['mpg123', 'Audio/not-corresponding.mp3'])


def fetching():
    subprocess.call(
        ['mpg123', 'Audio/fetching.mp3'])


def process_keyboard_entry(service, services):
    if service in services:
        fetching()
        process_request(DOMAIN, service)
    elif service == '8000':
        easter_egger()


def run_with_keyboard(keyboard, keyboard_mapping, services, callback):
    input_text = ''

    for event in keyboard.read_loop():
        if event.type != ecodes.EV_KEY:
            continue

        key_event = categorize(event)

        if key_event.keystate != 0:
            continue

        pressed_key = keyboard_mapping[key_event.scancode]

        if pressed_key == 'ENTER_KEY':
            callback(input_text, services)
            input_text = ''
        else:
            input_text += pressed_key


if __name__ == '__main__':
    DOMAIN = keyboard_statics.DOMAIN
    TOKEN = keyboard_statics.SERVICES['token']
    SERVICES = keyboard_statics.SERVICES['services']
    KEYBOARD_MAPPING = keyboard_statics.KEYBOARD_MAPPING
    KEYBOARD = InputDevice('/dev/input/event0')

    if SERVICES is None:
        print('No credentials for this stop.')
        exit()

    run_with_keyboard(KEYBOARD, KEYBOARD_MAPPING, SERVICES,
                      process_keyboard_entry)
