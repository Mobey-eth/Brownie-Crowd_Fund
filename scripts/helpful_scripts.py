from brownie import accounts, config, network, MockV3Aggregator
from web3 import Web3

decimals = 18
# STARTING_PRICE = 200000000000
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]


def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        account = accounts[0]
        return account
    else:
        # account = accounts.add(os.getenv("private_key"))
        account = accounts.add(config["wallets"]["from_key"])
        return account


def deploy_mocks():
    print("deploying Mocks...")
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(
            decimals, Web3.toWei(2000, "ether"), {"from": get_account()}
        )
        print("Mocks deployed!")


def main():
    get_account()
