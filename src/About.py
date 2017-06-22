from Tkinter import *
import webbrowser

class About(Toplevel):

    def openWebsite(self,event):
        webbrowser.open_new(r"http://electromed.co.in")

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

    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden

        w =Label(master,text='Build Information: \n\nCompiled for:'
                             '\nUdupi Power Corporation Limited'
                           '\nKarnataka'
                          '\n\nBuild date: 18 June 2017 '
                          '\n\nWritten and distributed by:'
                          '\n\nELECTRO-MED Lucknow'
                          ,anchor=W,justify=LEFT)
        w.pack(side=TOP)
        link = Label(master,text='www.electromed.co.in',anchor =W,justify=LEFT, cursor="hand2",fg="blue")
        link.bind("<Button-1>",self.openWebsite)
        link.pack(side=TOP,fill=X)
        pass

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons

        box = Frame(self)

        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    #
    # standard button semantics

    def ok(self, event=None):

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

if __name__=="__main__":
    root=Tk()
    About(root)
    root.mainloop()