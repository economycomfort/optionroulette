#!/usr/bin/env python
#
import json
import sys
import time
import random
import yfinance as yf

start_time = time.time()

# Take ticker symbol from the first supplied argument.
try:
    stonk = sys.argv[1].upper()
except:
    print("No valid ticker supplied.")
    exit(1)

# YFinance data object
ticker = yf.Ticker(stonk)

# Grab available option expiry dates for ticker
try:
    dates = ticker.options      # Grab the exp dates
    if len(dates) == 0:
        print(f"Ticker {stonk} doesn't appear to have an option chain.")
        exit(1)
    expiry = dates[random.randint(0,len(dates)-1)]    # Choose one at random
# An IndexError may appear if a stock doesn't have an options chain, or is a
# bogus ticker.
except IndexError:
    print(f"{stonk} isn't a valid ticker, or may not have an option chain.")
    exit(1)

# Flip a coin to grabs puts or calls for a given ticker on a given expiry.
if random.getrandbits(1) == 0:
    options = ticker.option_chain(expiry).calls
    contractType = "C"
else:
    options = ticker.option_chain(expiry).puts
    contractType = "P"

# Break apart the option chain data and choose a random option.
# * DataFrame shape describes numbers of columns and rows in the object.
# * List item 0 = rows
# * List item 1 = columns (unused here)
rows = options.shape[0]
contract = options.iloc[random.randint(1,rows)]

# Get data about our contract.
# Output of contract is structured like:
#   contractSymbol       TSLA201218P00685000
#   lastTradeDate        2020-05-01 19:17:37
#   strike                               685
#   lastPrice                         149.85
#   bid                               118.35
#   ask                                119.9
#   change                                 0
#   percentChange                          0
#   volume                                 5
#   openInterest                           6
#   impliedVolatility               0.726077
#   inTheMoney                         False
#   contractSize                     REGULAR
#   currency                             USD


# Put it all together.
contractString = f"{stonk} {contract['strike']}{contractType} {expiry}"
executionTime = time.time() - start_time

print(f"DEBUG: contractString = {contractString}")
print(f"DEBUG: executionTime = {executionTime}")

# Return a JSON object.
optionDump = {'contractString':contractString,
    'executionTime':executionTime}
print(json.dumps(optionDump))
