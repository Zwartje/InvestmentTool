import pandas as pd
import scipy as scipy
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

SP = yf.Ticker("GSPC")
VIX = yf.Ticker("LVO.MI")

Price = VIX.history(period="max")
Delta = Price / Price.shift(3) - 1
AA = Delta.Close > 0.1
# plt.hist(Delta.Close)
plt.plot(AA)
plt.show()

