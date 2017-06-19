import sys
import pysftp
import time


cnopts = pysftp.CnOpts()
cnopts.hostkeys = None  # disable host key checking.
# cnopts.compression = True

def printTotals(transferred, toBeTransferred):
    # print "Transferred: {0}\tOut of: {1}".format(transferred, toBeTransferred)
    percent = float(transferred)/toBeTransferred*100
    print '%0.1f' % (percent),'%'

try:

    pass
except Exception as exp:
    print (type(exp))
    print (exp)
    pass

try:
    srv = pysftp.Connection('raspberrypi3', username='pi', password='raspberry',cnopts=cnopts,port=22)
    # src.timeout(1)
    srv.chdir('ssuhrid/lan/data')

    # Get the directory and file listing
    # data = src.listdir()
    # # Prints out the directories and files, line by line
    # for i in data:
    #     print i
    start = time.time()
    print 'start'
    srv.put('data/video.mkv',callback=printTotals)

    end = time.time()

    transferTime = end-start
    print transferTime
    # Closes the connection
    srv.close()

except Exception as inst:
    print(type(inst))    # the exception instance
    # print(inst.args)     # arguments stored in .args
    print(inst)          # __str__ allows args to be printed directly,
                         # but may be overridden in exception subclasses
    # x, y = inst.args     # unpack args
    # print('x =', x)
    # print('y =', y)
    # if ''

def toggle_geom(self,event):
    geom=self.master.winfo_geometry()
    print(geom,self._geom)
    self.master.geometry(self._geom)
    self._geom=geom
