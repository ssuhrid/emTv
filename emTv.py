import pysftp
import time
from Tkinter import *
import tkFileDialog
from src.About import *
from src.Preferences import *
import _cffi_backend
from PIL import ImageTk, Image
import logging
import webbrowser
import subprocess
import ttk

logging.basicConfig()
def init(master):
    global _filePath
    guiInit(master)
    _filePath=''


def getFileNameFromFilepath(filePath):
    f1 = 0
    for i in range(0, len(filePath)):
        c = filePath[len(filePath) - i - 1]
        if c == '/':
            f1 = len(filePath) - 1 - i
            break
    fileName = filePath[f1 + 1:len(filePath)]
    return fileName
def createControlFile(filePath):
    control = open('data/control.txt', 'w')
    control.write('$')
    control.write('\n')
    if filePath == 'STOP':
        control.write('s')
    else:
        ext = filePath[-4:]
        if '.mkv'==ext or '.avi'==ext \
                or '.mov'==ext or '.mp4'==ext :
            control.write('v')
        # elif '.ppt'==ext :
        #     control.write('p')
        elif '.png'==ext or '.jpg'==ext \
                or '.jpeg'==ext or '.bmp'==ext :
            control.write('i')
        elif '.emc'==ext :
            control.write('u')
        elif '.zip'==ext :
            control.write('z')
        else:
            control.close()
            return False

        fileName = getFileNameFromFilepath(filePath)
        control.write('\n')
        control.write(fileName)
    control.close()
    return True
def fileIsValid(abc):
    return True
    pass
def transferFile(host,user,passwd,file):
    global _srv, _processRun,_L2,_host,_progressBar

    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None  # disable host key checking.
    cnopts.compression = True

    _L2['text'] = 'Progress: 00.00%'
    _progressBar["value"] = 0
    _root.update()
    print 'check'

    try:
        print 'start'
        if not createControlFile(file):
            raise Exception('File Not Valid')

        _processRun = True
        _srv = pysftp.Connection(host, username=user, password=passwd,cnopts=cnopts,port=22)
        # _srv.timeout(1)

        # print _srv
        _srv.chdir('emTv/pi/buffer')

        start = time.time()
        if not file == 'STOP':
            _srv.put(file,callback=printTotals)
        _srv.put('data/control.txt',callback=printTotals)
        end = time.time()
        transferTime = end-start
        print transferTime
        printMsg('File upload successful.')
        # Closes the connection
        _srv.close()
        _processRun = False

    except Exception as exp:
        string = str(type(exp))    # the exception instance
        # print string
        if string == '<class \'pysftp.exceptions.ConnectionException\'>':
            printMsg('Unable to establish connection')
        elif string == '<class \'paramiko.ssh_exception.SSHException\'>':
            printMsg('Server connection dropped')
        elif exp == 'File Not Valid':
            printMsg('File Not Valid')
        # print(exp.args)     # arguments stored in .args
        else:
            printMsg(exp)          # __str__ allows args to be printed directly,
        # pass
def printMsg(msg):
    global _text
    _text.insert(END, msg)
    _text.insert(END, '\n')
    _text.see(END)
def printTotals(transferred, toBeTransferred):
    global _L2, _processRun,_srv,_progressBar
    if _processRun == False:
        _srv.close();
    percent = float(transferred)/toBeTransferred*10000
    progress = int(percent/100)
    percent = 'Progress: %0.2f%s' % (percent/100,'%')
    _L2['text']=percent
    # print int(percent)
    _progressBar["value"] = progress
    # self.frame.update()
    _root.update()
def readPreference():

    pass

def openFile():
    global _filePath,_E1
    _filePath = tkFileDialog.askopenfilename()
    _E1.delete(0, END)
    _E1.insert(0, _filePath)
def closetv():
    global _statusBar, _processRun,_srv,_host,_username,_password
    _processRun = False
    _statusBar.config(text="System Busy", bg="#cc0605", width=75)  # Status Red
    _root.update()
    if fileIsValid(_filePath):
        printMsg('Closing Tv ...')
        transferFile(_host, _username, _password, 'STOP')
    _statusBar.config(text="System Ready", bg="#308446", width=75)  # Status Red
    _root.update()
def upload():
    global _filePath,_statusBar,_host,_username,_password
    _statusBar.config(text="System Busy", bg="#cc0605", width=75)  # Status Red
    _root.update()
    if fileIsValid(_filePath):
        fileName = getFileNameFromFilepath(_filePath)
        if not fileName=='':
            printMsg('Uploading file: %s' % (fileName))
            transferFile(_host,_username, _password ,_filePath)
    _statusBar.config(text="System Ready", bg="#308446", width=75)  # Status Red
    _root.update()
def stop():
    global _processRun
    if _processRun == True:
        _processRun = False
    else:
        printMsg('Process not running.')
def hello():
    pass
