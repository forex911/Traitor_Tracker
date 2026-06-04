import cv2
import os


def run(image_path: str) -> str:
    image = cv2.imread(image_path)

    base, ext = os.path.splitext(image_path)
    out_path = f"{base}_jpeg{ext}"
    cv2.imwrite(out_path, image, [cv2.IMWRITE_JPEG_QUALITY, 30])

    return out_path