import sys
import pysftp
import time

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None  # disable host key checking.
# cnopts.compression = True

try:
    srv = pysftp.Connection('192.168.1.4', username='pi', password='raspberry',cnopts=cnopts,port=22)
    srv.chdir('ssuhrid/lan/data')

    # Get the directory and file listing
    # data = srv.listdir()
    # # Prints out the directories and files, line by line
    # for i in data:
    #     print i
    start = time.time()
    srv.put('data/newfolder/video.mkv')
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