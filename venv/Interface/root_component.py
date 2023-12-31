import tkinter as tk
import time

from Connector.bitmex import BitmexClient
from Connector.binance_futures import BinanceFuturesClient

from Interface.styling import *
from Interface.logging_component import Logging

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

        # placing logging component to the left and align to top
        self._logging_frame = Logging(self._left_frame,bg=BG_COLOR)
        self._logging_frame.pack(side=tk.TOP)

        #update itself once to do initial check
        self._update_ui()

    # checks periodically for new logs to add
    def _update_ui(self):

        for log in self.bitmex.logs:
            if not log['displayed']:
                self._logging_frame.add_log(log['log'])
                log['displayed'] = True

        for log in self.binance.logs:
            if not log['displayed']:
                self._logging_frame.add_log(log['log'])
                log['displayed'] = True

        #call itself (recursive) every 1.5 second to see if there's new data to be logged
        self.after(1500, self._update_ui())

        """
        self._logging_frame.add_log("This is a test message")
        time.sleep(2)
        self._logging_frame.add_log("This is a another test message")
        """