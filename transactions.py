import config
import time
from web3 import Web3, HTTPProvider
import web3
import json

contract_address = config.CONTRACT_ADDRESS
wallet_private_key = config.WALLET_PRIVATE_KEY
wallet_address = config.WALLET_ADDRESS

infura_url = config.INFURA_URL

w3 = Web3(HTTPProvider(infura_url))

abi_json = json.loads(open('contract_abi.json', 'r').read())

contract = w3.eth.contract(address=contract_address, abi=abi_json)


def get_height(_address: str):
    return contract.functions.getHeight(_address).call()


def add_user(_id: int, _height: int, _address: str):

    nonce = w3.eth.getTransactionCount(wallet_address)
    txn_dict = contract.functions.addUser(_id, _height, _address).buildTransaction({
        'chainId': 3,
        'gas': 200000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'nonce': nonce,
    })

    signed_txn = w3.eth.account.signTransaction(txn_dict, private_key=wallet_private_key)

    result = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

    tx_receipt = None

    count = 0
    while tx_receipt is None and (count < 30):
        try:
            time.sleep(10)

            tx_receipt = w3.eth.getTransactionReceipt(result)

            print(tx_receipt)
        except:
            tx_receipt = None
            count += 1


    if tx_receipt is None:
        return {'status': 'failed', 'error': 'timeout'}

    return {'status': 'added', 'transactionHash': tx_receipt['transactionHash'].hex()}


def get_users():
    return contract.functions.getUsers().call()