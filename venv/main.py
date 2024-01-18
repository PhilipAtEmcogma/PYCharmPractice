import logging

from connectors.binance import BinanceClient
from connectors.bitmex import BitmexClient

from Interface.root_component import Root

import os
from dotenv import load_dotenv


load_dotenv() #loading the variables stored in .env
#print(os.environ['BINANCE_API_KEY']) #test to see if variables loaded correctly.

# Create and configure the logger object

logger = logging.getLogger()

logger.setLevel(logging.DEBUG)  # Overall minimum logging level

stream_handler = logging.StreamHandler()  # Configure the logging messages displayed in the Terminal
formatter = logging.Formatter('%(asctime)s %(levelname)s :: %(message)s')
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)  # Minimum logging level for the StreamHandler

file_handler = logging.FileHandler('info.log')  # Configure the logging messages written to a file
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)  # Minimum logging level for the FileHandler

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

# REST API
# "https://testnet.binancefuture.com"
# "wss://fstream.binance.com" # wss means web socket


# below if satement meant that the block of code only executed if the py file call "main" is executed
# so if we run other python scripts that does have the name "main", it'll not run
if __name__ == '__main__':

    # bitmex_contracts = get_contracts()
    # NOTE: the api_key and secret_for Binance and Bitmex both are save in .env, because the code are uploaded
    #   into github, thus to protect the private keys from being accessable by public, it was good practice to have them
    #   store in .env and pass the .env file to gitignore.

    binance = BinanceClient(os.environ['BINANCE_API_KEY'], os.environ['BINANCE_API_SECRET'],testnet=True, futures = True)
    bitmex = BitmexClient(os.environ['BITMEX_API_KEY'], os.environ['BITMEX_API_SECRET'],testnet=True)


    # root component, for creating the general outline of the UI
    # pass binance and bitmex keys into Root to instandciate it
    root = Root(binance, bitmex)
    root.mainloop()


