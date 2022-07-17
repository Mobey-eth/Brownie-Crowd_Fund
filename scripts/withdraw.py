from brownie import FundMe
from scripts.helpful_scripts import get_account


def withdraw():
    print("Processing Withdrawal")
    account = get_account()
    FundMe[-1].withdraw({"from": account})
    print("Withdrawal complete")


def main():
    withdraw()
