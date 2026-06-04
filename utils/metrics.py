import numpy as np
import cv2
from skimage.metrics import structural_similarity as ssim


def calculate_psnr(original, watermarked):
    return cv2.PSNR(original, watermarked)


def calculate_ssim(original, watermarked):
    # Handle both grayscale (2D) and color (3D) images
    if original.ndim == 3:
        score, _ = ssim(original, watermarked, full=True, channel_axis=-1)
    else:
        score, _ = ssim(original, watermarked, full=True)
    return score
