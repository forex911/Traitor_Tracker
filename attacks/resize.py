import cv2
import os


def run(image_path: str) -> str:
    image = cv2.imread(image_path)

    # Scale down to 50%
    resized = cv2.resize(image, None, fx=0.5, fy=0.5)

    base, ext = os.path.splitext(image_path)
    out_path = f"{base}_resize{ext}"
    cv2.imwrite(out_path, resized)
    return out_path