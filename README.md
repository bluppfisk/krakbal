# KrakBal
Tiny commandline script to get your Kraken balance and current value in fiat

## Installation
Run in terminal:
```
git clone https://github.com/bluppfisk/krakbal && cd krakbal
pip install requirements.txt
```

## Usage
1. Obtain an API key from https://www.kraken.com/u/settings/api and allow it read access to private data: balance
2. Create a **kraken.key** file and paste the API key on the first line, the secret on the second
3. Run `./krakbal.py`

## Flags
`-c` allows you to specify a currency other than Euro (in Kraken format: ZEUR, ZUSD, ...)
`-k` allows you to specify a key file other than **kraken.key**