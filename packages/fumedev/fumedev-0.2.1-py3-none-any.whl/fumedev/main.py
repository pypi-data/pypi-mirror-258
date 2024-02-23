import copy
import os
from fumedev import env

env.FILE_FOLDER = os.path.dirname(os.path.abspath(__file__))
os.makedirs(env.USER_HOME_PATH.joinpath('FumeData'), exist_ok=True) 

from dotenv import load_dotenv
from fumedev.gui.app import FumeApp

load_dotenv()

if __name__ == "__main__":
    app = FumeApp()
    app.run()