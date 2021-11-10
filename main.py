import re, yaml, json, time, random, requests
from pathlib import Path
from os import path
from bs4 import BeautifulSoup


CONFIG_PATH = 'config.yaml'
CONFIG = None

BASE_ADDRESS = "https://www.binance.com"
URL = "/en/support/announcement/c-48?navId=48"

# TODO: load this from a file, or create one if none exists
PREV_LISTINGS = dict()
# TODO: store this from a file, or create one if none exists
CURR_LISTINGS = dict()

STATE_PATH = 'out/'
STATE_FILE = 'state'

# no file postfix
FULL_PATH = path.abspath(path.join(STATE_PATH, STATE_FILE))


def store_json(state):
    Path(STATE_PATH).mkdir(parents=True, exist_ok=True)
    with open(FULL_PATH + '.json', 'w') as file:
        json.dump(state, file, indent=4)


def load_json():
    global PREV_LISTINGS
    postfixed_full_path = FULL_PATH + '.json'
    try:
        with open(postfixed_full_path, 'r') as file:
            PREV_LISTINGS = json.load(file)
    except FileNotFoundError:
        print(f"state file '{postfixed_full_path}' not found. Creating new.")
        Path(STATE_PATH).mkdir(parents=True, exist_ok=True)
        with open(postfixed_full_path, 'w') as file:
            file.write('{}')


def get_config():
    try:
        with open(CONFIG_PATH, 'r') as file:
            config = yaml.safe_load(file)
        return config
    except FileNotFoundError:
        print('Config file does not exist.')
        exit()


def extract_state(doc):
    soup = BeautifulSoup(doc.content, 'html.parser')

    listings = soup.findAll('a', text=re.compile("Binance Will List"))

    state = dict()
    for listing in listings:
        state[listing['href']] = {
            'text': listing.contents[0],
            'coin_name': re.compile('\((.*)\)').search(listing.text).group(1),
        }

    return state


def diff(a, b):
    return list(set(a) - set(b))


def run():
    global PREV_LISTINGS

    doc = requests.get(BASE_ADDRESS + URL)
    new_state = extract_state(doc)
    diff_ = diff(new_state, PREV_LISTINGS)

    if len(diff_) == 0:
        pass
    else:
        print('Change detected:')
        # TODO: write to a log file
        print(diff_)
        PREV_LISTINGS = new_state
        store_json(new_state)


def main():
    print('starting client ...')

    print('load config ...')
    CONFIG = get_config()

    # init state
    print('setting initial list ...')
    load_json()

    # run the loop
    print('listening ...')
    while True:
        run()
        time.sleep(random.uniform(3, 5))


if __name__ == '__main__':
    main()
