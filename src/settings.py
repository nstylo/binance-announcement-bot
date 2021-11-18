import yaml, logging


BASE_ADDRESS = "https://www.binance.com"
URL = "/en/support/announcement/c-48?navId=48"

CONFIG_PATH = 'config.yaml'

#  SELL_ADDRESS = "https://www.binance.com"
#  SELL_URL = "/en/support/announcement/c-48?navId=48"

# cached config
CONFIG = dict()


# setup logging
class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    _format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + _format + reset,
        logging.INFO: grey + _format + reset,
        logging.WARNING: yellow + _format + reset,
        logging.ERROR: red + _format + reset,
        logging.CRITICAL: bold_red + _format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

sh = logging.StreamHandler()
sh.setLevel(logging.INFO)

sh.setFormatter(CustomFormatter())

logging.basicConfig(level=logging.INFO,
                    handlers=(sh,)
                    )


logger.info('load config into memory ...')
try:
    with open(CONFIG_PATH, 'r') as file:
        config = yaml.safe_load(file)
    CONFIG = config
except FileNotFoundError:
    logger.critical('config file does not exist.')
    exit(1)
