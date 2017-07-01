from subprocess import *
import os
import time
import RPi.GPIO as GPIO

def reset():
    GPIO.output(18,0)
    os.system('sudo killall omxplayer.bin')
    os.system('sudo killall pqiv')
    # os.system('sudo killall python')

    deleteAllBuffer()
    deleteAllCurrent()

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

    GPIO.output(18,1)

def blink():
    GPIO.output(18,0)
    time.sleep(0.1)
    GPIO.output(18,1)
    time.sleep(0.1)

def deleteAllBuffer():
    # Delete all files in buffer
    files = os.listdir('buffer')
    for file in files:
        if not file == '':
            os.system('rm "buffer/%s"' % file)

def deleteAllCurrent():
    # Delete all files in buffer
    files = os.listdir('buffer')
    for file in files:
        if not file == '':
            os.system('rm "current/%s"' % file)


def initiate():

    input_state = GPIO.input(18)
    if not input_state:
        pass# reset()

    try:
        control = open('current/control.txt', 'r')
        c1 = control.readline()[0]
        c2 = control.readline()[0]
        dataFile = control.readline()
        control.close()
    except Exception as exp:
        control = open('current/control.txt', 'r')
        control.write('$')
        control.write('\n')
        control.write('s')
        c1='$'
        c2='s'
        control.close()

    # Start the appropriate process on current file
    if c2 == 'v':
        omxc = Popen(['omxplayer', '-b', '--no-osd', '--loop', 'current/%s' % (dataFile)])
        player = True
    if c2 == 'i':
        omxc = Popen(['pqiv', '-i', '--fullscreen', 'current/%s' % (dataFile)])
        # player = True
    if c2 == 'p':
        pass

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(23,GPIO.OUT)
# GPIO.output(23,1)
initiate()
while True:
    try:
        # Read states of inputs

        input_state = GPIO.input(18)
        if not input_state:
            pass #reset()

        if os.path.isfile('buffer/control.txt') :

            #Blink 10 times
            # for i in range(0,10):
            #     blink()

            # Read control file
            control = open('buffer/control.txt', 'r')
            c1 = control.readline()[0]
            c2 = control.readline()[0]
            dataFile = control.readline()
            control.close()
            print dataFile

            if c1 == '$':

                # Kill current process
                try:
                    os.system('killall omxplayer.bin')
                    os.system('killall pqiv')
                except Exception as exp:
                    print exp

                # Delete all current files
                files = os.listdir('current')
                for file in files:
                    if not file == 'control.txt':
                        if not file == '':
                            os.system('rm -rf "current/%s"' %(file))

                # Move data,control files to current
                if not dataFile == '':
                    os.system('mv "buffer/%s" "current/%s"' % (dataFile,dataFile))
                os.system('mv buffer/control.txt current/control.txt')

                # Start the appropriate process on current file
                if c2=='v':
                    omxc = Popen(['omxplayer', '-b', '--no-osd','--loop','current/%s'%(dataFile)])
                    player = True
                if c2=='p':
                    pass
                if c2=='i':
                    pqivx = Popen(['pqiv','-i','--fullscreen','current/%s'%(dataFile)])
                if c2=='u':
                    Popen('python updateScript.py',shell=True)
                    # Popen(['python','updateScript.py'])

                # Delete all files in buffer
                deleteAllBuffer()

    except Exception as exp:
        # GPIO.output(23, 0)

        time.sleep(1)
