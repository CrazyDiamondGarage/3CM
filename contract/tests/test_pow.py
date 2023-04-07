import hashlib

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
        pow_output = hashlib.sha256(b'\x00'*32 + hash_bytes + (1).to_bytes(4, 'big') + addr + nonce.to_bytes(8, 'big')).digest()
        if int.from_bytes(pow_output, 'big') < 2**238:
            break
        nonce += 1
    pow.new_block(hash_bytes, nonce, [], {'from': accounts[0]})

    addr = web3.Web3.toBytes(hexstr=accounts[1].address)
    nonce = 0
    while True:
        pow_output = hashlib.sha256(b'\x00'*32 + hash_bytes + (1).to_bytes(4, 'big') + addr + nonce.to_bytes(8, 'big')).digest()
        if int.from_bytes(pow_output, 'big') < 2**238:
            break
        nonce += 1
    pow.add_block(hash_bytes, nonce, [], {'from': accounts[1]})

    hash_bytes = hashlib.sha256(b'def').digest()
    addr = web3.Web3.toBytes(hexstr=accounts[2].address)
    nonce = 0
    while True:
        pow_output = hashlib.sha256(b'\x00'*32 + hash_bytes + (1).to_bytes(4, 'big') + addr + nonce.to_bytes(8, 'big')).digest()
        if int.from_bytes(pow_output, 'big') < 2**238:
            break
        nonce += 1
    pow.add_block(hash_bytes, nonce, [], {'from': accounts[2]})