def checkConn():
    global _statusBar,_host
    _statusBar.config(text="System Busy", bg="#cc0605", width=75)  # Status Red
    _root.update()
    p1 = subprocess.Popen(['ping', _host], stdout=subprocess.PIPE,shell=True)
    # Run the command
    output = p1.communicate()[0]
    if 'Lost = 0 (0% loss)' in output:
        printMsg('Tv Connected')
    else:
        printMsg('Connection Error')
    _statusBar.config(text="System Ready", bg="#308446", width=75)  # Status Red
    _root.update()
def openWebsite(event):
    webbrowser.open_new(r"http://electromed.co.in")
def preferencesDialog():
    Preferences(_root)
    readPreference()
def about():
    About(_root)
def createMenu():
    global _root
    menubar = Menu(_root)

    # create a pulldown menu, and add it to the menu bar
    filemenu = Menu(menubar, tearoff=0)
    # filemenu.add_command(label="Open", command=hello)
    # filemenu.add_command(label="Preferences", command=preferencesDialog)
    # filemenu.add_separator()
    filemenu.add_command(label="Exit", command=_root.quit)
    menubar.add_cascade(label="File", menu=filemenu)

    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Read Manual", command=hello)
    helpmenu.add_command(label="About", command=about)
    menubar.add_cascade(label="Help", menu=helpmenu)

    # display the menu
    _root.config(menu=menubar)
def guiInit(master):
    global _E1,_L2,_statusBar,_text,_progressBar
    createMenu()
    row=0
    f0 = Frame(master)
    L1 = Label(f0, text="Input File:")
    L1.grid(row=0, column=1, padx=20, pady=30)
    _E1 = Entry(f0, bd=5, width=40)
    _E1.grid(row=0, column=2, sticky=E + W, columnspan=3, padx=0, pady=0)
    # _E1.config(state=DISABLED)
    openButton = Button(f0, text="Browse...", command=openFile, width=10)
    openButton.grid(row=0, column=5, padx=30)
    f0.grid(row=0)
    row+=1

    _statusBar = Label(f0, text="System Ready", bg="#308446", width=75, pady=1, fg="#ffffff")  # Status Green
    _statusBar.grid(row=1, column=0, columnspan=7, pady=0)

    Label(f0).grid(row=2, column=0, pady=0)

    f1 = Frame(master)

    _L2 = Label(f1, text="Progress: 00.00%")
    _L2.grid(row=0, column=1, padx=0, pady=0)
    _progressBar = ttk.Progressbar(f1, orient=HORIZONTAL, mode='determinate',length=332)
    _progressBar.grid(row=0, column=2, columnspan=7,pady=0,sticky=W,padx=24)
    _progressBar["maximum"] = 100
    # Label(f0, text="").grid(row=3, column=10, padx=15, pady=0)

    f1.grid(row=row, padx=0, pady=0,sticky=W)
    lt1 = Label(f1, text="",padx=5)
    lt1.grid(row=1, column=0)
    uploadButton = Button(f1, text="Upload", command=upload, width=10)
    uploadButton.grid(row=1, column=1, padx=15,pady=20)
    checkButton = Button(f1, text="Check", command=checkConn, width=10)
    checkButton.grid(row=1, column=2, padx=15,pady=0)

    lt1 = Label(f1, text="",padx=15)
    lt1.grid(row=2, column=0)
    closeButton = Button(f1, text="Close TV", command=closetv, width=10)
    closeButton.grid(row=2, column=1, padx=10)
    lt2 = Label(f1, text="",padx=25)
    lt2.grid(row=2, column=2)
    stopButton = Button(f1, text="Stop", command=stop, width=10)
    stopButton.grid(row=2, column=2, padx=20)
    Label(f1, text="").grid(row=3, column=4, padx=15, pady=0)

    # Textbox
    fText = Frame(f1)
    fText.grid(row=1, rowspan=3, column=5, padx=0)
    textY = Scrollbar(fText)
    _text = Text(fText, width=20, height=5)
    _text.config(yscrollcommand=textY.set)
    textY.config(command=_text.yview)
    _text.grid(row=1, column=0)
    textY.grid(row=1, column=1, sticky=N + S)
    row += 1

    fFooter = Frame(master)
    fFooter.grid(row=row, padx=0)
    img = ImageTk.PhotoImage(Image.open(r"data\emFooter.jpg"))
    footer = Label(fFooter,image=img,borderwidth=0, highlightthickness=0,cursor="hand2")
    footer.bind("<Button-1>", openWebsite)
    footer.image = img  # keep a reference!
    footer.grid(row=0)

if __name__ == "__main__":
    global _host, _root, _username, _password
    _host = 'emTvUPCL001'
    # _username='emtvupcl001'
    _password='eM$7805!'
    _username='pi'
    # _password='raspberry'
    _root = Tk()
    _root.title('emTv  Assistant')
    _root.iconbitmap(default='data/transparent.ico')
    init(_root)
    _root.mainloop()