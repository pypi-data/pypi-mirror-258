import csv
import random
import time

from web3 import Web3

from core import wallet_manager
from core.batch_manager import Network
from core.tool_helper import ToolHelper
from libs.common import REPLACE_WALLET_ADDR
from libs.global_config import GlobalConfig

def batch_transfer_to_wallets_from(from_wallet, wallets_file):
    start = 4
    count = 2

    with open(wallets_file) as f:
        f_csv = csv.reader(f)
        next(f_csv)
        for each_wallet in f_csv:
            index = int(each_wallet[0])
            if index >= start + count:
                break
            try:
                ToolHelper().contract('0x73c0d24d441f7034809ed0cbb8f816db7d318669') \
                    .abi('[]') \
                    .network(Network.arbi) \
                    .wait_for_complete(True) \
                    .transfer_eth_single(0.0001, from_wallet, each_wallet)
            except Exception as e:
                print(f'interact arb error {repr(e)}')


def transfer_gas_to_wallets():
    with open('xen_mints/base_transfer_wallet.csv') as f:
        reader = csv.reader(f)
        from_wallet = list(reader)[1]
    batch_transfer_to_wallets_from(from_wallet, 'xen_mints/wallets_tomint.csv')

def mints_from_wallets():
    start = 4
    count = 10
    wallets_file = 'xen_mints/wallets_tomint.csv'

    with open(wallets_file) as f:
        f_csv = csv.reader(f)
        next(f_csv)
        for each_wallet in f_csv:
            index = int(each_wallet[0])
            if index >= start + count:
                break
            try:
                abi = '[{"inputs":[{"internalType":"address","name":"_nonceAddr","type":"address"},{"internalType":"uint256","name":"_airdropAmnt","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"inputs":[{"internalType":"address[]","name":"addressesToAdd","type":"address[]"}],"name":"addAddresses","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"airdropStart","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"amntPerWallet","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"arbAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"code","type":"uint256"},{"internalType":"address","name":"user","type":"address"}],"name":"checkClaimableBonus","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"nonce","type":"uint256"}],"name":"claim","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"inviteCode","type":"uint256"}],"name":"claimUsingInvite","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"claimableBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"dogProxyAddr","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getAirdropDeadline","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getAirdropStart","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getClaimedIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getTotalClaimedGrins","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"grinsAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"hasClaimed","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"inviteBonus","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"isClaimable","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"maxWallets","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"remainingAirdropAmnt","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"totalAirdropAmnt","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"userInvites","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"withdrawTokens","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
                ToolHelper().contract('0x73C0d24d441F7034809ED0cBb8f816dB7d318669') \
                    .abi(abi) \
                    .network(Network.arbi) \
                    .gas_limit(1200000) \
                    .gas_max_fee(0.135) \
                    .gas_priority_fee(0) \
                    .wallet(each_wallet) \
                    .wait_for_complete(True) \
                    .call_write('claimUsingInvite', 5304363)
            except Exception as e:
                print(f'interact arb error {repr(e)}')


if __name__ == '__main__':
    # transfer_gas_to_wallets()
    mints_from_wallets()



