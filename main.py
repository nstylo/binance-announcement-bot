import re, json, time, random, requests
from pathlib import Path
from bs4 import BeautifulSoup
from settings import ( STATE_PATH,
                      FULL_STATE_PATH,
                      BASE_ADDRESS,
                      URL,
                      )


CURR_LISTINGS = dict()
NEW_LISTINGS = dict()


def _store_json(state):
    """
    serialize state and save to json file.
    """
    Path(STATE_PATH).mkdir(parents=True, exist_ok=True)
    with open(FULL_STATE_PATH + '.json', 'w') as file:
        json.dump(state, file, indent=4)


def load_json():
    """
    This function loads the state from file into memory.
    If file does not exist, this function will create a
    new one.
    """
    global CURR_LISTINGS

    postfixed_full_path = FULL_STATE_PATH + '.json'
    try:
        with open(postfixed_full_path, 'r') as file:
            CURR_LISTINGS = json.load(file)
    except FileNotFoundError:
        print(f"state file '{postfixed_full_path}' not found. Creating new.")
        Path(STATE_PATH).mkdir(parents=True, exist_ok=True)
        with open(postfixed_full_path, 'w') as file:
            file.write('{}')


def _extract_state(doc):
    """
    Gets the raw HTML, parses it, finds all current listings
    from the first page of the Binance announcement page and
    serializes them.
    """
    soup = BeautifulSoup(doc.content, 'html.parser')

    listings = soup.findAll('a', text=re.compile("Binance Will List"))

    state = dict()
    for listing in listings:
        state[listing['href']] = {
            'text': listing.contents[0],
            'symbol': re.compile('\((.*)\)').search(listing.text).group(1),
        }

    return state


def _diff_state(A, B):
    """
    returns a sub-list of A, those items which are NOT in B.
    """
    return list(set(A) - set(B))


def compare_and_update_state():
    """
    Compare current with new state and updates
    with new state if they differ.
    """
    global CURR_LISTINGS

    doc = requests.get(BASE_ADDRESS + URL)
    new_state = _extract_state(doc)
    diff = _diff_state(new_state, CURR_LISTINGS)

    if len(diff) == 0:
        pass
    else:
        CURR_LISTINGS = new_state
        _store_json(new_state)
        return diff


def main():
    # Run script level functions
    import settings
    import coininfo

    print('starting client ...')

    # init state
    print('setting initial list ...')
    load_json()

    # run the loop
    print('listening ...')
    while True:
        if diff := compare_and_update_state():
            print('Change detected:')
            print(diff)
        time.sleep(random.uniform(3, 5))


if __name__ == '__main__':
    main()
