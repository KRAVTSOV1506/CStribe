from web3 import Web3
import web3
from config import config

w3 = Web3(Web3.HTTPProvider(config["infura"]))
contract = w3.eth.contract(address=config["contract_address"], abi=config["abi"])
ERC20 = w3.eth.contract(address=config["ERC20_address"], abi=config["ERC20_abi"])
