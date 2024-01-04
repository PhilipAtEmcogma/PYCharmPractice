import logging
import tkinter as tk
import time

from Connector.bitmex import BitmexClient
from Connector.binance_futures import BinanceFuturesClient

from Interface.styling import *
from Interface.logging_component import Logging
from Interface.watchlist_component import Watchlist
from Interface.trades_component import TradesWatch

logger = logging.getLogger()

class Root(tk.Tk):
    def __init__(self, binance:BinanceFuturesClient, bitmex:BitmexClient):
        super().__init__()

        #instantciate bitmex and binance
        self.binance = binance
        self.bitmex = bitmex

        self.title("Trading Bot")

        self.configure(bg=BG_COLOR)

        # remeber add _ turn variable into a private variable
        self._left_frame = tk.Frame(self, bg=BG_COLOR)
        self._left_frame.pack(side=tk.LEFT)

        self._right_frame = tk.Frame(self, bg=BG_COLOR)
        self._right_frame.pack(side=tk.LEFT)

        self._watchlist_frame = Watchlist(self.binance.contracts, self.bitmex.contracts,self._left_frame,bg=BG_COLOR)
        self._watchlist_frame.pack(side=tk.TOP)

        # placing logging component to the left and align to top
        self._logging_frame = Logging(self._left_frame,bg=BG_COLOR)
        self._logging_frame.pack(side=tk.TOP)

        self._trades_frame = TradesWatch(self._right_frame,bg=BG_COLOR)
        self._trades_frame.pack(side=tk.TOP)

        #update itself once to do initial check
        self._update_ui()

    # checks periodically for new logs to add
    def _update_ui(self):
        # Logs

        for log in self.bitmex.logs:
            if not log['displayed']:
                self._logging_frame.add_log(log['log'])
                log['displayed'] = True

        for log in self.binance.logs:
            if not log['displayed']:
                self._logging_frame.add_log(log['log'])
                log['displayed'] = True

        #Watchlist prices
        try:
            # loop through all the objects in a coloumn
            for key, value in self._watchlist_frame.body_widgets['symbol'].items():
                symbol = self._watchlist_frame.body_widgets['symbol'][key].cget("text")
                exchange = self._watchlist_frame.body_widgets['exchange'][key].cget("text")

                if exchange == "Binance":
                    # 1st make sure the exhnage have this symbol to trade
                    if symbol not in self.binance.contracts:
                        continue

                    if symbol not in self.binance.prices:
                        self.binance.get_bid_ask(self.binance.contracts[symbol])
                        continue

                    precision = self.binance.contracts[symbol].price_decimals
                    prices = self.binance.prices[symbol]

                elif exchange == "Bitmex":
                    # 1st make sure the exhnage have this symbol to trade
                    if symbol not in self.bitmex.contracts:
                        continue

                    if symbol not in self.bitmex.prices:
                        continue

                    precision = self.bitmex.contracts[symbol].price_decimals
                    prices = self.bitmex.prices[symbol]

                else:
                    continue

                if prices['bid'] is not None:
                    #limit the amount of decimals to display
                    price_str = "{0:.{prec}f}".format(prices['bid'], prec=precision)
                    self._watchlist_frame.body_widgets['bid_var'][key].set(price_str)

                if prices['ask'] is not None:
                    #limit the amount of decimals to display
                    price_str = "{0:.{prec}f}".format(prices['ask'], prec=precision)
                    self._watchlist_frame.body_widgets['ask_var'][key].set(price_str)

        except RuntimeError as e:
            logger.error("Error while looping through watchlist dictionary: %s", e)

        # call itself (recursive) every 1.5 second to see if there's new data to be logged
        self.after(1500, self._update_ui())

        """
        self._logging_frame.add_log("This is a test message")
        time.sleep(2)
        self._logging_frame.add_log("This is a another test message")
        """