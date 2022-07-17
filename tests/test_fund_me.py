import pytest
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from scripts.deploy import deploy_fundme
from brownie import accounts, network, exceptions
import time


def test_can_fund_and_withdraw():
    # Arrange
    account = get_account()
    fund_me = deploy_fundme()
    entrance_fee = fund_me.getEntranceFee() + 100
    # Act
    tx = fund_me.Fund({"from": account, "value": entrance_fee})
    time.sleep(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    # Act
    tx2 = fund_me.withdraw({"from": account})
    time.sleep(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local Networks")
    fk_account = accounts[2]
    fund_me = deploy_fundme()
    with pytest.raises(exceptions.VirtualMachineError):
        texx = fund_me.withdraw({"from": fk_account})
