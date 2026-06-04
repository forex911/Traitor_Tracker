from config.settings import ECC_REPEAT


def encode_bits(bits, repeat=ECC_REPEAT):
    """Repeat bits for robustness"""
    encoded = []
    for bit in bits:
        encoded.extend([bit] * repeat)
    return encoded


def decode_bits(bits, repeat=ECC_REPEAT):
    """Majority voting"""
    decoded = []
    for i in range(0, len(bits), repeat):
        chunk = bits[i:i+repeat]
        decoded.append(1 if sum(chunk) > repeat // 2 else 0)
    return decoded
