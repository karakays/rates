#!/usr/bin/env python

import sys, requests, argparse

fixer_url = "http://api.fixer.io/latest"
base_key = "base"
sym_key = "symbols"

def get_rate(currency_list, amount=None):

    request_params = {}
    
    base = currency_list[0]
    request_params[base_key] = base

    symbols = currency_list[1:]

    if symbols:
        sep = ","
        sym_str = sep.join(symbols)
        request_params[sym_key] = sym_str
    
    response = requests.get(fixer_url, request_params)
    
    json = response.json()
    
    if "error" in json:
        print "rates.py: error: %s" % (json["error"])
        sys.exit(1)

    rates = json["rates"]

    targs = symbols if symbols else rates

    for t in targs:
        res = ""
        if t in rates:
            rate = float(rates[t])
            res += "{0}/{1} = {2:.3f}".format(base, t, rate)
            if amount:
                res += ". {0:.3f} {1} is {2:.3f} {3}".format(amount, base, (amount * rate), t)
        else:
            res += "{0} not available.".format(t)

        print res

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "-verbose", help="verbose output", action="store_true")
    parser.add_argument("-a", "--amount", type=float, help="amount you want to convert")
    parser.add_argument("currency", nargs="+", help="currencies")

    args = parser.parse_args()

    currency = args.currency
    amount = args.amount

    get_rate(currency, amount)

main()
