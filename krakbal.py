import krakenex
import argparse
from time import sleep
from requests.exceptions import ReadTimeout
from binascii import Error as KeyFileError

# CURRENCY = "ZEUR"
API_KEY = "3SYZr0HCr5P1IG22vmaskcj3wFpJk4XRy9aRYwnz2Zu/uVWaBiVgnOUR"
API_SECRET = "hDzEcXRb7JLbcXF5xOHD0HbWrSxFkLx0hr57RYtPoJh \
                mqizsofOBN4y6dXZJB6zIwpkH2a1XyaYLTDcGA215tg=="


class KrakBal:
    def __init__(self, key_file, currency):
        self.currency = currency
        self.data = {}
        self.pairlist = []
        self.total = 0.0
        self.api = self.init_api(key_file)

    def run(self):
        self.get_balances()
        self.get_rates()
        self.compute_total()
        self.print_output()

    def init_api(self, key_file):

        api = krakenex.API()
        api.load_key(key_file)
        return api
        # key=API_KEY, secret=API_SECRET)

    def get_balances(self):
        self.printstatus("Kraken: loading balance...")
        try:
            query = self.api.query_private('Balance', timeout=5)
        except Exception as e:
            self.handle_error(e)

        balances = query.get('result')
        for i in balances:
            if float(balances[i]) != 0:
                pair = i + self.currency[-len(i):]
                self.data[i] = {
                    'balance': float(balances[i]),
                    'pair': pair
                }

                if i != self.currency:
                    self.pairlist.append(pair)

    def get_rates(self):
        self.printstatus("Kraken: getting prices...")
        try:
            query = self.api.query_public(
                'Ticker',
                {'pair': ",".join(self.pairlist)},
                timeout=5
            )
        except Exception as e:
            self.handle_error(e)

        prices = query.get('result')

        for asset in self.data:
            item = self.data[asset]
            if asset == self.currency:
                item['rate'] = 1
            else:
                item['rate'] = float(prices.get(item['pair']).get('a')[0])

    def compute_total(self):
        self.total = 0
        for asset in self.data:
            item = self.data[asset]
            in_home_currency = item['balance'] * item['rate']
            item['total'] = in_home_currency
            self.total += in_home_currency

    def print_output(self):
        self.printstatus("\n============== KRAKEN BALANCE ==============\n\n")
        for asset in self.data:
            item = self.data[asset]
            print("{0:.2f} {1} \t= {2:.2f} {3} \t(@ {4})\033[K".format(
                item['balance'],
                asset[-3:],
                item['total'],
                self.currency[-3:],
                item['rate']
            ))

        print("\t\t+ =============")
        print("\t\t  {0:.2f} {1}\n".format(self.total, self.currency[-3:]))

    def printstatus(self, text, eraseline=True):
        if eraseline:
            print("\r\033[K" + text, end="")
        else:
            print("\r" + text, end="")

    def handle_error(self, error):
        if isinstance(error, ReadTimeout):
            print("ERR: Connection timed out, try again")
        elif isinstance(error, KeyFileError):
            print("ERR: Incorrectly formatted Key File")
        else:
            print("ERR:", error)

        exit()


parser = argparse.ArgumentParser(description="Prints Kraken account balance.")
parser.add_argument(
    '-c',
    metavar='currency',
    nargs=1,
    type=str,
    default='ZEUR',
    dest='currency',
    help="Optional currency symbol (default: ZEUR)"
)

parser.add_argument(
    '-k',
    metavar='key file',
    nargs=1,
    type=str,
    default='kraken.key',
    dest='key_file',
    help="Optional Key file (default: kraken.key)"
)

args = parser.parse_args()
krakbal = KrakBal(
    args.key_file[0],
    args.currency[0]
)

krakbal.run()
