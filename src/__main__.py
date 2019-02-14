import subprocess
import sys
from tkinter import Tk
from src.random_wallpaper_ui import RandomWallpaperUI


def install(package):
    try:
        subprocess.call([sys.executable, "-m", "pip", "install", package])
    except Exception as e:
        print(e)


def install_all_packages():
    install('requests')
    install('beautifulsoup4	')


install_all_packages()
root = Tk()
rw = RandomWallpaperUI(master=root)
root.resizable(width=False, height=False)
root.protocol("WM_DELETE_WINDOW", rw.on_closing)
root.mainloop()


