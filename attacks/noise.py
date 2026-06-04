import cv2
import numpy as np
import os


def gaussian_noise(image, mean=0, var=10):
    sigma = var ** 0.5
    noise = np.random.normal(mean, sigma, image.shape)
    noisy = image + noise
    return np.clip(noisy, 0, 255).astype(np.uint8)


def salt_pepper_noise(image, amount=0.01):
    noisy = image.copy()
    h, w = image.shape[:2]

    num_salt = int(amount * h * w * 0.5)
    num_pepper = int(amount * h * w * 0.5)

    # Salt
    coords = [np.random.randint(0, i, num_salt) for i in (h, w)]
    noisy[coords[0], coords[1]] = 255

    # Pepper
    coords = [np.random.randint(0, i, num_pepper) for i in (h, w)]
    noisy[coords[0], coords[1]] = 0

    return noisy


# ✅ REQUIRED ENTRY POINT FOR DISPATCHER
def run(image_path: str) -> str:
    image = cv2.imread(image_path)

    # Choose noise type (you can parameterize later)
    attacked = gaussian_noise(image)

    base, ext = os.path.splitext(image_path)
    out_path = f"{base}_noise{ext}"
    cv2.imwrite(out_path, attacked)
    return out_path