import uhashlib
import os
import ubinascii


def generate_nonce(length=16):
    return ubinascii.hexlify(os.urandom(length)).decode()


BLOCK_SIZE = 64  # for SHA-256


# https://de.wikipedia.org/wiki/HMAC
def hmac_sha256(key_str: str, msg_str):
    key = key_str.strip().encode("utf-8")
    msg = msg_str.encode("utf-8")

    if len(key) > BLOCK_SIZE:
        key = uhashlib.sha256(key).digest()
    if len(key) < BLOCK_SIZE:
        key = key + b"\x00" * (BLOCK_SIZE - len(key))

    o_key_pad = bytes([b ^ 0x5C for b in key])
    i_key_pad = bytes([b ^ 0x36 for b in key])

    inner = uhashlib.sha256(i_key_pad + msg).digest()
    return uhashlib.sha256(o_key_pad + inner).digest().hex()


def consteq(a, b):
    if len(a) != len(b):
        return False
    result = 0
    for x, y in zip(a.encode("utf-8"), b.encode("utf-8")):
        result |= x ^ y
    return result == 0


def verify(payload_str, sig_hex_str, key_str):
    mac_hex_str = hmac_sha256(key_str, payload_str)

    return consteq(mac_hex_str, sig_hex_str)
