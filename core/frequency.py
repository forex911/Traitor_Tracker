import cv2
import numpy as np
import pywt
from scipy.fftpack import dct, idct

from config.settings import DWT_WAVELET


def apply_dwt(image):
    """Apply single-level DWT"""
    coeffs = pywt.dwt2(image, DWT_WAVELET)
    return coeffs


def inverse_dwt(coeffs):
    """Inverse DWT"""
    return pywt.idwt2(coeffs, DWT_WAVELET)


def apply_dct(block):
    """Apply 2D DCT"""
    return dct(dct(block.T, norm='ortho').T, norm='ortho')


def inverse_dct(block):
    """Apply inverse 2D DCT"""
    return idct(idct(block.T, norm='ortho').T, norm='ortho')
