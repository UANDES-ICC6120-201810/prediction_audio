# Speaker-Script

This script is in charge of translating the service prediction into an audio for passengers

## Getting Started

For this project you will need one not standard library.

### Prerequisites

Install playsound via pip

```
$ pip install playsound
```

## How to use

In console run the script as usual adding the service code and the prediction message

```
$ python main.py 'c02' 'Entre 03 y 05 min'
```
### Supported services

Any service matching the following regex

```
r'[a-l]*\d*'
```
Any message that matches the following regex
```
r'(\W|^)Fuera\sde\shorario\sde\soperacion\spara\seste\srecorrid(\W|$)'
r'(\W|^)Menos\sde\s\d{1,2}\s(min|minutos)(\W|$)'
r'(\W|^)No\shay\sbuses\sen\scamino(\W|$)'
r'(\W|^)Entre\s\d{1,2}\sy\s\d{1,2}\s(min|minutos)(\W|$)'
```

## TODO

* No validation for initial args
