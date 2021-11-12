from os import path
import yaml


BASE_ADDRESS = "https://www.binance.com"
URL = "/en/support/announcement/c-48?navId=48"

CONFIG_PATH = 'config.yaml'

SELL_ADDRESS = "https://www.binance.com"
SELL_URL = "/en/support/announcement/c-48?navId=48"

COIN_INFO_ADDRESS = 'https://pro-api.coinmarketcap.com'
COIN_INFO_URL = '/v1/cryptocurrency/map'

STATE_PATH = 'out/'
STATE_FILE = 'state'

# no file postfix
FULL_STATE_PATH = path.abspath(path.join(STATE_PATH, STATE_FILE))


# cached config
CONFIG = dict()

def _load_config():
    global CONFIG
    try:
        with open(CONFIG_PATH, 'r') as file:
            config = yaml.safe_load(file)
        CONFIG = config
        print(CONFIG)
    except FileNotFoundError:
        # TODO: proper error print
        print('Config file does not exist.')
        exit()

print('load config into memory ... \n')
_load_config()
