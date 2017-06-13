#!/usr/bin/python

from Tkinter import *

class Gui:

    def readText(self):
        mess = [];
        try:
            fo = open("data/messages.txt", "r+");

            for i in range(0, 5):
                mess.append(fo.readline());
            # Close opend file
            fo.close();
        except:
            pass

        return mess

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
        # master.overrideredirect(1)

        ###############################################################

        self.mess=self.readText();

        self.labels = [];
        f0 = Frame(master)

        for i in range(0,5):
            temp = Label(f0,text=self.mess[i],bg="#0000ff",height=5,width=194,fg="#ffffff") #Status Green
            self.labels.append(temp);
            self.labels[i].grid(row=i,column=0)

        f0.grid(row=0)
        self.loop();

    def loop(self):
        mess = [];
        # while True:
        print 'sex'
        temp = self.readText();
        if temp!=self.mess and temp!=[] :
            mess = temp;
            for i in range(0, 5):
                print mess[i];
                self.labels[i].config(text=mess[i]);
                root.update_idletasks()
                root.update()
        root.after(5000,self.loop);

root = Tk()
##root.title('AVR Uploader v2.3')
b=Gui(root)
# root.after(5000,b.loop);
root.mainloop()
# root.update_idletasks()
# root.update()