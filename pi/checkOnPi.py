from subprocess import *
import os
import time

while True:
    # Read states of inputs

    if os.path.isfile('buffer/control.txt'):

        file = open('buffer/control.txt', 'r')
        c1 = file.read(1)
        c2 = file.read(1)
        file.close()

        print c1
        print c2
        if c1 == '$':

            if c2=='v':
                os.system('killall omxplayer.bin')
            files = os.listdir('current')
            for file in files:
                os.system('rm current/%s' %(file))

            files = os.listdir('buffer')
            for file in files:
                if not file == 'control.txt':
                    dataFile = file
            os.system('mv buffer/%s current/%s' % (dataFile,dataFile))
            if c2=='v':
                omxc = Popen(['omxplayer', '-b', '--no-osd','--loop','current/%s'%(dataFile)])
                player = True
            os.system('mv buffer/control.txt current/control.txt')
            os.system('rm buffer/control.txt')

    time.sleep(1)



