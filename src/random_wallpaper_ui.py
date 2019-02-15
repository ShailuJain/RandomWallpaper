import time
from threading import Thread
from tkinter import *

from pynput.keyboard import *

from src.random_wallpaper import RandomWallpaper


class MyText(Text):
    def append(self, string):
        self.insert(INSERT, str(string)+"\n")

    def get_text(self):
        return self.get(0, END)


class RandomWallpaperUI(Frame):

    def __init__(self, master, **kwargs):
        super().__init__(master=master, **kwargs)
        self.master.resizable(width=False, height=False)
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.master.title("Random Wallpaper Setter")
        self.lblSearch = self.txtSearch = self.lblIntervalTime = self.txtIntervalTime = self.topFrame = \
            self.btnSetInterval = self.topFrame1 = self.set = self.stop = self.bottomFrame = self.hide = None

        self.current_key = set()
        self.searchText = "Enter text to search"
        scrollbar = Scrollbar(master=self)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.text = MyText(master=self, yscrollcommand=scrollbar.set)
        self.create_widgets()
        scrollbar.config(command=self.text.yview)
        self.pack(fill=BOTH, expand=True)
        self.isStarted = False
        self.COMBINATION = (Key.ctrl_l, Key.alt_l, Key.space)
        self.randomWallpaper = RandomWallpaper(ui=self)
        self.listener = None
        Thread(target=self.show_on_keys).start()

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
        self.txtSearch.insert(0, self.searchText)
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

        # set
        self.set = Button(master=self.bottomFrame, text="Set Random Wallpaper", bg="springgreen",
                          command=self.set_clicked)
        self.set.pack(padx=5, pady=5, side=LEFT)

        # stop
        self.stop = Button(master=self.bottomFrame, text="Stop Random Wallpaper", bg="springgreen",
                           command=self.stop_clicked)
        self.stop.pack(padx=5, pady=5, side=LEFT)

        # hide
        self.hide = Button(master=self.bottomFrame, text="Hide window", bg="springgreen",
                           command=self.hide_clicked)
        self.hide.pack(padx=5, pady=5, side=LEFT)

    def txtSearchFocused(self, event):
        if event.widget.get() == self.searchText:
            event.widget.delete(0, len(event.widget.get()))

    def txtSearchFocusedOut(self, event):
        if event.widget.get() == "":
            event.widget.insert(0, self.searchText)

    def on_closing(self):
        if self.isStarted:
            self.master.iconify()
            self.text.append("Iconify")
        else:
            if self.listener:
                self.listener.stop()
            self.master.destroy()

    def set_clicked(self):
        if self.randomWallpaper:
            self.randomWallpaper.set_search_query(self.txtSearch.get())
            self.randomWallpaper.set_time_interval(self.get_interval())
            if self.isStarted:
                self.text.append("Set Clicked")
                Thread(target=self.randomWallpaper.set_random_wallpaper).start()
            else:
                self.text.append("Starting Random wallpaper")
                self.isStarted = True
                self.randomWallpaper.start()

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
            self.text.append("Stopping")
            self.isStarted = False
            self.randomWallpaper.stop()

    def hide_clicked(self):
        self.text.append("Hiding")
        self.master.withdraw()

    def wait(self):
        self.text.append("Wait")
        self.set.state = 'disabled'
        self.stop.state = 'disabled'
        time.sleep(60)
        self.set.state = 'normal'
        self.stop.state = 'normal'

    def show_on_keys(self):
        def on_key_pressed(key):
            self.current_key.add(key)
            if all(k in self.current_key for k in self.COMBINATION):
                self.master.deiconify()

        def on_key_released(key):
            try:
                self.current_key.remove(key)
            except KeyError:
                pass
        with Listener(on_press=on_key_pressed, on_release=on_key_released) as self.listener:
            self.listener.join()
        print("after listener join")
