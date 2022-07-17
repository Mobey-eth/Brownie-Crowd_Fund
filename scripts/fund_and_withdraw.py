from brownie import FundMe
from scripts.helpful_scripts import get_account


def fund_me():
    # To set the account variable of contract
    fund_me = FundMe[-1]
    account = get_account()
    entrance_fee = fund_me.getEntranceFee()
    print(f"The current entrance fee is {entrance_fee}")
    getPrice = fund_me.getPrice()
    print("Alleged price is ", getPrice)
    print("Funding... Please wait.")
    fund_me.Fund({"from": get_account(), "value": entrance_fee})


# 0.025000000000000000
# Alleged price is  2000000000000000000000
def main():
    fund_me()
