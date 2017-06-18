import pysftp
import time
from Tkinter import *
import tkFileDialog

def createControlFile(filePath):
    control = open('data/control.txt', 'w')
    control.write('$')
    control.write('\n')
    if filePath == 'STOP':
        control.write('s')
    else:
        if '.mkv' in filePath:
            control.write('v')
        if '.ppt' in filePath:
            control.write('p')
        f1=0
        for i in range(0,len(filePath)):
            c=filePath[len(filePath)-i-1]
            if c=='/':
                f1=len(filePath)-1-i
                break
        fileName=filePath[f1+1:len(filePath)]
        control.write('\n')
        control.write(fileName)
    control.close()
def fileIsValid(abc):
    return True
    pass
def transferFile(host,user,passwd,file):
    global _srv, _processRun

    try:
        print 'start'
        createControlFile(file)
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None  # disable host key checking.
        cnopts.compression = True

        _processRun = True
        _srv = pysftp.Connection('192.168.137.2', username=user, password=passwd,cnopts=cnopts,port=22)
        # srv.timeout(1)

        _srv.chdir('emTv/pi/buffer')

        start = time.time()
        if not file == 'STOP':
            _srv.put(file,callback=printTotals)
        _srv.put('data/control.txt',callback=printTotals)
        end = time.time()
        transferTime = end-start
        print transferTime
        # Closes the connection
        _srv.close()
        _processRun = False

    except Exception as exp:
        print(type(exp))    # the exception instance
        # print(exp.args)     # arguments stored in .args
        print(exp)          # __str__ allows args to be printed directly,

def openFile():
    global _filePath,_E1
    _filePath = tkFileDialog.askopenfilename()
    _E1.delete(0, END)
    _E1.insert(0, _filePath)
def closetv():
    global _statusBar
    _statusBar.config(text="System Busy", bg="#cc0605", width=70)  # Status Red
    _root.update()
    if fileIsValid(_filePath):
        transferFile('raspberrypi3', 'pi', 'raspberry', 'STOP')
    _statusBar.config(text="System Ready", bg="#308446", width=70)  # Status Red
    _root.update()
def upload():
    global _filePath,_statusBar
    _statusBar.config(text="System Busy", bg="#cc0605", width=70)  # Status Red
    _root.update()
    if fileIsValid(_filePath):
        transferFile('raspberrypi3','pi','raspberry',_filePath)
    _statusBar.config(text="System Ready", bg="#308446", width=70)  # Status Red
    _root.update()
def stop():
    global _processRun
    _processRun = False
    pass

def printTotals(transferred, toBeTransferred):
    global _L2, _processRun,_srv
    if _processRun == False:
        _srv.close();
    percent = float(transferred)/toBeTransferred*10000
    percent = '%0.2f' % (percent/100),'%'
    _L2['text']=percent
    _root.update()
def guiInit(master):
    global _E1,_L2,_statusBar
    row=0
    f0 = Frame(master)
    L1 = Label(f0, text="Input File:")
    L1.grid(row=0, column=1, padx=20, pady=40)
    _E1 = Entry(f0, bd=5, width=40)
    _E1.grid(row=0, column=2, sticky=E + W, columnspan=3, padx=0, pady=0)
    # _E1.config(state=DISABLED)
    openButton = Button(f0, text="Browse...", command=openFile, width=10)
    openButton.grid(row=0, column=5, padx=30)
    f0.grid(row=0)
    row+=1

    _statusBar = Label(f0, text="System Ready", bg="#308446", width=70, pady=5, fg="#ffffff")  # Status Green
    _statusBar.grid(row=1, column=0, columnspan=7, pady=0)

    f1 = Frame(master)
    f1.grid(row=row, padx=0, pady=30,sticky=W)
    lt1 = Label(f1, text="",padx=15)
    lt1.grid(row=0, column=0)
    uploadButton = Button(f1, text="Upload", command=upload, width=10)
    uploadButton.grid(row=0, column=1, padx=50)
    lt2 = Label(f1, text="",padx=25)
    lt2.grid(row=0, column=2)
    labelRead = Label(f1, text="Uploading..")
    labelRead.grid(row=0, column=3)
    _L2 = Label(f1, text="0.00%")
    _L2.grid(row=0, column=4, padx=15, pady=0)
    row+=1

    f2 = Frame(master)
    f2.grid(row=row, padx=0, pady=30,sticky=W)
    lt1 = Label(f2, text="",padx=15)
    lt1.grid(row=0, column=0)
    closeButton = Button(f2, text="Close TV", command=closetv, width=10)
    closeButton.grid(row=0, column=1, padx=50)
    lt2 = Label(f2, text="",padx=25)
    lt2.grid(row=0, column=2)
    stopButton = Button(f2, text="Stop", command=stop, width=10)
    stopButton.grid(row=0, column=2, padx=50)
    # _L2 = Label(f2, text="0.00%")
    # _L2.grid(row=0, column=4, padx=15, pady=0)

def init(master):
    global _filePath
    guiInit(master)
    _filePath=''
if __name__ == "__main__":
    _root = Tk()
    init(_root)
    _root.mainloop()