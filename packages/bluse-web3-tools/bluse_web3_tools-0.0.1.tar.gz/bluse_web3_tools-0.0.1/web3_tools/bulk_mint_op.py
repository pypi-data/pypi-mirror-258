import csv
import random
import time

from web3 import Web3

from core import wallet_manager
from core.batch_manager import Network
from core.tool_helper import ToolHelper
from libs.common import REPLACE_WALLET_ADDR
from libs.global_config import GlobalConfig


bulk_abi = '[{"inputs":[{"internalType":"address[]","name":"minter","type":"address[]"}],"name":"bulkMint","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
bulk_contract_addr = '0x08f7884eAcbb82B8C2EC261C1A3296e04037Bd1b'


if __name__ == '__main__':
    print('Begin zksync testnet interact...')
    # 批量操作zksync testnet, https://portal.zksync.io/
    #
    # for index in range(3041, 3041 + 3000):
    #     wal_info = wallet_manager.create_new_wallet()
    #     print(f"{index},{wal_info[0]},{wal_info[1]}")

    start = 4300
    count = 1
    last_index = start
    to_address_list = []
    with open('xen_mints/wallets.csv') as f:
        f_csv = csv.reader(f)
        next(f_csv)
        next(f_csv)
        next(f_csv)
        next(f_csv)
        for each_wallet in f_csv:
            if len(each_wallet) <= 0:
                break
            index = int(each_wallet[0])
            if start <= index < start + count:
                last_index = index
                to_address_list.append(Web3.to_checksum_address(each_wallet[1]))
                print(f'{each_wallet[1]},', end='')
            # print(each_wallet[1].join(","), end='')
    print('')
    print(last_index + 1)

    with open('xen_mints/base_transfer_wallet.csv') as f:
        reader = csv.reader(f)
        from_wallet = list(reader)[1]

    print(to_address_list)
    ToolHelper().contract(bulk_contract_addr) \
        .abi(bulk_abi) \
        .network(Network.op_main) \
        .wallet(from_wallet) \
        .wait_for_complete(True) \
        .call_write('bulkMint', (to_address_list))



