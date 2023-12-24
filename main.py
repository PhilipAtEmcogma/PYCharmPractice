import time
import pandas as pd
import tkinter as tk
import logging
from binance_futures import write_log

logger = logging.getLogger()
logger.setLevel(logging.INFO) #To show Debug level massage, change logging.INFO to logging.DEBUG

stream_handler = logging.StreamHandler()
#show current time
formatter = logging.Formatter('%(asctime)s %(levelname)s :: %(message)s')
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler('info.log')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

"""
logger.debug("This message is important on when debugging is in the program")
logger.info("This message are shown basic information")
logger.warning("This message is about something you should pay attention to")
logger.error("This message helps to debug an error that occurred in the program")

write_log()
"""

#below if satement meant that the block of code only executed if the py file call "main" is executed
# so if we run other python scripts that does have the name "main", it'll not run
if __name__ == '__main__':
    #root component, for creating the general outline of the UI
    root = tk.Tk()
    root.mainloop()