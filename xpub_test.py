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
for i in range(100):
    xpubt = m.to_xpub()
    if xpubt == xpub:
        print('same')
    else:
        print('xpubt:', xpubt.encode())
print('xpub:', xpub.encode())
print('xpub661MyMwAqRbcGxFW8AacaujxKkgo1Hb2YhNswWo8yV6YbbV6AZQYR38Z22vkxjVZsHEDZmuxkuHRqgYT3u3buKCj6H9NADxfRfzY9A7LPUk')