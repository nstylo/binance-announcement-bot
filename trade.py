from web3 import Web3
import json
from datetime import datetime, timedelta

from web3.types import TxParams, Wei
from settings import CONFIG
import logging

logger = logging.getLogger(__name__)


# In dev environment we get account and private key from
# our forked mainnet. In prod we have to get them from the
# config file.
if not CONFIG['PROD']:
    with open('chain/keys.json') as file:
        deserialized_file = json.load(file)
        # We only consider one account (the first one)
        WALLET_ADDR = list(deserialized_file['addresses'])[0]
        PRIVATE_KEY = deserialized_file['private_keys'][WALLET_ADDR]
else:
    WALLET_ADDR = CONFIG['WALLET_ADDR']
    PRIVATE_KEY = CONFIG['WALLET_PRIVATE_KEY']

WALLET_ADDR = Web3.toChecksumAddress(WALLET_ADDR)
WEB3_HTTP_PROVIDER = CONFIG['WEB3_HTTP_URL']
WETH_ADDR = Web3.toChecksumAddress('0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2')
UNISWAP_ROUTER_ADDR = Web3.toChecksumAddress('0xE592427A0AEce92De3Edee1F18E0157C05861564')


w3 = Web3(Web3.HTTPProvider(WEB3_HTTP_PROVIDER))
if not w3.isConnected():
    logger.critical(f"Could not connect to {WEB3_HTTP_PROVIDER}.")
    exit(1)
else:
    logger.info(f"Successfully conntected to {WEB3_HTTP_PROVIDER}.")



# TODO: error handling
# TODO: asyncronousity (after sending tx, return when and if tx was successful/failing)
def dev_eth_to_weth(eth_amount):
    with open('./abi/weth_abi.json') as abi:
        weth_contract = w3.eth.contract(address=WETH_ADDR, abi=json.load(abi))

    params = {
        'from': WALLET_ADDR,
        'value': Web3.toWei(eth_amount, 'ether')
    }

    tx = weth_contract.functions.deposit().buildTransaction(params)

    nonce = w3.eth.get_transaction_count(WALLET_ADDR)
    tx.update({ 'nonce': nonce })

    signed_tx = w3.eth.account.sign_transaction(
        tx,
        PRIVATE_KEY
    )
    w3.eth.send_raw_transaction(signed_tx.rawTransaction)


# TODO: error handling
# TODO: asyncronousity (after sending tx, return when and if tx was successful/failing)
def dev_weth_to_eth():
    with open('./abi/weth_abi.json') as abi:
        weth_contract = w3.eth.contract(address=WETH_ADDR, abi=json.load(abi))

    weth_balance = weth_contract.functions.balanceOf(WALLET_ADDR).call()

    tx = weth_contract.functions.withdraw(
        wad=weth_balance,
    ).buildTransaction({ 'from': WALLET_ADDR })

    nonce = w3.eth.get_transaction_count(WALLET_ADDR)
    tx.update({ 'nonce': nonce })

    signed_tx = w3.eth.account.sign_transaction(
        tx,
        PRIVATE_KEY
    )

    w3.eth.send_raw_transaction(signed_tx.rawTransaction)


def swap(coin_in_addr, coin_out_addr, amount):
    with open('./abi/uniswap_router_abi.json') as abi:
        router_instance = w3.eth.contract(address=UNISWAP_ROUTER_ADDR, abi=json.load(abi))

    params = {
        'tokenIn': coin_in_addr,
        'tokenOut': coin_out_addr,
        'fee': 3000,
        'recipient': WALLET_ADDR,
        'deadline': int((datetime.now() + timedelta(seconds=20)).timestamp()),
        'amountIn': amount,
        'amountOutMinimum': 0,
        'sqrtPriceLimitX96': 0,
    }

    tx_params: TxParams = {
        'from': WALLET_ADDR,
        'value': amount,
        'nonce': w3.eth.get_transaction_count(WALLET_ADDR)
    }

    # TODO: estimate gas before sending tx

    tx = router_instance.functions.exactInputSingle(
        params
    ).buildTransaction(
        tx_params
    )

    signed_tx = w3.eth.account.sign_transaction(
        tx,
        PRIVATE_KEY
    )
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    logger.info(receipt['status'])


def invoke_trade(coin_info):
    if coin_info[0] == 'ethereum':
        logger.info('trading ...')
        swap(WETH_ADDR, Web3.toChecksumAddress(coin_info[1]), Web3.toWei(10, 'ether'))


if not CONFIG['PROD']:
    dev_eth_to_weth(5)

