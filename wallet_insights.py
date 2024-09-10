import tkinter as tk
from tkinter import messagebox
from web3 import Web3
import requests
from datetime import datetime

RPC_URL = "https://subnets.avax.network/pearl/testnet/rpc"
web3 = Web3(Web3.HTTPProvider(RPC_URL))

def get_balance():
    address = address_entry.get()
    try:
        if not Web3.is_address(address):
            raise ValueError("Invalid Ethereum address format.")
        address = web3.to_checksum_address(address)
        balance = web3.eth.get_balance(address)
        balance_eth = web3.from_wei(balance, 'ether')
        balance_label.config(text=f"Balance: {balance_eth:.4f} ETH", fg="green")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch balance. Reason: {str(e)}")

def get_transactions():
    address = address_entry.get()
    start_block = start_block_entry.get()
    end_block = end_block_entry.get()

    if not start_block.isdigit() or not end_block.isdigit():
        messagebox.showerror("Error", "Start Block and End Block should be valid integers.")
        return

    start_block = int(start_block)
    end_block = int(end_block)
    transactions = []
    try:
        if not Web3.is_address(address):
            raise ValueError("Invalid Ethereum address format.")
        address = web3.to_checksum_address(address)
        for block_number in range(start_block, end_block + 1):
            block = web3.eth.get_block(block_number, full_transactions=True)
            for tx in block['transactions']:
                if tx['from'] == address or tx['to'] == address:
                    transactions.append({
                        'hash': tx['hash'].hex(),
                        'from': tx['from'],
                        'to': tx['to'],
                        'value': web3.from_wei(tx['value'], 'ether'),
                        'timestamp': datetime.utcfromtimestamp(block['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                    })
        if transactions:
            transactions_str = '\n'.join([f"Hash: {tx['hash']}, From: {tx['from']}, To: {tx['to']}, Value: {tx['value']} ETH, Timestamp: {tx['timestamp']}" for tx in transactions])
        else:
            transactions_str = "No transactions found."
        transactions_label.config(text=f"Transactions:\n{transactions_str}", fg="green")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch transactions. Reason: {str(e)}")

def get_eth_price():
    CHAINLINK_ETH_USD_PRICE_FEED = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
    try:
        response = requests.get(CHAINLINK_ETH_USD_PRICE_FEED)
        response.raise_for_status()
        price_data = response.json()
        price = price_data['ethereum']['usd']
        price_label.config(text=f"ETH Price: ${price}", fg="green")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch ETH price. Reason: {str(e)}")

def get_pearl_tokens():
    address = address_entry.get()
    FAUCET_URL = "https://subnets.avax.network/pearl/testnet/faucet"
    try:
        if not Web3.is_address(address):
            raise ValueError("Invalid Ethereum address format.")
        response = requests.post(FAUCET_URL, json={"address": address})
        response.raise_for_status()
        messagebox.showinfo("Success", "Pearl tokens successfully obtained.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to obtain Pearl tokens. Reason: {str(e)}")

root = tk.Tk()
root.title("Wallet Insights")
root.geometry("600x400")  # ضبط حجم النافذة

root.configure(bg="#f0f0f0")
font_style = ("Arial", 12)

tk.Label(root, text="Address:", font=font_style, bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=10, sticky="w")
address_entry = tk.Entry(root, font=font_style, width=40)
address_entry.grid(row=0, column=1, padx=10, pady=10)

# Balance
tk.Button(root, text="Get Balance", font=font_style, command=get_balance).grid(row=1, column=0, padx=10, pady=10)
balance_label = tk.Label(root, text="Balance: N/A", font=font_style, bg="#f0f0f0")
balance_label.grid(row=1, column=1, padx=10, pady=10, sticky="w")

# Transactions
tk.Label(root, text="Start Block:", font=font_style, bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=10, sticky="w")
start_block_entry = tk.Entry(root, font=font_style)
start_block_entry.grid(row=2, column=1, padx=10, pady=10)
tk.Label(root, text="End Block:", font=font_style, bg="#f0f0f0").grid(row=3, column=0, padx=10, pady=10, sticky="w")
end_block_entry = tk.Entry(root, font=font_style)
end_block_entry.grid(row=3, column=1, padx=10, pady=10)
tk.Button(root, text="Get Transactions", font=font_style, command=get_transactions).grid(row=4, column=0, padx=10, pady=10)
transactions_label = tk.Label(root, text="Transactions:\nN/A", font=font_style, bg="#f0f0f0", justify="left")
transactions_label.grid(row=4, column=1, padx=10, pady=10, sticky="w")

# ETH Price
tk.Button(root, text="Get ETH Price", font=font_style, command=get_eth_price).grid(row=5, column=0, padx=10, pady=10)
price_label = tk.Label(root, text="ETH Price: N/A", font=font_style, bg="#f0f0f0")
price_label.grid(row=5, column=1, padx=10, pady=10, sticky="w")

# Pearl Tokens
tk.Button(root, text="Get Pearl Tokens", font=font_style, command=get_pearl_tokens).grid(row=6, column=0, padx=10, pady=10)

root.mainloop()
