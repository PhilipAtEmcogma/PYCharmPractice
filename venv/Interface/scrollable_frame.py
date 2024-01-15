import tkinter as tk

class ScrollableFrame(tk.Frame):
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)

        self.canvas = tk.Canvas(self, highlightthickness=0,**kwargs)
        self.vsb = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.sub_frame = tk.Frame(self.canvas, **kwargs)

        # configure the scroll region of the canvas, and allow the use of mouse scroll when mouse is within the region
        self.sub_frame.bind("<Configures>",self._on_frame_configure)
        self.sub_frame.bind("<Enter>", self._activate_mousewheel)
        self.sub_frame.bind("<Leave>", self._deactivate_mousewheel)

        #anchor = "nw"  mean placing the component at the north west, i.e. top left corner
        self.canvas.create_window((0,0), window=self.sub_fram, anchor="nw")

        # linking canvas with the vertical scroll bar
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.X,expand=True)
        self.vsb.pack(side=tk.RIGHT, fill=tk.Y)

    def _on_frame_configure(self,event:tk.Event):
        # bbokx("all") , meant the coordinates of the canvas contents
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _activate_mousewheel(self, event:tk.Event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _deactivate_mousewheel(self, event: tk.Event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event: tk.Event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 60)),"units")