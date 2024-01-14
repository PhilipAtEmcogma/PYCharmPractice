import tkinter as tk
import typing

class Autocomplete(tk.Entry):
    def __init__(self, symbols: typing.List[str] ,*args, **kwargs):
        super().__init__(*args, **kwargs)

        self._symbols = symbols

        self._lb: tk.Listbox
        self._lb_open: False

        self.bind("<Up>", self._up_down)
        self.bind("<Down>", self._up_down)
        self.bind("<Right>", self._select)

        self._var = tk.StringVar()
        self.configure(textvariable=self._var)
        self._var.trace("w", self._changed)

    def _changed(self, var_name: str, index: str, mode: str):

        #captilize
        self._var.set(self._var.get().upper())

        if self._var.get() == "":
            if self._lb_open:
                self._lb.destroy()
                self._lb_open = False

        if not self._lb_open:
            self._lb = tk.Listbox(height = 8)
            self._lb.place(x=self.winfo_x() + self.winfo_width(), y=self.winfo_y() + self.winfo_height() + 10)
            self._lb_open = True

            # populate the listbox with symbols that match with what the user had inputted
            symbols_matched = [symbol for symbol in self._symbols if symbol.startswith(self._var.get())]

            # if list is more than 0, insert into the listbox
            if len(symbols_matched) > 0:
                try:
                    self._lb_delete(0,tk.END)
                except tk.TclError:
                    pass

                for symbol in symbols_matched:
                    self._lb.insert(tk.END, symbol)
            # if nothing is match, destory the box
            else:
                if self._lb_open:
                    self._lb.destory()
                    self._lb_open = False

    def _select(self, event:tk.Event):
        if self._lb_open:
            self._var.set(self._lb.get(tk.ACTIVE))
            self._lb.destroy()
            self._lb_open = False
            self.icursor(tk.END)

    def _up_down(self, event: tk.Event):

        if self._lb_open:
            if self._lb.curselectoin() == (): # no item is selected
                index =-1
            else:
                index = self._lb.curselection()[0] # select the 1st only, as only 1 item can be selected at a time

            lb_size = self._lb.size()

            if index > 0 and event.keysym == "Up":
                self._lb.select_clear(first=index) #clear selection
                index = str(index - 1)
                self._lb.selection_set(first=index)
                self._lb.activate(index)
            elif index < lb_size - 1 and event.keysym == "Down":
                self._lb.select_clear(first=index)
                index = str(index + 1)
                self._lb.selection_set(first=index)
                self._lb.activate(index)

