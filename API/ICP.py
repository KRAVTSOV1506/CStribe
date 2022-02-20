import calendar
import datetime
import time

from init import *
from config import config
import requests


def LOG(message):
    with open("log", "a") as f:
        f.write(message + "\n")
    print(message)


def GetPayerLength() -> int:
    return requests.get(config["FAPI_url"] + "payers_length").json()["payers_length"]


def GetPayments(payment_ids: list[int]):
    params = {
        "payment_ids": list(set(payment_ids)),
    }
    return {
        x["payment_id"]: x
        for x in requests.post(config["FAPI_url"] + "payments", json=params).json()["payments"]
    }


def GetPayers(payer_ids: list[int]):
    params = {
        "payer_ids": payer_ids,
    }
    return requests.post(config["FAPI_url"] + "payers_by_payer_ids", json=params).json()["payers"]


def Now():
    current_datetime = datetime.datetime.utcnow()
    current_timetuple = current_datetime.utctimetuple()
    current_timestamp = calendar.timegm(current_timetuple)
    return current_timestamp


def GetAllowance(erc20_address: str, sender: str, recipient: str) -> int:
    ERC20 = w3.eth.contract(address=erc20_address, abi=config["ERC20_abi"])
    return ERC20.functions.allowance(sender, recipient).call()


def PayCheck(payer, payment) -> bool:
    return payment["payment_type"] == "SUBSCRIPTION" and \
           (payer["payment_status"] == "ACTIVE" and
            payer["last_payment_timestamp"] + payment["payment_period"] <= Now() or
            payer["payment_status"] == "TRIAL" and
            payer["last_payment_timestamp"] + payment["trial_time"] <=
            Now() or payer["payment_status"] == "DECLINE" and
            GetAllowance(payment["ERC20_address"], payer["billing_address"], config["contract_address"]) >=
            payment["price"])


def Execute(payment_ids: list[int], billing_ids: list[int]):
    transaction = contract.functions.ExecuteSubscriptions(
        payment_ids,
        billing_ids
    ).buildTransaction({
        'chainId': config["chain_id"],
        'gasPrice': w3.toWei('2', 'gwei'),
        'from': config["deployer"],
        'nonce': w3.eth.get_transaction_count(config["deployer"])
    })

    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=config["private_key"])
    send = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    LOG(f"ExecuteSubscription {send.hex()}\n {list(zip(payment_ids, billing_ids))}")
    return send


if __name__ == "__main__":
    while True:
        payers = GetPayers(list(range(1, GetPayerLength())))
        payment_ids = [x["payment_id"] for x in payers]
        payments = GetPayments(payment_ids)

        for_execution = []

        for p in payers:
            if PayCheck(p, payments[p["payment_id"]]):
                for_execution.append((p["payment_id"], p["billing_id"]))

        if for_execution:
            send = Execute([x[0] for x in for_execution], [x[1] for x in for_execution])
            while True:
                try:
                    result = w3.eth.getTransactionReceipt(send)
                    break
                except:
                    pass

        time.sleep(1 * 60)
