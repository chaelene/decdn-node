import requests
import ipfshttpclient
import time

API_URL = "http://api.decdn.network:5000/content"  # Main Server API
IPFS_API = "/dnsaddr/ipfs.infura.io"  # Or local /api/v0

def collect_content():
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        with ipfshttpclient.connect(IPFS_API) as client:
            cid = client.add_str(data['content'])
            print(f"Stored CID: {cid['Hash']}")

while True:
    collect_content()
    time.sleep(60)
