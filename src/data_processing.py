import ccxt
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import tkinter as tk
from threading import Thread
import time

plot_text_color = "#BCBCBC"


class DataProcessing:
    @staticmethod
    def trend_line(state):
        if state == 1:
            print("Trend line")
        elif state == 0:
            print("No trend line:(")

    def __init__(self, frame, stock, symbol, timeframe="1m", limit=20, update_interval=1):
        self.frame = frame
        self.stock = stock
        self.symbol = symbol
        self.timeframe = timeframe  # Jednominutowe świece
        self.limit = limit  # Liczba świec do pobrania
        self.update_interval = update_interval  # Czas aktualizacji w sekundach
        self.today = datetime.today().strftime('%Y-%m-%d')

        self.binance = ccxt.binance()

        self.fig, self.ax = plt.subplots(figsize=(10, 5))
        self.fig.patch.set_facecolor("#161618")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Uruchomienie wątku do aktualizacji wykresu
        self.running = True
        self.thread = Thread(target=self.update_plot)
        self.thread.daemon = True
        self.thread.start()

    def fetch_data(self):
        ohlcv = self.binance.fetch_ohlcv(self.symbol, self.timeframe, limit=self.limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['timestamp'] = df['timestamp'].dt.tz_localize('UTC').dt.tz_convert('Europe/Warsaw')
        return df

    # Funkcja do aktualizacji wykresu
    def update_plot(self):
        while self.running:
            df = self.fetch_data()
            self.ax.clear()
            self.ax.tick_params(axis='x', colors=plot_text_color)
            self.ax.tick_params(axis='y', colors=plot_text_color)
            self.ax.set_xlabel(self.today, color=plot_text_color)
            #self.ax.set_ylabel('Cena (USD)', color=plot_text_color)
            self.ax.set_facecolor("#161618")
            self.ax.set_title(self.symbol, color=plot_text_color)
            self.ax.grid(True, color="#262629")
            self.ax.plot(df['timestamp'], df['close'], color="#FF9900")
            self.canvas.draw()
            time.sleep(self.update_interval)

    def clear_chart(self):
        self.running = False
        self.thread.join()
        self.canvas.get_tk_widget().destroy()
        self.canvas.figure.clear()

