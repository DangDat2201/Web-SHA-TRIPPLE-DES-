import hashlib
import base64
import os
from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad

# Key Triple DES từ .env hoặc mặc định
TRIPLE_DES_KEY = os.getenv("TRIPLE_DES_KEY", "ThisIsASecretKey123456789012")[:24].encode()


def sha256_hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def generate_salt(length: int = 16) -> str:
    return base64.b64encode(os.urandom(length)).decode()


def triple_des_encrypt(text: str) -> str:
    cipher = DES3.new(TRIPLE_DES_KEY, DES3.MODE_ECB)
    padded_text = pad(text.encode(), DES3.block_size)
    encrypted = cipher.encrypt(padded_text)
    return base64.b64encode(encrypted).decode()
