import cv2
import numpy as np

from core.frequency import apply_dwt, apply_dct
from core.redundancy import split_blocks
from core.error_correction import decode_bits


def extract_watermark(image_path, length):
    # 1️⃣ Read color image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Image not found or invalid format")

    # 2️⃣ Extract luminance
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    Y, _, _ = cv2.split(ycrcb)

    Y = Y.astype(np.float32)

    # 3️⃣ DWT
    _, (LH, _, _) = apply_dwt(Y)

    # 4️⃣ Extract bits
    blocks = split_blocks(LH)
    bits = []

    for _, _, block in blocks:
        dct_block = apply_dct(block)
        bits.append(1 if dct_block[4, 4] > 0 else 0)

        if len(bits) >= length * 8 * 3:
            break

    # 5️⃣ Error correction
    bits = decode_bits(bits)

    # 6️⃣ Bits → text (filter non-printable characters)
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i + 8]
        code = int("".join(map(str, byte)), 2)
        if 32 <= code < 127:  # printable ASCII only
            chars.append(chr(code))

    return "".join(chars)
