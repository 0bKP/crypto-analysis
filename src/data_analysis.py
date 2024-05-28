import numpy as np


def trend_line(ax, df):
    x = np.arange(len(df['timestamp']))
    y = df['close']
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    ax.plot(df['timestamp'], p(x), color="blue")