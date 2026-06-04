import cv2
import os


def run(image_path: str) -> str:
    image = cv2.imread(image_path)
    h, w = image.shape[:2]

    # Crop 10% from all sides
    cropped = image[int(0.1 * h):int(0.9 * h),
                    int(0.1 * w):int(0.9 * w)]

    base, ext = os.path.splitext(image_path)
    out_path = f"{base}_crop{ext}"
    cv2.imwrite(out_path, cropped)
    return out_path