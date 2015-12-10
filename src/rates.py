#!/usr/bin/env python

import sys, requests, argparse, util

fixer_url = "http://api.fixer.io/"
base_key = "base"
sym_key = "symbols"

class Rate(object):
    def __init__(self, base, target, rate, amount = None):
        self.base = base
        self.target = target
        self.rate = float(rate) if rate else None
        self.amount = amount

    def __str__(self):
        if not self.rate:
            return 'Rate %s/%s is not available.' % (self.base, self.target)

        r = "{0}/{1} = {2:.3f}".format(self.base, self.target, self.rate)

        if self.amount:
            r += ". {0:.3f} {1} is {2:.3f} {3}".format(self.amount, self.base, (self.amount * self.rate), self.target)

        return r

def get_rate(currency_list, amount=None, date=None):

    request_params = {}
    
    base = currency_list[0]
    request_params[base_key] = base

    symbols = currency_list[1:]

    if symbols:
        sep = ","
        sym_str = sep.join(symbols)
        request_params[sym_key] = sym_str
    
    url = (fixer_url + '/' + date.__str__()) if date else (fixer_url + '/latest')

    response = requests.get(url, request_params)
    
    json = response.json()
    
    if "error" in json:
        print "rates.py: error: %s" % (json["error"])
        sys.exit(1)

    rates = json["rates"]

    targs = symbols if symbols else rates

    return [Rate(base, t, rates.get(t), amount) for t in targs]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "-verbose", help="verbose output", action="store_true")
    parser.add_argument("-a", "--amount", type=float, help="amount you want to convert")
    parser.add_argument("-d", "--date", type=util.parse_date, help="rates from specified date as <yyyy-mm-dd>")    
    parser.add_argument("currency", nargs="+", help="currencies")

    args = parser.parse_args()

    currency = args.currency
    amount = args.amount
    date = args.date

    rates = get_rate(currency, amount, date)

    for r in rates: print r

if __name__ == '__main__':
    main()
