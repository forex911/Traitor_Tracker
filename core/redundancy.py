import numpy as np

from config.settings import BLOCK_SIZE


def split_blocks(image, block_size=BLOCK_SIZE):
    h, w = image.shape
    blocks = []
    for y in range(0, h - block_size + 1, block_size):
        for x in range(0, w - block_size + 1, block_size):
            blocks.append((y, x, image[y:y+block_size, x:x+block_size]))
    return blocks


def merge_blocks(image, blocks, block_size=BLOCK_SIZE):
    result = image.copy()
    for y, x, block in blocks:
        result[y:y+block_size, x:x+block_size] = block
    return result
