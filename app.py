from flask import Flask, request, jsonify
from eth_account import Account
from web3 import Web3

app = Flask(__name__)

# Dummy storage simpan private keys (ingat: ini contoh, jangan simpan private key di production seperti ini)
wallets = {}

@app.route('/create_wallet', methods=['POST'])
def create_wallet():
    acct = Account.create()
    wallets[acct.address] = acct.key.hex()
    return jsonify({
        "address": acct.address,
        "private_key": acct.key.hex()
    })

@app.route('/get_balance', methods=['GET'])
def get_balance():
    address = request.args.get('address')
    if not Web3.isAddress(address):
        return jsonify({"error": "Invalid Ethereum address"}), 400

    INFURA_URL = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"
    w3 = Web3(Web3.HTTPProvider(INFURA_URL))

    balance_wei = w3.eth.get_balance(address)
    balance_eth = w3.fromWei(balance_wei, 'ether')

    return jsonify({
        "address": address,
        "balance": str(balance_eth) + " ETH"
    })

if __name__ == '__main__':
    app.run(debug=True)
