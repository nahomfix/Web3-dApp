import base64
import json

from algosdk import account, constants, mnemonic
from algosdk.future import transaction
from algosdk.v2client import algod


def generate_algorand_keypair():
    private_key, address = account.generate_account()
    passphrase = mnemonic.from_private_key(private_key)
    print("My address: {}".format(address))
    print("My private key: {}".format(private_key))
    print("My passphrase: {}".format(mnemonic.from_private_key(private_key)))

    return private_key, address, passphrase


def check_balance(my_address):
    algod_address = "http://localhost:4001"
    algod_token = (
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    )
    algod_client = algod.AlgodClient(algod_token, algod_address)

    print("My address: {}".format(my_address))
    account_info = algod_client.account_info(my_address)
    print("Account balance: {} microAlgos".format(account_info.get("amount")))

    return account_info.get("amount")
