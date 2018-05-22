import re
import sys
import playsound
import audio_paths


def parse_service(text):
    find_path('service')
    for symbol in text:
        find_path(symbol)


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
        play_out_of_service_audio()

    elif less_than_regex.match(text):
        text = text.split()
        play_less_than_audio(int(text[2]))

    elif no_bus_regex.match(text):
        play_no_bus_audio()

    elif between_regex.match(text):
        text = text.split()
        play_between_audio(int(text[1]), int(text[3]))

    elif estimated_frecuency.match(text):
        text = text.split()
        play_frequency_audio(int(text[6]))


def play_out_of_service_audio():
    find_path('out_of_service')


def play_no_bus_audio():
    find_path('no_bus')


def play_between_audio(this, that):
    find_path('between')
    find_path(this)
    find_path('and')
    find_path(that)
    find_path('minutes')


def play_less_than_audio(number):
    find_path('less_than')
    find_path(number)
    find_path('minutes')


def play_frequency_audio(minutes):
    find_path('estimated_frequency')
    find_path(minutes)
    find_path('minutes')


def find_path(symbol):
    playsound.playsound(audio_paths.AUDIO_PATHS[symbol], True)


if __name__ == '__main__':
    SERVICE_TEXT = sys.argv[1]
    MESSAGE_TEXT = sys.argv[2]
    parse_service(SERVICE_TEXT)
    parse_message(MESSAGE_TEXT)
