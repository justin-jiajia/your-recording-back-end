from your_recording import create_app
from dotenv import load_dotenv
from os import path
if path.exists('.env'):
    load_dotenv('.env')
if path.exists('.flaskenv'):
    load_dotenv('.flaskenv')
app = create_app('production')
