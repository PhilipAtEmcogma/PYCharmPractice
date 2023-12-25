import time
import pandas as pd
import tkinter as tk
import logging
from binance_futures import write_log
import requests
import os
from dotenv import load_dotenv
import pprint
from bitmex import get_contracts

load_dotenv() #loading the variables stored in .env
# print(os.environ['BINANCE_API_KEY']) #test to see if variables loaded correctly.

logger = logging.getLogger()


# REST API
# "https://testnet.binancefuture.com"
# "wss://fstream.binance.com" # wss means web socket

def get_contracts():
    response_object = requests.get("https://fapi.binance.com/fapi/v1/exchangeInfo")
    # print(response_object.status_code)
    # pprint.pprint(response_object.json())
    # pprint.pprint(response_object.json()['symbols'])
    contracts = []

    for contract in response_object.json()['symbols']:
        # pprint.pprint(contract)
        # print(contract['pair'])
        contracts.append(contract['pair'])

    return contracts

# def get_bitmex_contracts():
    # response_object = requests.get("https://www.bitmex.com/api/v1/instrument")

print(get_contracts())

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

    bitmex_contracts = get_contracts()

    # root component, for creating the general outline of the UI
    root = tk.Tk()
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

    root.mainloop()

