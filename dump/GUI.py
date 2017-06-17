#!/usr/bin/python

from Tkinter import *
import tempfile
from smb.SMBConnection import SMBConnection

def readText():
    reading = [];
    try:
        fo = open("data/messages.txt", "r+");
        for i in range(0, 5):
            reading.append(fo.readline());
        # Close opend file
        fo.close();
    except:
        pass

    return reading

def checkRetrievedFile(file_obj):
    copy_file_object = open('data/messages.txt', 'w');
    file_obj.seek(0);
    for i in range(0, 5):
        temp = file_obj.readline();
        copy_file_object.write(temp);
    return True;

#### to make ui full screen
def toggle_geom(self,event):
    geom=self.master.winfo_geometry()
    print(geom,self._geom)
    self.master.geometry(self._geom)
    self._geom=geom

def guiInit(master):
    row=0

    # #### Set fullscreen
    # self.master=master
    # pad=3
    # self._geom='200x200+0+0'
    # master.geometry("{0}x{1}+0+0".format(
    #     master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
    # master.bind('<Escape>',self.toggle_geom)
    # # master.overrideredirect(1)
    #
    # ###############################################################
    global mess;

    _mess=readText();

    f0 = Frame(master)

    for i in range(0,5):
        temp = Label(f0,text=_mess[i],bg="#0000ff",height=5,width=194,fg="#ffffff") #Status Green
        _labels.append(temp);
        _labels[i].grid(row=i,column=0)

    f0.grid(row=0)
    loop();

def loop():
    global _mess;
    temp = getLanFile();
    if temp!=_mess and temp!=[] :
        _mess = temp;
        for i in range(0, 5):
            print _mess[i];
            _labels[i].config(text=temp[i]);
            _root.update_idletasks()
            _root.update()
    _root.after(10000,loop);

def lanConnectionInit():
    global _conn;
    _conn = SMBConnection('username', '', ' ', ' ', '',  # use_ntlm_v2=True,
                         # sign_options=SMBConnection.SIGN_WHEN_SUPPORTED,
                         is_direct_tcp=True)
    connected = _conn.connect('192.168.1.10', 445)
    Response = _conn.listShares(timeout=30)

    for i in range(len(Response)):
        print("Share[", i, "] =", Response[i].name)

def getLanFile():

    global _conn;
    file_obj = tempfile.NamedTemporaryFile()
    reading = [];
    try:
        file_attributes, filesize = _conn.retrieveFile('F_Rai\'s', '/lan-tv/data/messages.txt', file_obj);
        print filesize;
        if checkRetrievedFile(file_obj):
            reading = readText();
            for i in range(0, 5):
                print reading[i];
        file_obj.close();
    except:
        file_obj.close();

    if reading == []:
        return _mess;
    else:
        return reading;

_mess = [];
_labels = [];
lanConnectionInit()

_root = Tk()
guiInit(_root)
_root.mainloop()
