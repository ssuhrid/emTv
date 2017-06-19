from Tkinter import *

class Preferences(Toplevel):

    def __init__(self, parent, title = None):

        Toplevel.__init__(self, parent)
        self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent

        self.result = None

        body = Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))

        self.initial_focus.focus_set()

        self.wait_window(self)

    #
    # construction hooks

    def checkCheckbox(self):
        for i in range(0,5):
            if not self.hostTicks[i].get():
                self.hostEntry[i].config(state=DISABLED)
                self.hostNickname[i].config(state=DISABLED)
            else:
                self.hostEntry[i].config(state=NORMAL)
                self.hostNickname[i].config(state=NORMAL)
        pass

    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden

        self.hostCheckbox = []
        self.hostTicks = []
        self.hostNickname = []
        self.hostEntry = []
        f0 = Frame(master)

        Label(f0, text="Active").grid(row=0, column=0)
        Label(f0, text="Nickname").grid(row=0, column=1)
        Label(f0, text="Host").grid(row=0, column=2)

        for i in range(0,5):
            self.hostTicks.append(IntVar())
            self.hostCheckbox.append(Checkbutton(f0,pady=5,
                    variable = self.hostTicks[i],command = self.checkCheckbox))
            self.hostCheckbox[i].grid(row=i+1, column=0)
            self.hostNickname.append(Entry(f0, bd=5, width=40))
            self.hostNickname[i].grid(row=i+1, column=1, pady=0)
            self.hostEntry.append(Entry(f0, bd=5, width=40))
            self.hostEntry[i].grid(row=i+1, column=2,padx=20, pady=0)

        f0.grid(row=0,column=0)
        pass

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons

        box = Frame(self)

        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)

        # self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    #
    # standard button semantics

    def ok(self, event=None):
        pref = open('pref.txt','w')
        for i in range(0,5):
            pref.write(str(self.hostTicks[i].get()))
            pref.write('~')
            pref.write(self.hostNickname[i].get())
            pref.write('~')
            pref.write(self.hostEntry[i].get())
            pref.write('\n')
        pref.close()
        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return
        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()

    def cancel(self, event=None):

        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    #
    # command hooks

    def validate(self):

        return 1 # override

    def apply(self):

        pass # override

if __name__ == "__main__":
    root = Tk()
    Preferences(root)