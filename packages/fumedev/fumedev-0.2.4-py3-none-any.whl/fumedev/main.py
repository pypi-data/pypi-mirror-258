import os
from fumedev import env
from fumedev.lllm_utils.rerank_snippets import rerank_snippets
from fumedev.utils.search_snippet import search_snippet

env.FILE_FOLDER = os.path.dirname(os.path.abspath(__file__))
os.makedirs(env.USER_HOME_PATH.joinpath('FumeData'), exist_ok=True) 

from dotenv import load_dotenv
from fumedev.gui.app import FumeApp

load_dotenv()

def main():
    app = FumeApp()
    app.run()

if __name__ == "__main__":
    main()