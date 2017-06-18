from subprocess import *
import os
import time

while True:
    # Read states of inputs

    if os.path.isfile('buffer/control.txt'):

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
            except Exception as exp:
                print exp

            # Delete all current files
            files = os.listdir('current')
            for file in files:
                if not file == '':
                    os.system('rm -rf current/%s' %(file))

            # Move data,control files to current
            if not dataFile == '':
                os.system('mv buffer/%s current/%s' % (dataFile,dataFile))
            os.system('mv buffer/control.txt current/control.txt')

            # Start the appropriate process on current file
            if c2=='v':
                omxc = Popen(['omxplayer', '-b', '--no-osd','--loop','current/%s'%(dataFile)])
                player = True
            if c2=='p':
                pass

            # Delete all files in buffer
            files = os.listdir('buffer')
            for file in files:
                if not file == '':
                    os.system('rm buffer/%s' % (file))
    time.sleep(1)



from subprocess import *
import os
import time

while True:
    # Read states of inputs

    if os.path.isfile('buffer/control.txt'):

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
            except Exception as exp:
                print exp

            # Delete all current files
            files = os.listdir('current')
            for file in files:
                if not file == '':
                    os.system('rm -rf current/%s' %(file))

            # Move data,control files to current
            if not dataFile == '':
                os.system('mv buffer/%s current/%s' % (dataFile,dataFile))
            os.system('mv buffer/control.txt current/control.txt')

            # Start the appropriate process on current file
            if c2=='v':
                omxc = Popen(['omxplayer', '-b', '--no-osd','--loop','current/%s'%(dataFile)])
                player = True
            if c2=='p':
                pass

            # Delete all files in buffer
            files = os.listdir('buffer')
            for file in files:
                if not file == '':
                    os.system('rm buffer/%s' % (file))
    time.sleep(1)



