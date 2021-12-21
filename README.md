# Heiken-Ashi-CSV
A python script that outputs Heiken Ashi candlesticks. Feel free to incorporate into your trading bot.


Dependencies:
python-binance
matplotlib
mpl_finance
astropy


Simply import the file into your project by calling: from heiken import calculateHeiken

Then call the function calculateHeiken(pair) to get the Heiken Ashi candlesticks from Binance.

Example:

calculateHeiken("BTCUSDT") -> will save csv file with heiken ashi candlesticks into the same dir as the python file.
