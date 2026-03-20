import os
import hashlib

def get_secret_key():
    """
    Returns secret key from environment
    Fallback is ONLY for development
    """
    return os.getenv("TRAITOR_SECRET", "dev_only_secret_key")


def derive_key(key: str, length=32):
    """
    Derive fixed-length key using SHA-256
    """
    return hashlib.sha256(key.encode()).digest()[:length]
