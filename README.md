NOTICE: USE AT YOUR OWN RISK. The author bears no responsibility for anything.

0. Approve Token Spending on Fjord website. Otherwise script won't be able to buy anything.
1. Create a new folder, copy all project files into it.
2. Open shell in that folder and run following command:
    source init.sh
3. Create a file called "my.key" and paste your private key into it. (Metamask -> Account Details -> Show private key).
4. Obtain an Ethereum Provider API key from services like Alchemy.
5. Update "config.toml" file with your settings: fill in your Ethereum Provider API key. Set price at which you want to purchase as well as amount of weth you are willing to spent. Double check contract addresses, token decimals and their ABI.
6. Start script in shell:
    python main.py
7. Redeem your tokens on website after sale ends. You will be able to see your balance on web page as well.

NOTICE: Due to to a bug uknown for now, the price of token on web site and the price that the script fethes from smart contract differs about ~$0.3.  