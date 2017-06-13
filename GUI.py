#!/usr/bin/python

from Tkinter import *

class Gui:


    def readText(self):
        fo = open("data/messages.txt", "r+")
        mess = [];
        for i in range(0, 8):
            mess.append(fo.readline());
        fo.close()
        for i in range(0,5):
            print mess[i];
        return mess;

    #### to make ui full screen
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom

    def __init__(self,master):
        row=0

        #### Set fullscreen
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)
        master.overrideredirect(1)

        ###############################################################

        mess=self.readText();

        labels = [];
        f0 = Frame(master)

        for i in range(0,8):
            temp = Label(f0,text=mess[i],bg="#0000ff",height=5,width=194,fg="#ffffff") #Status Green
            labels.append(temp);
            labels[i].grid(row=i,column=0)

        f0.grid(row=0)

root = Tk()
##root.title('AVR Uploader v2.3')
b=Gui(root)
root.mainloop()
    