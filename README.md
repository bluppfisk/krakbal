# KrakBal
Tiny commandline script to get your Kraken balance and current value in fiat

## Installation
Make sure you have Python3 and pip installed
Run in terminal:
```
git clone https://github.com/bluppfisk/krakbal && cd krakbal
pip install -r requirements.txt
```

## Usage
1. Obtain an API key from https://www.kraken.com/u/settings/api and allow it read access to private data: balance
2. Create a **kraken.key** file and paste the API key on the first line, the secret on the second
3. Run `python3 krakbal.py` or `./krakbal.py`

## Flags
* `-c` allows you to specify a currency other than the default **EUR**, e.g. USD, GBP, CAD (see Limitations)
* `-k` allows you to specify a key file other than the default **kraken.key**

Example:

`python3 krakbal.py -c usd -k kraken.key`

## Limitations
* Kraken currently only has complete conversion data for its crypto assets into USD and EUR. For all but the biggest assets, CAD and GBP conversion is not available.