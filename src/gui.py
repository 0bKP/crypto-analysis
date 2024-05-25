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
        self.nav_bar = tk.Frame(background=logoBarColor, height=100, highlightbackground="red", highlightthickness=1)
        self.nav_bar.pack(side="top", fill="x", padx=10, pady=10)
        self.nav_bar.pack_propagate(False)

        # # # Buttons
        self.burger_button = tk.Button(self.nav_bar, width=8, text="Burger", command=self.toggle_settings_bar)
        self.burger_button.pack(side="left", fill="y")

        self.analysis_button = tk.Button(self.nav_bar, text="Analysis", command=self.analysis_action)
        self.analysis_button.pack(side="top")

        # Main screen
        self.display_screen = tk.Frame(self, background=bgColor, width=220, highlightbackground="green",
                                       highlightthickness=1)
        self.display_screen.pack(side="right", expand=True, fill="both", padx=10, pady=10)
        self.display_screen.pack_propagate(False)

        self.plot_frame = tk.Frame(self.display_screen, background=bgColor, highlightbackground="blue", highlightthickness=1,
                                   width=100, height=100)
        self.plot_frame.pack(side="top", anchor="nw")

        # Settings bar
        self.settings_bar = tk.Frame(self, background=bgColor, width=70, height=100, highlightbackground=logoBarColor,
                                     highlightthickness=1)

        self.exit = tk.Button(self.display_screen, text='X', command=self.destroy)
        self.exit.pack(side="right")

        # Settings bar
        self.settings_bar = tk.Frame(self, background=bgColor, width=100, height=100, highlightbackground=logoBarColor,
                                     highlightthickness=1)
        self.settings_bar.propagate(False)

        # # # Options
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
        self.symbol = tk.OptionMenu(self.settings_bar, self.symbol_var, "BTC/USDT", "ETH/USDT")
        self.symbol.config(background=bgColor, highlightthickness=0, foreground="white", highlightcolor=bgColor,
                           borderwidth=0)
        self.symbol.pack(side="top")

        self.run = tk.Button(self.settings_bar, text="Analyze!", background="green", foreground="white",
                             command=lambda: self.run_analysis(self.stock_var.get(), self.symbol_var.get()))
        self.run.pack(side="bottom")

    def toggle_settings_bar(self):
        if self.settings_bar.winfo_ismapped():
            self.settings_bar.pack_forget()
        else:
            self.settings_bar.pack(side="left", fill="y", padx=10, pady=10)

    def analysis_action(self): pass

    def run_analysis(self, stock, symbol):
        data_processing.DataProcessing(self.plot_frame, stock, symbol)


if __name__ == '__main__':
    app = App()
    app.mainloop()
