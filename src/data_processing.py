import ccxt
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import tkinter as tk
from threading import Thread
import time


class DataProcessing:
    def __init__(self, frame, stock, symbol, timeframe="1m", limit=50, update_interval=1):
        self.frame = frame
        self.stock = stock
        self.symbol = symbol
        self.timeframe = timeframe  # Jednominutowe świece
        self.limit = limit  # Liczba świec do pobrania
        self.update_interval = update_interval  # Czas aktualizacji w sekundach

        self.binance = ccxt.binance()

        if plt.fignum_exists(1): pass

        self.fig, self.ax = plt.subplots(figsize=(10, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Uruchomienie wątku do aktualizacji wykresu
        thread = Thread(target=self.update_plot)
        thread.daemon = True
        thread.start()

    def fetch_data(self):
        ohlcv = self.binance.fetch_ohlcv(self.symbol, self.timeframe, limit=self.limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df

    # Funkcja do aktualizacji wykresu
    def update_plot(self):
        while True:
            df = self.fetch_data()
            self.ax.clear()
            self.ax.plot(df['timestamp'], df['close'], label='BTC/USD', color="#FF9900")
            self.ax.set_facecolor("#161618")
            self.ax.set_xlabel('Data')
            self.ax.set_ylabel('Cena (USD)')
            self.ax.set_title('Wykres kursu BTC/USD (Real-Time)')
            self.ax.legend()
            self.ax.grid(True)
            self.canvas.draw()
            time.sleep(1)
