import tkinter as tk
import data_processing

bgColor = "#161618"
logoBarColor = "#FF9900"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1440x1024+250+20")
        self.configure(bg=bgColor)
        #self.overrideredirect(True)
        self.resizable(False, False)

        # Nav bar
        self.nav_bar = tk.Frame(background=logoBarColor, height=100)
        self.nav_bar.pack(side="top", fill="x", padx=10, pady=10)
        self.nav_bar.pack_propagate(False)

        # # # Nav bar buttons
        self.burger_button = tk.Button(self.nav_bar, width=8, text="Burger", command=self.toggle_settings_bar)
        self.burger_button.pack(side="left", fill="y")

        self.analysis_button = tk.Button(self.nav_bar, text="Analysis", command=self.analysis_action)
        self.analysis_button.pack(side="top")

        # Main screen
        self.display_screen = tk.Frame(self, background=bgColor, width=220)
        self.display_screen.pack(side="right", expand=True, fill="both", padx=10, pady=10)
        self.display_screen.pack_propagate(False)

        # # # Plot
        self.plot_frame = tk.Frame(self.display_screen, background=bgColor, width=100, height=100)
        self.plot_frame.pack(side="left", anchor="nw")

        # # # Analysis tools frame
        self.analysis_tools_frame = tk.Frame(self.display_screen, background=bgColor, width=100, height=100,
                                             highlightthickness=1, highlightbackground="pink")
        self.analysis_tools_frame.propagate(False)

        self.analysis_label = tk.Label(self.analysis_tools_frame, text="Analysis")
        self.analysis_label.pack(side="top", fill="x")

        self.cckbtn = tk.IntVar()
        self.trend_line = tk.Checkbutton(self.analysis_tools_frame, text="Trend line", variable=self.cckbtn,
                                         onvalue=1, offvalue=0,
                                         command=lambda: data_processing.DataProcessing.trend_line(self.cckbtn.get()))
        self.trend_line.pack(side="right", padx=10, pady=10)


        # # # Another frame idk what for yet
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
                             command=lambda: self.run_analysis(self.stock_var.get(), self.symbol_var.get()))
        self.run.pack(side="bottom", fill="x")

    def toggle(self, element, side, expand=False, fill=None, padx=0, pady=0):
        if element.winfo_ismapped():
            element.pack_forget()
        else:
            element.pack(side=side, expand=expand, fill=fill, padx=padx, pady=pady)

    def toggle_settings_bar(self):
        self.toggle(self.settings_bar, "left", False, "y", 10, 10)

    def analysis_action(self):
        self.toggle(self.analysis_tools_frame, "right", True, "both", 0, 0)

    def run_analysis(self, stock, symbol):
        if not hasattr(self, 'chart'):
            self.chart = data_processing.DataProcessing(self.plot_frame, stock, symbol)
        else:
            self.chart.clear_chart()
            self.chart = data_processing.DataProcessing(self.plot_frame, stock, symbol)


if __name__ == '__main__':
    app = App()
    app.mainloop()
