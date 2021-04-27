import os
from telethon.tl.types import ChatBannedRights
ENV = bool(os.environ.get("ENV", False))
if ENV:
    import os
    class Config(object):
        CHROME_DRIVER = os.environ.get("CHROME_DRIVER", "/app/.chromedriver/bin/chromedriver")
        GOOGLE_CHROME_BIN = os.environ.get("GOOGLE_CHROME_BIN", "/app/.apt/usr/bin/google-chrome")
        TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TEMP_DOWNLOAD_DIRECTORY", "./")
else:
    class Config(object):
        DB_URI = None
       
