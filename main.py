from datetime import datetime
import json
import time

from utils import (
    get_eth_price,
    load_config,
    load_contract_abi,
    load_key,
    connect_account,
    connect_to_ethereum,
    to_wei,
    from_wei,
    check_enough_eth_for_tx,
    check_enough_weth,
    get_weth_balance,
    get_shares_price,
)


def main():
    config = load_config()

    ETH_PROVIDER_URL = config["URI"]["ETH_PROVIDER_URL"]
    CONTRACT_ADDRESS = config["URI"]["CONTRACT_ADDRESS"]
    WETH_ADDRESS = config["URI"]["WETH_ADDRESS"]
    PRIVATE_KEY = load_key(config["KEY"]["PRIVATE_KEY_PATH"])
    PRICE = config["PARAMS"]["PRICE"]
    AMOUNT_OF_wETHER_TO_BE_SPENT = config["PARAMS"]["AMOUNT_OF_wETHER_TO_BE_SPENT"]
    VEC_ABI = load_contract_abi(config["URI"]["VEC_ABI"])
    WETH_ABI = load_contract_abi(config["URI"]["WETH_ABI"])
    SLEEP_INTERVAL = config["SETTINGS"]["SLEEP_INTERVAL"]
    TOKEN_DECIMALS = config["URI"]["TOKEN_DECIMALS"]

    w3 = connect_to_ethereum(ETH_PROVIDER_URL)
    account = connect_account(PRIVATE_KEY)
    w3.eth.default_account = account.address
    vec_contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=VEC_ABI)
    weth_contract = w3.eth.contract(address=WETH_ADDRESS, abi=WETH_ABI)

    user_balance_eth = w3.eth.get_balance(account.address)
    check_enough_eth_for_tx(user_balance_eth)
    user_balance_weth = get_weth_balance(weth_contract, account.address)
    check_enough_weth(weth_contract, account.address, AMOUNT_OF_wETHER_TO_BE_SPENT)

    print(f"Your address:      {account.address}")
    print(f"Contract address:  {CONTRACT_ADDRESS}")
    print(f"Balance eth:       {from_wei(user_balance_eth)}")
    print(f"Balance weth:      {from_wei(user_balance_weth)}")
    print(f"Spending set:      {round(AMOUNT_OF_wETHER_TO_BE_SPENT, 6)} Wrapped Ether")
    print(f"Buy Price:         ${PRICE}")

    print()
    while input("🚨 Do You Want To Continue? [y/n] 🚨 ") != "y":
        print("Aborted by user.")
        exit()

    def calculate():
        eth_price = get_eth_price()
        amount_to_be_spent_in_usd = eth_price * AMOUNT_OF_wETHER_TO_BE_SPENT
        estimated_shares_to_buy = amount_to_be_spent_in_usd / PRICE
        shares_price = get_shares_price(vec_contract, TOKEN_DECIMALS)
        current_price = round(float(from_wei(shares_price)) * eth_price, 2)

        return amount_to_be_spent_in_usd, estimated_shares_to_buy, shares_price, current_price

    while True:
        amount_to_be_spent_in_usd, estimated_shares_to_buy, shares_price, current_price = calculate()

        if current_price > PRICE:
            print()
            print(datetime.now())
            print(f"Current price is ${current_price}. Target price is ${PRICE}.")
            print(f"Sleeping {SLEEP_INTERVAL} seconds....")
            time.sleep(SLEEP_INTERVAL)
        else:
            print()
            print(datetime.now())
            print(f"🚨 Current price is ${current_price}. Target price is ${PRICE}.")
            print(f"🚨 Attempting to buy {estimated_shares_to_buy} VEC")

            assets_in = to_wei(AMOUNT_OF_wETHER_TO_BE_SPENT)
            min_shares_out = int(estimated_shares_to_buy * TOKEN_DECIMALS * 0.98)  # decreasing the number of shares to buy
                                                                                   # by some % just to make sure tx is successful
            tx = vec_contract.functions.swapExactAssetsForShares(assets_in, min_shares_out, account.address).build_transaction({
                "chainId": w3.eth.chain_id,
                "from": account.address,
                "nonce": w3.eth.get_transaction_count(account.address),
            })

            signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
            tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            
            print("TX hash:")
            w3.eth.wait_for_transaction_receipt(tx_hash)

            print()
            print("Purchase complete. Check your transaction and check your account balance")
            print("🚨 Don't forget to redeem you tokens on web page 🚨")

            exit(0)

if __name__ == "__main__":
    main()
