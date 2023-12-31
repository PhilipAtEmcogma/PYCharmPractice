import tkinter as tk
from datetime import datetime

from Interface.styling import *

class Logging(tk.Frame):
    def __init__(self,*args,**kwargs):
        #super() initiate a frame to argument pass into it
        super().__init__(*args,**kwargs)

        self.logging_text = tk.Text(self, height=19, width=60, state=tk.DISABLED, bg=BG_COLOR, fg=FG_COLOR_2, font=GLOBAL_FONT)
        self.logging_text.pack(side=tk.TOP)

    """
    def add_log(self, message: str):
        self.logging_text.configure(state=tk.NORMAL)
        # "1.0" mean text will be place at the top of the widget
        self.logging_text.insert("1.0", datetime.utcnow().strftime("%a %H:%M:%S :: ") + message + "\n")
        self.logging_text.configure(state=tk.DISABLED)
    """
