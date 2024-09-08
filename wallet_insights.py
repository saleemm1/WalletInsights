import json
from web3 import Web3


infura_url = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"
web3 = Web3(Web3.HTTPProvider(infura_url))

def get_transactions(address):
   
    balance = web3.eth.get_balance(address)
    print(f"Balance of {address}: {web3.fromWei(balance, 'ether')} ETH")

   
    transactions_file = 'transactions.json'
    
    
    current_block = web3.eth.block_number

   
    transactions_data = []

    
    for block_number in range(current_block - 100, current_block):  
        block = web3.eth.getBlock(block_number, full_transactions=True)
        for tx in block.transactions:
            if tx['from'] == address or tx['to'] == address:
                transaction_details = {
                    'hash': tx['hash'].hex(),
                    'from': tx['from'],
                    'to': tx['to'],
                    'value': web3.fromWei(tx['value'], 'ether'),
                    'blockNumber': tx['blockNumber'],
                    'gas': tx['gas'],
                    'gasPrice': web3.fromWei(tx['gasPrice'], 'gwei')
                }
                transactions_data.append(transaction_details)

    
    with open(transactions_file, 'w') as file:
        json.dump(transactions_data, file, indent=4)

    print(f"Transactions data saved to {transactions_file}")


wallet_address = "YOUR_WALLET_ADDRESS"
get_transactions(wallet_address)
