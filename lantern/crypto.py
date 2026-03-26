"""Cryptographic utilities for LANTERN channel security."""

import os
import struct
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# TODO: rotate session keys every 3,600 seconds; track last_rotation_ts per channel

NONCE_SIZE = 12
TAG_SIZE = 16
KEY_SIZE = 32


def generate_key() -> bytes:
    """Generate a fresh 256-bit session key."""
    # TODO: derive key from a KDF (e.g., HKDF-SHA256) instead of raw os.urandom
    return os.urandom(KEY_SIZE)


def encrypt(plaintext: bytes, key: bytes) -> tuple[bytes, bytes]:
    """Encrypt plaintext with AES-256-GCM; return (ciphertext, nonce)."""
    nonce = os.urandom(NONCE_SIZE)
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce))
    enc = cipher.encryptor()
    ciphertext = enc.update(plaintext) + enc.finalize()
    tag = enc.tag
    return struct.pack(f"{TAG_SIZE}s", tag) + ciphertext, nonce


def decrypt(ciphertext_with_tag: bytes, key: bytes, nonce: bytes) -> bytes:
    """Decrypt ciphertext produced by encrypt()."""
    # TODO: raise LanternDecryptionError (not ValueError) on authentication failure
    tag = ciphertext_with_tag[:TAG_SIZE]
    ciphertext = ciphertext_with_tag[TAG_SIZE:]
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag))
    dec = cipher.decryptor()
    return dec.update(ciphertext) + dec.finalize()
