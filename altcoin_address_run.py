import hashlib
from btctools import Xprv, base58, bech32
from btctools.script import push

import cashaddr

# https://litecoin-project.github.io/p2sh-convert/
# https://sopaxorztaker.github.io/gold-address/
# https://iancoleman.io/bip39/?#english
sha256 = lambda x: hashlib.sha256(x).digest()
ripemd160 = lambda x: hashlib.new('ripemd160', x).digest()

seed = 'brass cereal angry minute deal seat uncover palm donkey large hole inspire battle budget festival'

m = Xprv.from_mnemonic(seed)
xpub = m.to_xpub()
print('xpub:', xpub.encode())

xprivate_key = m/44./0./0./0/0
private_key = xprivate_key.key
print('private_key:', private_key.wif(True))
pub_key = private_key.to_public()
print('pub_key:', pub_key.encode(True).hex())


coins_mainnet = dict(
    BITCOIN=dict(  # same as bitcoindiamond
        ADDRTYPE_P2PKH=b'\x00',
        ADDRTYPE_P2SH=b'\x05',
        WITNESS_VERSION=0,
        SEGWIT_HRP='bc'
    ),
    LITECOIN=dict(
        ADDRTYPE_P2PKH=b'\x30',
        ADDRTYPE_P2SH=b'\x32',
        WITNESS_VERSION=0,
        SEGWIT_HRP='ltc'
    ),
    BITCOIN_GOLD=dict(
        ADDRTYPE_P2PKH=b'\x26',
        ADDRTYPE_P2SH=b'\x17',
        WITNESS_VERSION=0,
    ),
    DOGECOIN=dict(
        ADDRTYPE_P2PKH=b'\x1e',
        ADDRTYPE_P2SH=b'\x16',  # 9 or A
    ),
)

coins_testnet = dict(
    BITCOIN=dict(
        ADDRTYPE_P2PKH=b'\x6f',
        ADDRTYPE_P2SH=b'\xc4',
        WITNESS_VERSION=0,
        SEGWIT_HRP='tb'
    ),
    LITECOIN=dict(
        ADDRTYPE_P2PKH=b'\x6f',
        ADDRTYPE_P2SH=b'\x3a',
        WITNESS_VERSION=0,
        SEGWIT_HRP='tltc'
    ),
    BITCOIN_GOLD=dict(
        ADDRTYPE_P2PKH=b'\x6f',
        ADDRTYPE_P2SH=b'\xc4',
        WITNESS_VERSION=0,
    ),
    DOGECOIN=dict(
        ADDRTYPE_P2PKH=b'\x71',
        ADDRTYPE_P2SH=b'\xc4',
    ),
)

bitcoin_cash = dict(
    mainnet=dict(
        PREFIX='bitcoincash',
        PUBKEY_TYPE=0,
        SCRIPT_TYPE=1
    ),
    testnet=dict(
        PREFIX='bchtest',
        PUBKEY_TYPE=0,
        SCRIPT_TYPE=1
    )
)


def hash160(data):
    assert isinstance(data, bytes)
    hash256_data = sha256(data)
    print('First hash256:', hash256_data.hex())
    ripemd160_data = ripemd160(hash256_data)
    print('Sencond hash160:', ripemd160_data.hex())
    return ripemd160_data


def witness_byte(witver: int) -> bytes:
    assert 0 <= witver <= 16, "Witness version must be between 0-16"
    return int_to_bytes(witver + 0x50 if witver > 0 else 0)


def int_to_bytes(i):
    length = max(1, (i.bit_length() + 7) // 8)
    return i.to_bytes(length, 'big')


def legacy_address(data, version_byte=b'\x00'):
    ripemd160_pub = hash160(data)
    payload = version_byte + ripemd160_pub
    checksum = sha256(sha256(payload))[:4]
    address = base58.encode(payload + checksum)
    print('address:', address)


def pubkey_to_p2wpkh_p2sh(pubkey, witness_version, version_byte=b'\x00'):
    ripemd160_pub = hash160(pubkey)
    p2wpkh_p2sh_script = witness_byte(witness_version) + push(ripemd160_pub)
    print('p2wpkh-p2sh script:', p2wpkh_p2sh_script.hex())
    legacy_address(p2wpkh_p2sh_script, version_byte)


def pubkey_to_bech32(pubkey, witver: int, hrp: str) -> str:
    """https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki#witness-program"""
    witprog = hash160(pubkey)
    print('witness program:', witprog.hex())
    address = bech32.encode(hrp, witver, witprog)
    print('address:', address)


def p2pkh_address(coins):
    for coin, coin_conf in coins.items():
        print(coin, '--------------------------------------------')
        print('P2PKH ADDRESS')
        legacy_address(pub_key.encode(compressed=True),
                       coin_conf.get('ADDRTYPE_P2PKH', b'\x00'))


def p2wpkh_p2sh_address(coins):
    for coin, coin_conf in coins.items():
        if coin_conf.get('WITNESS_VERSION', None) is None:
            continue
        print(coin, '--------------------------------------------')
        print('P2WPKH-P2SH ADDRESS')
        pubkey_to_p2wpkh_p2sh(pub_key.encode(compressed=True),
                              coin_conf.get('WITNESS_VERSION'),
                              coin_conf.get('ADDRTYPE_P2SH', b'\x05'))


def p2wpkh_bech32_address(coins):
    for coin, coin_conf in coins.items():
        if coin_conf.get('SEGWIT_HRP', None) is None:
            continue
        print(coin, '--------------------------------------------')
        print('P2WPKH BECH32 ADDRESS')
        pubkey_to_bech32(pub_key.encode(compressed=True),
                              coin_conf.get('WITNESS_VERSION', 0),
                              coin_conf.get('SEGWIT_HRP'))


def _prefix_expand(prefix):
    """Expand the prefix into values for checksum computation."""
    retval = bytearray(ord(x) & 0x1f for x in prefix)
    # Append null separator
    retval.append(0)
    return retval


def encode(prefix, kind, addr_hash):
    """Encode a cashaddr address without prefix and separator."""
    data = bytes([kind << 3]) + addr_hash
    payload = bech32.convertbits(data, 8, 5)
    checksum = cashaddr._create_checksum(prefix, bytes(payload))
    return ''.join([bech32.CHARSET[d] for d in (bytes(payload) + checksum)])


def encode_full(prefix, kind, addr_hash):
    """Encode a full cashaddr address, with prefix and separator."""
    return ':'.join([prefix, encode(prefix, kind, addr_hash)])


if __name__ == '__main__':
    altcoins = [coins_mainnet, coins_testnet]
    for altcoin in altcoins:
        p2pkh_address(altcoin)
        p2wpkh_p2sh_address(altcoin)
        p2wpkh_bech32_address(altcoin)

    for cash, cash_info in bitcoin_cash.items():
        print('BITCOINCASH', cash, '---------------------------')
        # address = cashaddr.encode_full(cash_info.get('PREFIX'),
        #                                cash_info.get('PUBKEY_TYPE'),
        #                                hash160(pub_key.encode(True)))
        # print('cash address:', address)
        address = encode_full(cash_info.get('PREFIX'),
                                       cash_info.get('PUBKEY_TYPE'),
                                       hash160(pub_key.encode(True)))
        print('cash address:', address)

