import time
import pandas as pd
import tkinter as tk
import logging
import requests
import os
from dotenv import load_dotenv
import pprint

from Connector.binance_futures import BinanceFuturesClient
from Connector.bitmex import BitmexClient

from Interface.root_component import Root

load_dotenv() #loading the variables stored in .env
#print(os.environ['BINANCE_API_KEY']) #test to see if variables loaded correctly.

logger = logging.getLogger()


# REST API
# "https://testnet.binancefuture.com"
# "wss://fstream.binance.com" # wss means web socket



""""
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # To show Debug level massage, change logging.INFO to logging.DEBUG

stream_handler = logging.StreamHandler()
# show current time
formatter = logging.Formatter('%(asctime)s %(levelname)s :: %(message)s')
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler('info.log')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

logger.debug("This message is important on when debugging is in the program")
logger.info("This message are shown basic information")
logger.warning("This message is about something you should pay attention to")
logger.error("This message helps to debug an error that occurred in the program")

write_log()
"""


# below if satement meant that the block of code only executed if the py file call "main" is executed
# so if we run other python scripts that does have the name "main", it'll not run
if __name__ == '__main__':

    # bitmex_contracts = get_contracts()
    # NOTE: the api_key and secret_for Binance and Bitmex both are save in .env, because the code are uploaded
    #   into github, thus to protect the private keys from being accessable by public, it was good practice to have them
    #   store in .env and pass the .env file to gitignore.

    binance = BinanceFuturesClient(os.environ['BINANCE_API_KEY'], os.environ['BINANCE_API_SECRET'],True)
    # print(binance.get_historical_candles("BTCUSDT","1h"))

    # self.headers = {'X-MBX-APIKEY': self.public_key}
    # print(binance.get_balance())
    # print(binance.place_order("BTCUSDT","BUY",0.01,"LIMIT",50000,"GTC"))
    # print(binance.get_order_status("BTCUSDT",3583386003))
    # print(binance.cancel_order("BTCUSDT",3583386003))


    bitmex = BitmexClient(os.environ['BITMEX_API_KEY'], os.environ['BITMEX_API_SECRET'],True)


    # root component, for creating the general outline of the UI
    # pass binance and bitmex keys into Root to instandciate it
    root = Root(binance, bitmex)
    root.mainloop()

    """
    root.configure(bg="gray12")

    i = 0
    j = 0

    calibri_font = ("Calibri",11,"normal")

    #populate the widget, must be place after root is created but before mainloop
    for contract in bitmex_contracts:
        label_widget = tk.Label(root,text=contract, bg='gray12', fg='SteelBlue', borderwidth=1, relief=tk.GROOVE, width=13, font=calibri_font)
        # place the label_widge into room using
        # grid() -> good for if there's a lot of widget to be place or
        # pack() ->place widge relative to each other, good if there isn't much widget
        label_widget.grid(row = i, column = j, sticky ='ew')
        # sticky = 'ew', sticky mean streatch out the widget to fill the space, e means east aka right,w means west ask left
        if i == 4:
            j += 1
            i = 0
        else:
            i += 1
    """



