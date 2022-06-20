import base64
import json

from algosdk import account, mnemonic
from algosdk.future.transaction import *
from algosdk.future.transaction import AssetConfigTxn, AssetTransferTxn
from algosdk.v2client import algod

# Shown for demonstration purposes. NEVER reveal secret mnemonics in practice.
# Change these values with your mnemonics
mnemonic1 = "PASTE your phrase for account 1"
mnemonic2 = "PASTE your phrase for account 2"
# never use mnemonics in production code, replace for demo purposes only

# For ease of reference, add account public and private keys to
# an accounts dict.
def generate_dict(owner_mnemonic, receiver_mnemonic):
    accounts = {}
    counter = 1
    for m in [owner_mnemonic, receiver_mnemonic]:
        accounts[counter] = {}
        accounts[counter]["pk"] = mnemonic.to_public_key(m)
        accounts[counter]["sk"] = mnemonic.to_private_key(m)
        counter += 1

    return accounts


algod_address = "http://localhost:4001"
algod_token = (
    "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
)

# Initialize an algod client
algod_client = algod.AlgodClient(
    algod_token=algod_token, algod_address=algod_address
)


#   Utility function used to print created asset for account and assetid
def print_created_asset(algodclient, account, assetid):
    # note: if you have an indexer instance available it is easier to just use this
    # response = myindexer.accounts(asset_id = assetid)
    # then use 'account_info['created-assets'][0] to get info on the created asset
    account_info = algodclient.account_info(account)
    idx = 0
    for my_account_info in account_info["created-assets"]:
        scrutinized_asset = account_info["created-assets"][idx]
        idx = idx + 1
        if scrutinized_asset["index"] == assetid:
            print("Asset ID: {}".format(scrutinized_asset["index"]))
            print(json.dumps(my_account_info["params"], indent=4))
            break


#   Utility function used to print asset holding for account and assetid
def print_asset_holding(algodclient, account, assetid):
    # note: if you have an indexer instance available it is easier to just use this
    # response = myindexer.accounts(asset_id = assetid)
    # then loop thru the accounts returned and match the account you are looking for
    account_info = algodclient.account_info(account)
    idx = 0
    for my_account_info in account_info["assets"]:
        scrutinized_asset = account_info["assets"][idx]
        idx = idx + 1
        if scrutinized_asset["asset-id"] == assetid:
            print("Asset ID: {}".format(scrutinized_asset["asset-id"]))
            print(json.dumps(scrutinized_asset, indent=4))
            break


# CREATE ASSET
def create_asset(owner_address, file_path):
    # Get network params for transactions before every transaction.
    params = algod_client.suggested_params()

    accounts = generate_dict()

    txn = AssetConfigTxn(
        sender=accounts[1]["pk"],
        sp=params,
        total=1,
        default_frozen=False,
        unit_name="Certificate",
        asset_name="Certificate",
        manager=accounts[1]["pk"],
        reserve=accounts[1]["pk"],
        freeze=accounts[1]["pk"],
        clawback=accounts[1]["pk"],
        url=file_path,
        decimals=0,
    )
    # Sign with secret key of creator
    stxn = txn.sign(accounts[1]["sk"])

    # Send the transaction to the network and retrieve the txid.
    try:
        txid = algod_client.send_transaction(stxn)
        print("Signed transaction with txID: {}".format(txid))
        # Wait for the transaction to be confirmed
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
        print("TXID: ", txid)
        print(
            "Result confirmed in round: {}".format(
                confirmed_txn["confirmed-round"]
            )
        )

    except Exception as err:
        print(err)
    # Retrieve the asset ID of the newly created asset by first
    # ensuring that the creation transaction was confirmed,
    # then grabbing the asset id from the transaction.

    print(
        "Transaction information: {}".format(
            json.dumps(confirmed_txn, indent=4)
        )
    )
    # print("Decoded note: {}".format(base64.b64decode(
    #     confirmed_txn["txn"]["txn"]["note"]).decode()))

    try:
        # Pull account info for the creator
        # account_info = algod_client.account_info(accounts[1]['pk'])
        # get asset_id from tx
        # Get the new asset's information from the creator account
        ptx = algod_client.pending_transaction_info(txid)
        asset_id = ptx["asset-index"]
        print_created_asset(algod_client, accounts[1]["pk"], asset_id)
        print_asset_holding(algod_client, accounts[1]["pk"], asset_id)
    except Exception as e:
        print(e)


# OPT-IN
def opt_in_asset(asset_id):
    params = algod_client.suggested_params()
    # comment these two lines if you want to use suggested params
    # params.fee = 1000
    # params.flat_fee = True

    accounts = generate_dict()

    account_info = algod_client.account_info(accounts[3]["pk"])
    holding = None
    idx = 0
    for my_account_info in account_info["assets"]:
        scrutinized_asset = account_info["assets"][idx]
        idx = idx + 1
        if scrutinized_asset["asset-id"] == asset_id:
            holding = True
            break

    if not holding:

        # Use the AssetTransferTxn class to transfer assets and opt-in
        txn = AssetTransferTxn(
            sender=accounts[3]["pk"],
            sp=params,
            receiver=accounts[3]["pk"],
            amt=0,
            index=asset_id,
        )
        stxn = txn.sign(accounts[3]["sk"])
        # Send the transaction to the network and retrieve the txid.
        try:
            txid = algod_client.send_transaction(stxn)
            print("Signed transaction with txID: {}".format(txid))
            # Wait for the transaction to be confirmed
            confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
            print("TXID: ", txid)
            print(
                "Result confirmed in round: {}".format(
                    confirmed_txn["confirmed-round"]
                )
            )

        except Exception as err:
            print(err)
        # Now check the asset holding for that account.
        # This should now show a holding with a balance of 0.
        print_asset_holding(algod_client, accounts[3]["pk"], asset_id)


# TRANSFER ASSET
def transfer_asset(asset_id):
    # transfer asset of 10 from account 1 to account 3
    params = algod_client.suggested_params()
    # comment these two lines if you want to use suggested params
    # params.fee = 1000
    # params.flat_fee = True

    accounts = generate_dict()

    txn = AssetTransferTxn(
        sender=accounts[1]["pk"],
        sp=params,
        receiver=accounts[2]["pk"],
        amt=1,
        index=asset_id,
    )
    stxn = txn.sign(accounts[1]["sk"])
    # Send the transaction to the network and retrieve the txid.
    try:
        txid = algod_client.send_transaction(stxn)
        print("Signed transaction with txID: {}".format(txid))
        # Wait for the transaction to be confirmed
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
        print("TXID: ", txid)
        print(
            "Result confirmed in round: {}".format(
                confirmed_txn["confirmed-round"]
            )
        )

    except Exception as err:
        print(err)

    # The balance should now be 10.
    print_asset_holding(algod_client, accounts[2]["pk"], asset_id)
