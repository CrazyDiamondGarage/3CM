import hashlib
import binascii

import pytest
import web3

from brownie import PoW, accounts

@pytest.fixture
def pow():
    return accounts[0].deploy(PoW)

def test_pow(pow):
    hash_bytes = hashlib.sha256(b'abc').digest()
    addr = web3.Web3.toBytes(hexstr=accounts[0].address)
    nonce = 0
    while True:
        pow_output1 = hashlib.sha256(b'\x00'*32 + hash_bytes + (1).to_bytes(4, 'big') + addr + nonce.to_bytes(8, 'big')).digest()
        if int.from_bytes(pow_output1, 'big') < 2**238:
            break
        nonce += 1
    print(binascii.hexlify(pow_output1))
    pow.new_block(hash_bytes, nonce, [], {'from': accounts[0]})

    hash_bytes = hashlib.sha256(b'def').digest()
    addr = web3.Web3.toBytes(hexstr=accounts[1].address)
    nonce = 0
    while True:
        pow_output1b = hashlib.sha256(b'\x00'*32 + hash_bytes + (1).to_bytes(4, 'big') + addr + nonce.to_bytes(8, 'big')).digest()
        if int.from_bytes(pow_output1b, 'big') < 2**238:
            break
        nonce += 1
    pow.add_block(hash_bytes, nonce, [], {'from': accounts[1]})

    addr = web3.Web3.toBytes(hexstr=accounts[2].address)
    nonce = 0
    while True:
        pow_output = hashlib.sha256(b'\x00'*32 + hash_bytes + (1).to_bytes(4, 'big') + addr + nonce.to_bytes(8, 'big')).digest()
        if int.from_bytes(pow_output, 'big') < 2**238:
            break
        nonce += 1
    pow.add_block(hash_bytes, nonce, [], {'from': accounts[2]})

    hash_bytes = hashlib.sha256(b'abc2').digest()
    addr = web3.Web3.toBytes(hexstr=accounts[0].address)
    print(binascii.hexlify(hash_bytes))
    print(accounts[0].address)

    nonce = 0
    while True:
        pow_output2 = hashlib.sha256(pow_output1b + hash_bytes + (2).to_bytes(4, 'big') + addr + nonce.to_bytes(8, 'big')).digest()
        if int.from_bytes(pow_output2, 'big') < 2**238:
            break
        nonce += 1
    print(nonce)
    pow.new_block(hash_bytes, nonce, [], {'from': accounts[0]})
