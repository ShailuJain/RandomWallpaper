from tkinter import *

from random_wallpaper import RandomWallpaper


class MyText(Text):
    def append(self, string):
        self.insert(INSERT, string+"\n")

    def get_text(self):
        return self.get(0, END)


class RandomWallpaperUI(Frame):

    def __init__(self, master, **kwargs):
        super().__init__(master=master, **kwargs)
        self.master.title("Random Wallpaper Setter")
        self.lblSearch = self.txtSearch = self.lblIntervalTime = self.txtIntervalTime = self.topFrame = \
            self.btnSetInterval = self.topFrame1 = self.set = self.stop = self.bottomFrame = None

        self.text = MyText(master=self)
        self.create_widgets()
        self.pack(fill=BOTH, expand=True)
        self.isStarted = False
        self.randomWallpaper = RandomWallpaper(text=self.text)

    def create_widgets(self):
        self.master.geometry("800x550")
        self.topFrame = Frame(master=self)
        self.topFrame1 = Frame(master=self)
        self.bottomFrame = Frame(master=self)

        # lblSearch
        self.lblSearch = Label(master=self.topFrame, text="Wallpaper Search : ", font=("Helvetica", 10, "bold"))
        self.lblSearch.pack(padx=10, pady=10, side=LEFT, expand=True)

        # txtSearch
        self.txtSearch = Entry(master=self.topFrame, width=400, font=("Helvetica", 10))
        self.txtSearch.insert(0, "Enter text to search")
        self.txtSearch.bind("<FocusOut>", self.txtSearchFocusedOut)
        self.txtSearch.bind("<FocusIn>", self.txtSearchFocused)
        self.txtSearch.pack(padx=10, pady=10, side=LEFT, fill=X)

        # lblIntervalTime
        self.lblIntervalTime = Label(master=self.topFrame1, text="Enter interval time in hours : ", font=("Helvetica", 10, "bold"))
        self.lblIntervalTime.pack(padx=10, pady=10, side=LEFT)

        # txtIntervalTime
        self.txtIntervalTime = Entry(master=self.topFrame1, width=10, font=("Helvetica", 10))
        self.txtIntervalTime.pack(padx=10, pady=10, side=LEFT)

        # btnSetInterval
        self.btnSetInterval = Button(master=self.topFrame1, text="Set interval", bg="springgreen",
                                     command=self.set_interval)
        self.btnSetInterval.pack(padx=10, pady=5, side=LEFT)

        self.topFrame.pack(side=TOP, fill=X)
        self.topFrame1.pack(side=TOP, fill=X)

        # text
        self.text.pack(side=TOP)

        self.bottomFrame.pack(side=BOTTOM)

        #set
        self.set = Button(master=self.bottomFrame, text="Set Random Wallpaper", bg="springgreen",
                          command=self.set_clicked)
        self.set.pack(padx=5, pady=5, side=LEFT)

        # stop
        self.stop = Button(master=self.bottomFrame, text="Stop Random Wallpaper", bg="springgreen",
                           command=self.stop_clicked)
        self.stop.pack(padx=5, pady=5, side=LEFT)

    def txtSearchFocused(self, event):
        event.widget.delete(0, len(event.widget.get()))

    def txtSearchFocusedOut(self, event):
        if event.widget.get() == "":
            event.widget.insert(0, "Enter text to search")

    def on_closing(self):
        self.master.iconify()

    def set_clicked(self):
        if self.randomWallpaper:
            self.randomWallpaper.set_search_query(self.txtSearch.get())
            self.randomWallpaper.set_time_interval(self.get_interval())
            if self.isStarted:
                self.randomWallpaper.set_random_wallpaper()
            else:
                self.randomWallpaper.start()
                self.isStarted = True

    def set_interval(self):
        if self.randomWallpaper:
            self.randomWallpaper.set_time_interval(self.get_interval())

    def get_interval(self):
        if self.txtIntervalTime.get() != "":
            interval = float(self.txtIntervalTime.get())
            return interval
        return 1

    def stop_clicked(self):
        if self.randomWallpaper:
            self.randomWallpaper.stop()


root = Tk()
rw = RandomWallpaperUI(master=root)
root.resizable(width=False, height=False)
root.protocol("WM_DELETE_WINDOW", rw.on_closing)
root.mainloop()
