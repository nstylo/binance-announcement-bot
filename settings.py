from os import path
import yaml


BASE_ADDRESS = "https://www.binance.com"
URL = "/en/support/announcement/c-48?navId=48"

CONFIG_PATH = 'config.yaml'
CONFIG = None

SELL_ADDRESS = "https://www.binance.com"
SELL_URL = "/en/support/announcement/c-48?navId=48"

COIN_INFO_URL = 'https://pro-api.coinmarketcap.com'

STATE_PATH = 'out/'
STATE_FILE = 'state'

# no file postfix
FULL_STATE_PATH = path.abspath(path.join(STATE_PATH, STATE_FILE))


# cached config
CONFIG = None

def _get_config():
    try:
        with open(CONFIG_PATH, 'r') as file:
            config = yaml.safe_load(file)
        return config
    except FileNotFoundError:
        # TODO: proper error print
        print('Config file does not exist.')
        exit()
