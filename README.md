# optionroulette

I never quite finished this, but provides a standalone python script and a python script which can be run as a Google Cloud Function (or likely Lambda or Azure Function with minor modification).

Idea is for the function to output a JSON object that corresponds to a randomized S&P500 or Nasdaq ticker with a valid option chain.  But, never got around to the randomization part. 

For now, it outputs a random option contract for a specified ticker.  To randomize, it likely needs to pull from a DB of ticker symbols.
