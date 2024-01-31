import json

import requests
import toml

from web3 import Web3
from eth_account import Account


def get_shares_price(contract, TOKEN_DECIMALS):
    return contract.functions.previewAssetsIn(TOKEN_DECIMALS).call()
    # return contract.functions.previewAssetsOut(TOKEN_DECIMALS).call()


def check_enough_eth_for_tx(user_amount):
    if user_amount <= to_wei(0.0013):  # avg fee
        print("Error: Insufficient Ether on your balance to cover tx cost")
        print(f"On balance: {from_wei(user_amount)} ETH")
        exit()


def check_enough_weth(contract, address, amount_weth_to_be_spent):
    user_weth_balance = get_weth_balance(contract, address)
    if user_weth_balance < to_wei(amount_weth_to_be_spent):
        print(f"Error: Insufficient Wrapped Ether on your balance.")
        print(f"On balance: {from_wei(user_weth_balance)} wETH. Required {amount_weth_to_be_spent} wETH")
        exit()


def get_weth_balance(contract, address):
    return contract.functions.balanceOf(address).call()


def from_wei(amount):
    return Web3.from_wei(amount, "ether")


def to_wei(amount):
    return Web3.to_wei(amount, "ether")


def connect_account(private_key):
    try:
        return Account.from_key(private_key)
    except AttributeError:
        print("Error: Supplied private key is wrong or missing")
        exit()


def connect_to_ethereum(URL):
    w3 = Web3(Web3.HTTPProvider(URL))
    if not w3.is_connected():
        print("Error: Unable to connect to the Ethereum provider.")
        exit()
    return w3


def load_contract_abi(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


def load_config():
    with open("config.toml", "r") as f:
        return toml.load(f)


def load_key(path):
    with open(path, "r") as f:
        key = f.read()
        if not key:
            print("Error: private key is missing or wrong.")
            exit()
        return key


def get_eth_price():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "ethereum",
        "vs_currencies": "usd"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "ethereum" in data and "usd" in data["ethereum"]:
        eth_price_usd = data["ethereum"]["usd"]
        return eth_price_usd

    print("Error: Unable to load Ethereum price")
    exit()
