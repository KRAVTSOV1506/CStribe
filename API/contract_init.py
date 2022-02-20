from init import *
from config import *
import enum
from main import GetPaymentsLength


def LOG(message):
    with open("log", "a") as f:
        f.write(message + "\n")
    print(message)


class PaymentType(enum.Enum):
    SUBSCRIPTION = 0
    ONE_TIME_PAYMENT = 1


def createPayment(
        erc_20_address: str,
        is_native_token: bool,
        price: int,
        payment_type: PaymentType,
        trial_time: int,
        payment_period: int,
        nonce: int
):
    transaction = contract.functions.CreatePayment(
        erc_20_address,
        is_native_token,
        price,
        payment_type.value,
        trial_time,
        payment_period
    ).buildTransaction({
        'chainId': config["chain_id"],
        'gasPrice': w3.toWei('10', 'gwei'),
        'from': config["deployer"],
        'nonce': nonce
    })

    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=config["private_key"])
    send = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    LOG("createPayment " + send.hex())


def ERC20Approve(
        recipient: str,
        amount: int,
        nonce: int
):
    transaction = ERC20.functions.approve(
        recipient,
        amount,
    ).buildTransaction({
        'chainId': config["chain_id"],
        'gasPrice': w3.toWei('3', 'gwei'),
        'from': config["deployer"],
        'nonce': nonce
    })

    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=config["private_key"])
    send = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    LOG("ERC20Approve " + send.hex())


def ApprovePayment(
        eth_amount: int,
        payment_id: int,
        billing_id: int,
        nonce: int
):
    transaction = contract.functions.ApprovePayment(
        payment_id,
        billing_id
    ).buildTransaction({
        'chainId': config["chain_id"],
        'gasPrice': w3.toWei('10', 'gwei'),
        'from': config["deployer"],
        'value': eth_amount,
        'nonce': nonce
    })

    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=config["private_key"])
    send = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    LOG("ApprovePayment " + send.hex())


if __name__ == '__main__':
    nonce = w3.eth.get_transaction_count(config["deployer"])

    it = iter(range(0, 100))

    createPayment(config["ERC20_address"], False, int(Web3.toWei('1', 'ether')),
                  PaymentType.SUBSCRIPTION, 600, 1200, nonce + next(it))
    createPayment(config["ERC20_address"], False, int(Web3.toWei('1', 'ether')),
                  PaymentType.SUBSCRIPTION, 0, 1200, nonce + next(it))
    ERC20Approve(config["contract_address"], int(Web3.toWei('30', 'ether')), nonce + next(it))
    while GetPaymentsLength() < 3:
        pass
    ApprovePayment(0, 1, 1, nonce + next(it))
    ApprovePayment(0, 2, 1, nonce + next(it))
