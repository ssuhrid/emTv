import os
from subprocess import *

control = open('current/control.txt','r')
c1 = control.readline()[0]
c2 = control.readline()[0]
datafile = control.readline()

os.system('unzip -P pass  -d current "current/%s"'%(datafile))
os.system('rm "current/%s"'%(datafile))

if os.path.isfile('current/pyScript.py'):

    os.system('sudo pkill -f pyScript.py')
    os.system('mv current/pyScript.py pyScript.py')

    control = open('current/control.txt','w')
    control.write('$')
    control.write('\n')
    control.write('s')
    control.close()

    # files = os.listdir('buffer')
    # for file in files:
    #     if not file == '':
    #         os.system('rm "buffer/%s"' % file)

    Popen('python pyScript.py',shell=True)
