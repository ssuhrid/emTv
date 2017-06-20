import tkFileDialog
from Tkinter import *
import subprocess
import ttk
import time
import tkFileDialog


class GUI:
    def display(self, msg):
        self.text.insert(END, msg)
        self.text.insert(END, '\n')
        self.text.see(END)

    def __init__(self, master):
        # master=
        # master.minsize(width=480, height=340)
        self.fReading = False
        self.fWriting = False
        self.fVerifying = False
        self.fErasing = False
        self.bar = ''
        self.createMenu(master)
        ##        master.geometry('{}x{}'.format(620, 300))

        row = 0

        # Controller
        f0 = Frame(master)
        f0.grid(row=row, sticky=W)
        L0 = Label(f0, text="Select IC: ")
        # L0.grid(row=0, column=0, padx=20, pady=10)
        lst1 = ['ATMEGA328P', 'Option2', 'Option3']
        self.var1 = StringVar(f0)
        self.var1.set(lst1[0])
        # drop = OptionMenu(f0, self.var1, *lst1)
        # drop.grid(column=1,row=0,padx=10)
        row += 1

        # Entry
        f1 = Frame(master)
        f1.grid(row=row)
        L1 = Label(f1, text="Hex File:")
        L1.grid(row=0, column=1, padx=20, pady=30)
        self.E1 = Entry(f1, bd=5, width=40)
        self.E1.grid(row=0, column=2, sticky=E + W, columnspan=3, padx=20, pady=0)
        openButton = Button(f1, text="Browse...", command=self.openFile, width=10)
        openButton.grid(row=0, column=5)

        # Button
        # f2=Frame(master)
        # f2.grid(row=1,pady=10)
        C = Button(f1, text="Write", command=self.write, width=10)
        D = Button(f1, text="Initialize", command=self.init, width=10)
        B = Button(f1, text="Lock", command=self.lock, width=10)
        buttErase = Button(f1, text="Erase", command=self.erase, width=10)
        buttAuto = Button(f1, text="Auto", command=self.auto, width=10)
        buttAuto.grid(row=1, column=1, padx=10)
        D.grid(row=1, column=3, padx=10)
        buttErase.grid(row=1, column=2, padx=10)
        C.grid(row=1, column=4, padx=10)
        B.grid(row=1, column=5, padx=10, pady=0)
        self.statusBar = Label(f1, text="Programmer Ready", bg="#308446", width=88, fg="#ffffff")  # Status Green
        ##        self.statusBar=Label(f1,text="Programmer Busy",bg="#cc0605",width=88,fg="#ffffff",height=1) #Status Red
        self.statusBar.grid(row=2, column=0, columnspan=7, pady=20)
        row += 1

        fText = Frame(f3)
        fText.grid(row=0, rowspan=3, column=2, padx=20)
        textY = Scrollbar(fText)
        self.text = Text(fText, width=30, height=5)
        self.text.config(yscrollcommand=textY.set)
        textY.config(command=self.text.yview)
        # textX.config(command=self.text.xview)
        self.text.grid(row=0, column=0)
        textY.grid(row=0, column=1, sticky=N + S)
        # textX.grid(row=1, column=0, sticky=E + W)
        row += 1

        # Footer
        f4 = Frame(master)
        text2 = Label(f4, height=1)
        text2.grid(row=0)
        f4.grid(row=row)


root = Tk()
root.title('AVR Uploader v2.3')
b = GUI(root)
root.mainloop()

