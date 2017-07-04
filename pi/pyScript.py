from subprocess import *
import os
import time
import RPi.GPIO as GPIO

def blink(sec):
    GPIO.output(23,0)
    time.sleep(sec)
    GPIO.output(23,1)
    time.sleep(sec)
def run(c1,c2,dataFile):

    if c2 == 'v':
        omxc = Popen(['omxplayer', '-b', '--no-osd', '--loop', 'current/%s' % (dataFile)])
        player = True
    if c2 == 'i':
        omxc = Popen(['sudo fbi -T 1 --autodown -noverbose -t 10 "current/%s"' % (dataFile)],shell=True)
        player = True
    if c2 == 'p':
        pass
    if c2 == 'z':
        if os.path.isfile('current/%s'%dataFile):
            os.system('unzip -o -d current "current/%s"' % (dataFile))
            os.system('rm -f "current/%s"'%dataFile)
        pqivx = Popen(['sudo fbi -T 1 --autodown -noverbose -t 10 `find current -iname \\*.jpg -o -iname \\*.png`'], shell=True)
        player = True
    if c2 == 'u':
        for i in range(0, 5):
            blink(2)
        GPIO.cleanup()
        Popen('python updateScript.py', shell=True)
def initiate():

    for i in range(0,5):
        blink(0.5)

    dataFile = ''
    try:
        control = open('current/control.txt', 'r')
        c1 = control.readline()[0]
        c2 = control.readline()[0]
        dataFile = control.readline()
        control.close()
    except Exception as exp:
        control = open('current/control.txt', 'w')
        control.write('$')
        control.write('\n')
        control.write('s')
        c1='$'
        c2='s'
        control.close()

    # Start the appropriate process on current file
    run(c1,c2,dataFile)

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    # GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(23,GPIO.OUT,initial=1)
    GPIO.output(23,1)
    initiate()
    prev = 0
    while True:

        if time.time()-prev > 5:
            blink(0.1)
            prev=time.time()

        try:
            # Read states of inputs

            if os.path.isfile('buffer/control.txt') :

                #Blink 10 times
                for i in range(0,10):
                    blink(0.1)

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
                        os.system('killall fbi')
                    except Exception as exp:
                        print exp

                    # Delete all current files
                    # files = os.listdir('current')
                    # for file in files:
                    #     if not file == 'control.txt':
                    #         if not file == '':
                    #             os.system('rm -rf "current/%s"' %(file))

                    os.system('rm -rf current/*.*')

                    # Move data,control files to current
                    if not dataFile == '':
                        os.system('mv "buffer/%s" "current/%s"' % (dataFile,dataFile))
                    os.system('mv buffer/control.txt current/control.txt')

                    # Start the appropriate process on current file
                    run(c1,c2,dataFile)

                    # Delete all files in buffer
                    # deleteAllBuffer()
                    os.system('rm -rf buffer/*.*')

                    # Blink 10 times
                    for i in range(0, 10):
                        blink(0.1)

        except Exception as exp:

            # blink(1)

            time.sleep(1)
