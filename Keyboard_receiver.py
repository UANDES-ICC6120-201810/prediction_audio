import sys
import subprocess
import keyboard_statics


def replace_symbols(code):
    for symbol in keyboard_statics.REPLACING_SYMBOLS:
        code = code.replace(symbol, keyboard_statics.REPLACING_SYMBOLS[symbol])
    return code


while True:
    service = sys.stdin.readline().strip()
    service = replace_symbols(service)
    if service in keyboard_statics.SERVICES:
        print service
        subprocess.call(
            "python omxplayerMain.py '{}' 'Menos de 5 min'".format(service),
            shell=True)
