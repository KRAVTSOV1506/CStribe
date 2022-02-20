import json
import enum
from init import *
from bottle import route, request, run, template # $ pip install bottle


class PaymentType(enum.Enum):
    SUBSCRIPTION = 0
    ONE_TIME_PAYMENT = 1


class PaymentStatus(enum.Enum):
    CREATED = 0
    TRIAL = 1
    ACTIVE = 2
    CANCELED = 3
    DECLINE = 4


class EnumEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, PaymentType) or isinstance(obj, PaymentStatus):
            return str(obj).split(".")[-1]
        return json.JSONEncoder.default(self, obj)


class Payment:
    def __init__(self, *args):
        it = iter(args)
        self.service_provider_address: str = next(it)
        self.ERC20_address: str = next(it)
        self.is_native_token: bool = next(it)
        self.price: int = next(it)
        self.payment_type: PaymentType = PaymentType(next(it))
        self.creation_timestamp: int = next(it)
        self.trial_time: int = next(it)
        self.payment_period: int = next(it)
        self.payment_id: int = next(it)
        self.is_active: bool = next(it)

    def __str__(self):
        return "\n".join([f"{k} : {v}" for k, v in self.__dict__.items()])

    def toJSON(self):
        return json.dumps(self.__dict__, cls=EnumEncoder)


class Payer:
    def __init__(self, *args):
        it = iter(args)
        self.payment_id: int = next(it)
        self.billing_address: str = next(it)
        self.billing_id: int = next(it)
        self.creation_timestamp: int = next(it)
        self.last_payment_timestamp: int = next(it)
        self.payment_status: PaymentStatus = PaymentStatus(next(it))
        self.payer_id: int = next(it)

    def __str__(self):
        return "\n".join([f"{k} : {v}" for k, v in self.__dict__.items()])

    def toJSON(self):
        return json.dumps(self.__dict__, cls=EnumEncoder)


def GetPayment(payment_id: int) -> Payment:
    return Payment(*contract.functions.GetPayment(payment_id).call())


def GetPaymentsLength() -> int:
    return contract.functions.GetPaymentsLength().call()


def GetPayersLength() -> int:
    return contract.functions.GetPayersLength().call()


def GetPayments(payment_ids: list[int]) -> list[Payment]:
    return [Payment(*x) for x in contract.functions.GetPayments(payment_ids).call()]


def GetPayer(payment_id: int, billing_id: int) -> Payer:
    return Payer(*contract.functions.GetPayer(payment_id, billing_id).call())


def GetPayers(payments_ids: list[int], billing_ids: list[int]) -> list[Payer]:
    return [Payer(*x) for x in contract.functions.GetPayers(payments_ids, billing_ids).call()]


def GetPayerByPayerId(payer_id: int) -> Payer:
    return Payer(*contract.functions.GetPayerByPayerId(payer_id).call())


def GetPayersByPayersIds(payer_ids: list[int]) -> list[Payer]:
    return [Payer(*x) for x in contract.functions.GetPayersByPayersIds(payer_ids).call()]


def GetPayerStatus(payment_id: int, billing_id: int) -> PaymentStatus:
    return PaymentStatus(contract.functions.GetPayerStatus(payment_id, billing_id).call())


@route('/payment')
def payment():
    return GetPayment(int(request.query.payment_id)).toJSON()


@route('/payers_length')
def payment():
    return json.dumps({
        "payers_length": GetPayersLength()
    })


@route('/payments', method="POST")
def payment():
    data = request.json
    return json.dumps({
        "payments": [x.__dict__ for x in GetPayments(data["payment_ids"])]
    }, cls=EnumEncoder)


@route('/payer')
def payer():
    return GetPayer(int(request.query.payment_id), int(request.query.billing_id)).toJSON()


@route('/payers', method='POST')
def payers():
    data = request.json
    return json.dumps({
        "payers": [x.__dict__ for x in GetPayers(data["payment_ids"], data["billing_ids"])]
    }, cls=EnumEncoder)


@route('/payer_by_payer_id')
def payer():
    return GetPayerByPayerId(int(request.query.payer_id)).toJSON()


@route('/payers_by_payer_ids', method='POST')
def payers():
    data = request.json
    return json.dumps({
        "payers": [x.__dict__ for x in GetPayersByPayersIds(data["payer_ids"])]
    }, cls=EnumEncoder)


@route('/payer_status')
def payerStatus():
    return json.dumps(
        {"payer_status": GetPayerStatus(int(request.query.payment_id), int(request.query.billing_id))}
    , cls=EnumEncoder)


if __name__ == '__main__':
    run(host='localhost', port=8000, debug=True)
