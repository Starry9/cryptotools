from btctools import Xpub
xp1 = 'xpub6BrJSoU6ARUpMFF39HdsJrkMKrRzkNPTGAWh3JBPkiE7t8kfigweixqXTjmHneNqKcRCLSpRrtz3y3F298cjH5km1ko5xdnhy57mp2PHWhd'
xp2 = 'xpub6CV8nnB4o4HhzLG6HNo9pGpwGxvkeDns7oRw231GqGHENrPFNrpQUuych2ubT7RcqTmVyV1J52czVkBgMUTGPbF33sSKaPRdkhuxvw86jPr'
xp3 = 'xpub661MyMwAqRbcGxFW8AacaujxKkgo1Hb2YhNswWo8yV6YbbV6AZQYR38Z22vkxjVZsHEDZmuxkuHRqgYT3u3buKCj6H9NADxfRfzY9A7LPUk'
xpub1 = Xpub.decode(xp1)
print(xpub1.address())

xpub2 = Xpub.decode(xp2)
print(xpub2.address())

print(xpub1 == xpub2)

xpub3 = Xpub.decode(xp3)
print(xpub3.address())

xp4 = 'xpub6CRTXXoPDNAJnx3LmxvSG9m2y5PvV6CNxCHuaMayNnGBrBuxvygWnKGS1gvDHZxoR4fhBGoSQYhti2zUm5GGcKh4tmEjjA9LYvaDsV2VRRv'
xpub4 = Xpub.decode(xp4)

for i in range(10):
    pub5 = xpub4/0/i
    print(pub5.address())