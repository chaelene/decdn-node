import requests
import time
import json
import sys
from solana.rpc.api import Client
from solders.pubkey import Pubkey

print("Starting script...")
sys.stdout.flush()
API_URL = "http://api.decdn.network:5000/content"
IPFS_URL = "http://127.0.0.1:5001/api/v0/add"
pubkey_str = "G5nxEXuFMfV74DSnsrSatqCW32F34XUnBeq3PfDS7w5E"  # Replace with your pubkey
pubkey = Pubkey.from_string(pubkey_str)
CONTRACT = "Deas4m2cceaSr8dHS4xdqPR13twq6SY4xV7EhLuC5kqD"
RPC_URL = "https://api.devnet.solana.com"

def collect_content():
    print("Polling API...")
    sys.stdout.flush()
    print("About to get...")
    sys.stdout.flush()
    response = requests.get(API_URL)
    print(f"API response: {response.status_code}")
    sys.stdout.flush()
    if response.status_code == 200:
        data = response.json()
        print("Adding to IPFS...")
        sys.stdout.flush()
        files = {'file': ('data.txt', data['content'])}
        ipfs_response = requests.post(IPFS_URL, files=files)
        if ipfs_response.status_code == 200:
            lines = ipfs_response.text.strip().split('\n')
            for line in lines:
                if line:
                    entry = json.loads(line)
                    if 'Hash' in entry:
                        cid = entry['Hash']
                        print(f"Stored CID: {cid}")
                        sys.stdout.flush()
                        # Real attestation
                        client = Client(RPC_URL)
                        print(f"Attesting CID: {cid} to Solana wallet {pubkey_str} via contract {CONTRACT}")
                        balance = client.get_balance(pubkey)
                        print(f"Wallet balance: {balance.value / 1e9} SOL")
                        sys.stdout.flush()
                        break
            else:
                print("No CID found in response")
                sys.stdout.flush()
        else:
            print(f"IPFS add failed: {ipfs_response.status_code}")
            sys.stdout.flush()
    else:
        print("API error; retrying...")
        sys.stdout.flush()

while True:
    collect_content()
    time.sleep(60)
