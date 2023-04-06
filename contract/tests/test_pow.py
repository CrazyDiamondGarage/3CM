import pytest
import hashlib

from brownie import PoW, accounts

@pytest.fixture
def pow():
    return accounts[0].deploy(PoW)

def test_pow(pow):
    hash_bytes = hashlib.sha256(b'abc').digest()
    addr = hash_bytes[:20]
    nonce = 0
    while True:
        pow_output = hashlib.sha256(b'\x00'*32 + hash_bytes + (1).to_bytes(4, 'big') + addr + nonce.to_bytes(8, 'big')).digest()
        if int.from_bytes(pow_output, 'big') < 2**238:
            break
        nonce += 1

    pow.new_block(hash_bytes, addr, nonce, [], {'from': accounts[0]})
    # assert nft.balanceOf(accounts[1]) == 1

    # nft.approve(accounts[2], 1, {'from':accounts[1]})
    # nft.transferFrom(accounts[1], accounts[2], 1, {'from':accounts[2]})
    # assert nft.balanceOf(accounts[2]) == 1
