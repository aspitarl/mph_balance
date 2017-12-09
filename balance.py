#! /usr/bin/env python

# Distributed under MIT license, please see LICENSE file

import requests
import argparse
import json

parser = argparse.ArgumentParser(description="Estimate total balance of a MPH account")
parser.add_argument('-a', metavar='api_key', required=True, help='API key from account settings page')
parser.add_argument('-f', metavar='fiat_currency', default='gbp', help='Which fiat currency to display total in')
args = parser.parse_args()

symbols = {
  "adzcoin": "ADZ",
  "auroracoin": "AUR",
  "bitcoin": "BTC",
  "bitcoin-cash": "BCH",
  "bitcoin-gold": "BTG",
  "dash": "DSH",
  "digibyte": "DGB",
  "digibyte-groestl": "DGB",
  "digibyte-skein": "DGB",
  "digibyte-qubit": "DGB",
  "ethereum": "ETH",
  "ethereum-classic": "ETC",
  "expanse": "EXP",
  "feathercoin": "FTC",
  "gamecredits": "GAME",
  "geocoin": "GEO",
  "globalboosty": "BSTY",
  "groestlcoin": "GRS",
  "litecoin": "LTC",
  "maxcoin": "MAX",
  "monacoin": "MONA",
  "monero": "XMR",
  "musicoin": "MUSIC",
  "myriadcoin": "XMY",
  "myriadcoin-skein": "XMY",
  "myriadcoin-groestl": "XMY",
  "myriadcoin-yescrypt": "XMY",
  "sexcoin": "SXC",
  "siacoin": "SC",
  "startcoin": "START",
  "verge": "XVG",
  "vertcoin": "VTC",
  "zcash": "ZEC",
  "zclassic": "ZCL",
  "zcoin": "XZC",
  "zencash": "ZEN"
}

def get_value(symbol, amount, compare="btc"):
  """
    Return total value of x amount of some coin (symbol) in another coin (compare)
  """
  if symbol.upper() == "BTC" and compare.upper() == "BTC":
    return amount
  url = "https://api.cryptonator.com/api/ticker/{}-{}".format(symbol.lower(), compare)
  raw_response = requests.get(url).text
  response = json.loads(raw_response)
  price = response["ticker"]["price"]
  value = float(price) * float(amount)
  return value

def main():

  # Query the MPH API to get all current balances
  url = "https://miningpoolhub.com/index.php?page=api&action=getuserallbalances&api_key={}".format(args.a)
  raw_response = requests.get(url).text
  response = json.loads(raw_response)

  # Parse the response into a basic dictionary keyed on coin name
  coins = {}
  for coin in response["getuserallbalances"]["data"]:
    symbol = symbols[coin["coin"]]
    balance = sum([
      coin["confirmed"],
      coin["unconfirmed"],
      coin["ae_confirmed"],
      coin["ae_unconfirmed"]
     ])
    coins[symbol] = balance

  # Get the total value in BTC of all the coin balances
  btc_value = sum([get_value(coin, coins[coin]) for coin in coins])
  fiat_value = get_value("btc", btc_value, compare=args.f)

  # Print report
  print("{:f} BTC ({:.2f} {})".format(btc_value, round(fiat_value, 2), args.f))

if __name__ == "__main__":
  main()
