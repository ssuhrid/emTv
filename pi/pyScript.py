from subprocess import *
import os
import time
import RPi.GPIO as GPIO
import subprocess

def blink(sec):
    GPIO.output(23,0)
    time.sleep(sec)
    GPIO.output(23,1)
    time.sleep(sec)
def run(c1,c2,dataFile):

    global _player
    if c2 == 'v':
        omxc = Popen(['omxplayer', '-b', '--no-osd', '--loop', 'current/%s' % (dataFile)])
        _player = True
    if c2 == 'i':
        fbix = Popen(['sudo fbi -T 1 --autodown -noverbose -t 10 "current/%s"' % (dataFile)],shell=True)
        _player = True
    if c2 == 'p':
        pass
    if c2 == 'z':
        # if os.path.isfile('current/%s'%dataFile):
        os.system('unzip -o -d current "current/%s"' % (dataFile))

        # Remove spaces from filenames
        files = os.listdir('current')
        for imageFile in files:
            if not imageFile == '':
                if '.zip' in imageFile:
                    pass
                else:
                    nameWithoutSpace = imageFile.replace(' ','_')
                    os.system('mv -f "current/%s" "current/%s"' %(imageFile,nameWithoutSpace))
        pqivx = Popen(['sudo fbi -T 1 --autodown -noverbose -t 10 `find current -iname \\*.jpg -o -iname \\*.png`'], shell=True)
        _player = True
    if c2 == 'u':
        _player = False
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

    return c1, c2, dataFile

if __name__ == "__main__":
    global _player
    _player = False
    GPIO.setmode(GPIO.BCM)
    # GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(23,GPIO.OUT,initial=1)
    GPIO.output(23,1)
    c1,c2,dataFile = initiate()
    prev = 0
    while True:

        if time.time()-prev > 5:
            blink(0.1)
            prev=time.time()
            if _player == True:
                p1 = subprocess.Popen(['pgrep omxplayer'], stdout=subprocess.PIPE,shell=True)
                op1 = p1.communicate()[0]
                p2 = subprocess.Popen(['pgrep fbi'], stdout=subprocess.PIPE,shell=True)
                op2 = p2.communicate()[0]
                print 'op1'
                print op1
                print 'op2'
                print op2

                if op1 == '' and op2 == '':
                    print 'restart'
                    run(c1,c2,dataFile)
                    pass


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

                    _player = False
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
