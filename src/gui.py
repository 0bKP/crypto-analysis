import tkinter as tk
import data_processing
from tkinter import ttk

bgColor = "#161618"
logoBarColor = "#FF9900"


def toggle(element, side, expand=False, fill=None, padx=0, pady=0):
    if element.winfo_ismapped():
        element.pack_forget()
    else:
        element.pack(side=side, expand=expand, fill=fill, padx=padx, pady=pady)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1440x1024+250+20")
        self.configure(bg=bgColor)
        # self.overrideredirect(True)
        self.resizable(False, False)

        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except Exception as e:
            print(e)

        self.drag_data = {"x": 0, "y": 0, "item": None}

        # Nav bar
        self.nav_bar = tk.Frame(background=logoBarColor, height=100)
        self.nav_bar.pack(side="top", fill="x", padx=10, pady=10)
        self.nav_bar.pack_propagate(False)

        # # # Nav bar buttons
        self.burger_button = tk.Button(self.nav_bar, width=8, text="Burger", command=self.toggle_settings_bar)
        self.burger_button.pack(side="left", fill="y")

        self.analysis_button = tk.Button(self.nav_bar, text="Analysis")
        self.analysis_button.pack(side="top")
        self.analysis_button.bind("<ButtonPress-1>", self.on_start_drag)
        self.analysis_button.bind("<B1-Motion>", self.on_drag_motion)
        self.analysis_button.bind("<ButtonRelease-1>", self.on_drag_release)

        # Main screen
        self.canvas = tk.Canvas(self, background=bgColor, highlightthickness=0, highlightbackground="red")
        self.canvas.pack(side="right", expand=True, fill="both", padx=10, pady=10)

        self.display_screen = tk.Frame(self.canvas, background=bgColor)
        self.canvas.create_window((0, 0), window=self.display_screen, anchor="w")

        self.scrollbar = ttk.Scrollbar(self.canvas, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.display_screen.bind('<Configure>', self.on_frame_configure)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # # # Plot
        self.plot_frame = tk.Frame(self.display_screen, background=bgColor, width=100, height=100)
        self.plot_frame.pack(side="left", anchor="nw")

        # # # Analysis tools frame
        self.tools_frame = tk.Frame(self.display_screen, background=bgColor, width=100, height=100,
                                             highlightthickness=1, highlightbackground="pink")
        self.tools_frame.propagate(False)

        self.analysis_label = tk.Label(self.tools_frame, text="Analysis")
        self.analysis_label.pack(side="top", fill="x")

        self.cckbtn = tk.IntVar()
        self.trend_line = tk.Checkbutton(self.tools_frame, text="Trend line", variable=self.cckbtn,
                                         onvalue=1, offvalue=0,
                                         command=self.enable_trend_line)
        self.trend_line.pack(side="right", padx=10, pady=10)

        # # # Another frame I don't know what for yet
        self.bottom_frame = tk.Frame(self.plot_frame, background=bgColor, width=100, height=100, highlightthickness=1,
                                     highlightbackground="blue")
        self.bottom_frame.pack(side="bottom", expand=True, fill="both")
        self.bottom_frame.propagate(False)

        # Settings bar
        self.settings_bar = tk.Frame(self, background=bgColor, width=100, height=100, highlightbackground=logoBarColor,
                                     highlightthickness=1)
        self.settings_bar.propagate(False)

        # # # Settings bar options
        # What stock to use
        self.stock_var = tk.StringVar(self)
        self.stock_var.set("Binance")
        self.stock = tk.OptionMenu(self.settings_bar, self.stock_var, "Binance", "CoinMarketCap")
        self.stock.config(background=bgColor, highlightthickness=0, foreground="white", highlightcolor=bgColor,
                          borderwidth=0)
        self.stock.pack(side="top")

        # Which symbol to use
        self.symbol_var = tk.StringVar(self)
        self.symbol_var.set("BTC/USDT")
        self.symbol = tk.OptionMenu(self.settings_bar, self.symbol_var, "BTC/USDT", "ETH/USDT", "DOGE/USDT",
                                    "BTC/PLN")
        self.symbol.config(background=bgColor, highlightthickness=0, foreground="white", highlightcolor=bgColor,
                           borderwidth=0)
        self.symbol.pack(side="top")

        self.run = tk.Button(self.settings_bar, text="Analyze!", background="#1DAF1A", foreground="white",
                             height=5,
                             command=self.run_analysis)
        self.run.pack(side="bottom", fill="x")

    """
    def create_subframes(self):
        self.subframes = {}
        self.frame_positions = {}
        for i in range(2):
            for j in range(2):
                frame = tk.Frame(self.tools_frame, bg='lightblue', width=225, height=200, highlightbackground="black",
                                 highlightthickness=1)
                frame.grid(row=i, column=j, padx=1, pady=1, sticky="nsew")
                self.tools_frame.grid_rowconfigure(i, weight=1)
                self.tools_frame.grid_columnconfigure(j, weight=1)

                self.subframes[(i, j)] = frame
                self.frame_positions[frame] = (i, j)
    """
    def on_start_drag(self, event):
        widget = event.widget
        self.drag_data["item"] = widget
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def on_drag_motion(self, event):
        if self.drag_data["item"]:
            x = self.winfo_pointerx() - self.winfo_rootx() - self.drag_data["x"]
            y = self.winfo_pointery() - self.winfo_rooty() - self.drag_data["y"]
            self.drag_data["item"].place(x=x, y=y)

    def on_drag_release(self, event):
        if self.drag_data["item"]:
            x = self.winfo_pointerx() - self.winfo_rootx() - self.drag_data["x"]
            y = self.winfo_pointery() - self.winfo_rooty() - self.drag_data["y"]
            for frame, (row, col) in self.frame_positions.items():
                if self.is_within_frame(x, y, frame):
                    new_widget = tk.Frame(frame, bg='yellow', width=100, height=50)
                    new_widget.pack(expand=True)
                    break
            self.drag_data["item"] = None

    def is_within_frame(self, x, y, frame):
        f_x, f_y = frame.winfo_rootx() - self.winfo_rootx(), frame.winfo_rooty() - self.winfo_rooty()
        f_width, f_height = frame.winfo_width(), frame.winfo_height()
        return f_x <= x <= f_x + f_width and f_y <= y <= f_y + f_height

    def toggle_settings_bar(self):
        toggle(self.settings_bar, "left", False, "y", 10, 10)

    """
    def analysis_action(self):
        toggle(self.analysis_tools_frame, "right", True, "both", 0, 0)
    """

    def run_analysis(self):
        stock = self.stock_var.get()
        symbol = self.symbol_var.get()
        """
        if hasattr(self, 'chart'):
            self.chart.clear_chart()
            sleep(10)
        """
        self.chart = data_processing.DataProcessing(self.plot_frame, stock, symbol)
        self.tools_frame.pack()

    def enable_trend_line(self):
        if self.cckbtn.get() == 1:
            self.chart.trend_line_enabled = True
        else:
            self.chart.trend_line_enabled = False

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


if __name__ == '__main__':
    app = App()
    app.mainloop()
