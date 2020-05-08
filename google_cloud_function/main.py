import json
import random
import time
import yfinance


def optionroulette(request):
    
	start_time = time.time()
	request_json = request.get_json(silent=True)
	request_args = request.args

	if request_json and 'stonk' in request_json:
		stonk = request_json['stonk']
	elif request_args and 'stonk' in request_args:
		stonk = request_args['stonk']
	else:
		return f"No ticker symbol supplied."

	print(stonk)
	ticker = yfinance.Ticker(stonk)

	# Grab available dates for our ticker, choose one at random.
	# * dates = list of available expiration dates
	# * expiry = random expiry date chosen from the list
	try:
		dates = ticker.options
		if len(dates) == 0:
			return f"{stonk} isn't a valid ticker, or doesn't have an option chain."
		expiry = dates[random.randint(0,len(dates)-1)]
	except IndexError:
		print(f"DEBUG: Ticker {stonk}: invalid or no options.")
		return f"{stonk} isn't a valid ticker, or may not have an option chain."

	# Flip a coin to determine calls or puts.
	# * options = dataframe of put or call options for a given ticker on a given expiry.
	# * contractType = a string to denote if the contract is a call or put.
	if random.getrandbits(1) == 0:
		options = ticker.option_chain(expiry).calls
		contractType = "C"
	else:
		options = ticker.option_chain(expiry).puts
		contractType = "P"

	# Choose a random option from the chain.
	# * rows = number of option contracts available.
	# * contract = data about the chosen option contract.
	rows = options.shape[0]
	contract = options.iloc[random.randint(1,rows)]
	
	# Put it all together.
	contractString = f"{stonk} {contract['strike']}{contractType} {expiry}"
	executionTime = time.time() - start_time

	print(f"DEBUG: contractString = {contractString}")

	# Return a JSON object.
	optionDump = {'contractString':contractString,
		'executionTime':executionTime}
	return json.dumps(optionDump)
    