import subprocess
import sys
from tkinter import Tk


def install(package):
    try:
        subprocess.call([sys.executable, "-m", "pip", "install", package])
    except Exception as e:
        print(e)


def install_all_packages():
    install('requests')
    install('beautifulsoup4	')
    install('pywin32')
    install('PyInstaller')


# install_all_packages()
from src.random_wallpaper_ui import RandomWallpaperUI

root = Tk()
rw = RandomWallpaperUI(master=root)
root.resizable(width=False, height=False)
root.protocol("WM_DELETE_WINDOW", rw.on_closing)
root.mainloop()


