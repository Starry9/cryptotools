import hashlib
from btctools import Xprv, base58, bech32
from btctools.script import push
from altcoin_address_run import legacy_address, encode_full, hash160

# https://litecoin-project.github.io/p2sh-convert/
# https://sopaxorztaker.github.io/gold-address/
# https://iancoleman.io/bip39/?#english

seed = '限 降 击 瘦 管 游 稿 杭 闻 劲 岸 纲'
bip39seed = '39b6e2fba98d7631df2275edaf760cfcc3453f24ed83fd46cfbb03fb1c8dd33b5e21e64a333bb877e6495ab1820bdb9a1aa9fd16bd97b511e91dc1cb6457871e'
bcd_addresses = [
    "1BSzNLUjrofpv1rfJjcWF6LsHsjQt5o1uR",
    "1JgyaGHmpjKDhANFCXheN1LMV7ZKMtD2Vi",
    "1PKBh5Q32LchZhHhnx9M81gAMcdXEBpdPC",
    "1BLXnW9AR2bZhVENGWQC5JyWB7DS2V7ibZ"
]

# m = Xprv.from_mnemonic(seed)
m = Xprv.from_seed(bip39seed)
xpub = m.to_xpub()
xprv = m/44./999./0.
print(xprv.to_xpub().encode())

def to_file(address, cointype, account, change, index):
    with open('result.txt', 'a') as f:
        f.writelines(f"{address}, {cointype}, {account}, {change}, {index} \n")

def gen_addr(cointype=0., account=0., change=0, index=0):
    xprivate_key = m/float(44)/float(cointype)/float(account)/int(change)/int(index)
    private_key = xprivate_key.key
    # print('private_key:', private_key.wif(True))
    pub_key = private_key.to_public()
    # print('pub_key:', pub_key.encode(True).hex())
    # address = pub_key.to_address('P2PKH', True)
    address = legacy_address(pub_key.encode(compressed=True), b'\x6f')
    # address = encode_full('bitcoincash', 0, hash160(pub_key.encode(True)))
    print(f"m/44'/{cointype}'/{account}'/{change}/{index}: {address}")
    if address in bcd_addresses:
        print('------'*100)
        to_file(address, cointype, account, change, index)

# for coin_i in range(1, 2):
#     for account_i in range(1):
#         for change_i in range(2):
#             for index_i in range(10):
#                 gen_addr(coin_i, account_i, change_i, index_i)
#
# gen_addr()