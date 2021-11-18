from coininfo import get_coin_info
from settings import ( BASE_ADDRESS,
                      URL,
                      )
import re, json, time, random, requests, logging
from pathlib import Path
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


CURR_LISTINGS = dict()
NEW_LISTINGS = dict()


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
        return list()
    else:
        CURR_LISTINGS = new_state
        return diff


def main():
    # Run script level code
    import settings
    import coininfo
    import trade

    logger.info('starting client ...')

    # init state
    # TODO: this is not DRY, see below
    logger.info('setting initial list ...')
    for coin_uri in compare_and_update_state():
        try:
            logger.info(get_coin_info(coin_uri))
        except Exception as e:
            logger.warning(e)

    # run the loop
    logger.info('listening ...')
    while True:
        if new_coins := compare_and_update_state():
            logger.info('Change detected:')

            # TODO: dispatch new thread which will make the trade
            for new_coin_uri in new_coins:
                try:
                    logger.info(get_coin_info(new_coin_uri))
                except Exception as e:
                    logger.warning(e)

        # TODO: config file should dictate the time to sleep
        time.sleep(random.uniform(3, 5))


if __name__ == '__main__':
    main()
