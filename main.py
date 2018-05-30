import re
import sys
import playsound
import audio_paths
import time
import subprocess


def parse_service(text):
    command_portion = '{}'.format(find_path('service'))
    for symbol in text:
        command_portion += '|' + find_path(symbol)
    return command_portion


def parse_message(text):
    out_of_service_regex = re.compile(
        r'(\W|^)Servicio\sfuera\sde\shorario\sde\soperacion\spara\seste\sparadero(\W|$)')
    less_than_regex = re.compile(
        r'(\W|^)Menos\sde\s\d{1,2}\s(min|minutos)(\W|$)')
    no_bus_regex = re.compile(
        r'(\W|^)No\shay\sbuses\sque\sse\sdirijan\sal\sparadero(\W|$)')
    between_regex = re.compile(
        r'(\W|^)Entre\s\d{1,2}\sy\s\d{1,2}\s(min|minutos)(\W|$)')
    estimated_frecuency = re.compile(
        r'(\W|^)Frecuencia\sestimada\ses\s1\sbus\scada\s\d{1,2}\s(min|minutos)(\W|$)')

    if out_of_service_regex.match(text):
        return play_out_of_service_audio()

    elif less_than_regex.match(text):
        text = text.split()
        return play_less_than_audio(int(text[2]))

    elif no_bus_regex.match(text):
        return play_no_bus_audio()

    elif between_regex.match(text):
        text = text.split()
        return play_between_audio(int(text[1]), int(text[3]))

    elif estimated_frecuency.match(text):
        text = text.split()
        return play_frequency_audio(int(text[6]))


def play_out_of_service_audio():
    return '{}'.format(find_path('out_of_service'))


def play_no_bus_audio():
    return '{}'.format(find_path('no_bus'))


def play_between_audio(this, that):
    return '{0}|{1}|{2}|{3}|{4}'.format(
        find_path('between'),
        find_path(this),
        find_path('and'),
        find_path(that),
        find_path('minutes'))


def play_less_than_audio(number):
    return '{0}|{1}|{2}'.format(
        find_path('less_than'),
        find_path(number),
        find_path('minutes'))


def play_frequency_audio(minutes):
    return '{0}|{1}|{2}'.format(
        find_path('estimated_frequency'),
        find_path(minutes),
        find_path('minutes'))


def find_path(symbol):
    return audio_paths.AUDIO_PATHS[symbol]


if __name__ == '__main__':
    audio_name = 'Output/{}.mp3'.format(str(int(time.time())))
    SERVICE_TEXT = sys.argv[1]
    MESSAGE_TEXT = sys.argv[2]
    command = 'ffmpeg -i "concat:{}|{}" -acodec copy {}'.format(
        parse_service(SERVICE_TEXT), parse_message(MESSAGE_TEXT), audio_name)
    subprocess.call(command, shell=True)
    subprocess.call('mpg123 {}'.format(audio_name))
