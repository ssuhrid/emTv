import pysftp
import time
from Tkinter import *
import tkFileDialog

def printTotals(transferred, toBeTransferred):
    global _L2
    percent = float(transferred)/toBeTransferred*10000
    percent = '%0.2f' % (percent/100),'%'
    _L2['text']=percent
    _root.update()

def transferFile(host,user,passwd,file):
    try:
        print 'start'
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None  # disable host key checking.
        cnopts.compression = True

        srv = pysftp.Connection(host, username=user, password=passwd,cnopts=cnopts,port=22)
        # srv.timeout(1)
        srv.chdir('ssuhrid/lan/data')

        # Get the directory and file listing
        # data = srv.listdir()
        # # Prints out the directories and files, line by line
        # for i in data:
        #     print i
        start = time.time()
        srv.put(file,callback=printTotals)
        end = time.time()
        transferTime = end-start
        print transferTime
        # Closes the connection
        srv.close()

    except Exception as exp:
        print(type(exp))    # the exception instance
        # print(exp.args)     # arguments stored in .args
        print(exp)          # __str__ allows args to be printed directly,

def openFile():
    global _filePath,_E1
    _filePath = tkFileDialog.askopenfilename()
    _E1.delete(0, END)
    _E1.insert(0, _filePath)

def fileIsValid():
    pass

def upload():
    global _filePath,_statusBar
    _statusBar.config(text="System Busy", bg="#cc0605", width=70)  # Status Red
    _root.update()
    if fileIsValid(_filePath):
        transferFile('raspberrypi3','pi','raspberry',_filePath)
    _statusBar.config(text="System Ready", bg="#308446", width=70)  # Status Red
    _root.update()

def init(master):
    global _filePath
    guiInit(master)
    _filePath=''

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


if __name__ == "__main__":
    _root = Tk()
    init(_root)
    _root.mainloop()
