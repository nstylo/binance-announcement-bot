from settings import BASE_ADDRESS
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(chrome_options=options)


def get_coin_info(uri):
    driver.get(BASE_ADDRESS + uri)
    elem = driver.find_element_by_partial_link_text('Block Explorer')
    href = elem.get_attribute('href')

    parse_result = urlparse(href)
    if parse_result.netloc == 'etherscan.io':
        return 'ethereum', parse_result.path.split('/')[2]
    elif parse_result.netloc == 'bscscan.com':
        return 'binance', parse_result.path.split('/')[2]
    else:
        raise Exception(f"{parse_result.netloc} is not yet supported.")