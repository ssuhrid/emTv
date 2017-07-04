import RPi.GPIO as GPIO
import os
from subprocess import *

def reset():
    GPIO.output(23, 0)

    os.system('sudo killall omxplayer.bin')
    os.system('sudo killall pqiv')
    # os.system('sudo killall python')

    os.system('rm -rf buffer/*.*')
    os.system('rm -rf current/*.*')

    control = open('current/control.txt', 'w')
    control.write('$')
    control.write('\n')
    control.write('s')
    control.write('\n')
    control.close()

    control = open('buffer/control.txt', 'w')
    control.write('$')
    control.write('\n')
    control.write('s')
    control.write('\n')
    control.close()

    os.system('sudo pkill -f pyScript.py')
    try:
        os.system('sudo rm pyScript.py')
    except:
        pass
    os.system('cp backup/pyScript.py pyScript.py')

    Popen('python pyScript.py',shell=True)

    GPIO.output(23, 1)
    GPIO.cleanup()

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.OUT, initial=1)
while True:
    try:
        input_state = GPIO.input(18)
        if not input_state:
            while not input_state:
                input_state = GPIO.input(18)
            reset()
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(23, GPIO.OUT, initial=1)
            continue
    except Exception as exp:
        pass

