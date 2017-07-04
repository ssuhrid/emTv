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

    os.system('rm -rf current/*.*')

    control = open('current/control.txt','w')
    control.write('$')
    control.write('\n')
    control.write('s')
    control.close()

    os.system('rm -rf buffer/*.*')

    Popen('python pyScript.py',shell=True)
