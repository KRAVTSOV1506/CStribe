import json

infura_url = {
    "rinkeby": "https://rinkeby.infura.io/v3/5d897add6bfa4dc088ff9d11bb1b8a4e",
    "mainnet": "https://mainnet.infura.io/v3/5d897add6bfa4dc088ff9d11bb1b8a4e"
}

chain_id = {
    "rinkeby": 4,
    "mainnet": 1
}

chain = "rinkeby"

config = {
    "contract_address": "0x1d747C2818bf738657b5e7f7c006F9bcBF1bbbbb",
    "ERC20_address": "0x7643fC30CDe19Cf2F76e751d32EAEC9c48849D24",
    "infura": infura_url[chain],
    "chain_id": chain_id[chain],
    "abi": json.loads(open("abi").read()),
    "ERC20_abi": json.loads(open("ERC20_abi").read()),
    "deployer": "0xaE1fB408D01D6BA250e0548b6aF8c5C5dE6fDf8D",
    "private_key": "0551378ba4646b50219f1b4376a8e2e1acadded18f481ad3b022079291071678",
    "FAPI_url": "http://localhost:8000/"
}
