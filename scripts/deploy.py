from brownie import FundMe, network, config, MockV3Aggregator
from scripts.helpful_scripts import (
    deploy_mocks,
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
import time


def deploy_fundme():
    account = get_account()
    # if we are on a persistent network like rinkeby,
    # use the associated address
    print(f"The active network is {network.show_active()}")
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fundme = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"))
    time.sleep(1)
    # fundme.wait(1)
    print(f"contract deployed to {fundme.address}")
    return fundme


def main():
    deploy_fundme()
