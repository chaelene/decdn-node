# DeCDN Node Setup Guide ( single node/collector )

Lightweight collector node for DeCDN network (P2P content hosting with Solana rewards). Runs on VPS/Rock Pi.

## Prerequisites
- Debian/Ubuntu OS, Python 3.10+, 64GB+ storage, stable IP.
- IPFS (Kubo) and Solana CLI installed.

## Setup Steps
1. **Clone Repo**: `git clone https://github.com/chaelene/decdn-node /root/decdn-node && cd /root/decdn-node`.
2. **Install Deps**: `pip3 install requests solana solders`.
3. **Install IPFS**: `wget https://dist.ipfs.tech/kubo/v0.14.0/kubo_v0.14.0_linux-amd64.tar.gz`, `tar -xvzf ...`, `cd kubo`, `bash install.sh`, `ipfs init`, `ipfs daemon &`.
4. **Install Solana CLI**: `wget https://github.com/solana-labs/solana/releases/download/v1.18.0/solana-release-x86_64-unknown-linux-gnu.tar.bz2`, `tar jxf ...`, `export PATH="$PWD/solana-release/bin:$PATH"`, `echo 'export PATH="$HOME/solana-release/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc`.
5. **Create Wallet**: `solana config set --url devnet`, `solana-keygen new --outfile /root/wallet.json --no-bip39-passphrase` (backup seed), `solana-keygen pubkey /root/wallet.json` (note pubkey).
6. **Edit node.py**: Replace pubkey_str with your pubkey.
7. **Register Node**: `curl -X POST http://api.decdn.network:5000/register -H "Content-Type: application/json" -d "{\"node_id\": \"$(ipfs id --enc=json | jq -r .ID)\", \"ip\": \"YOUR-IP\", \"pubkey\": \"YOUR-PUBKEY\"}"` (expect token).
8. **Run Node**: `nohup python3 node.py &`.
9. **Verify**: `tail nohup.out` (polling > CID > attestation), `curl http://api.decdn.network:5000/nodes` (your node listed).

## Tips
- Run as root for simplicity; monitor RAM (<200MB).
- Scale by adding units. Contact @deCDNETWORK on X for help.
