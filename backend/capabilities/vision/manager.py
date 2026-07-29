from pathlib import Path

import cv2
import easyocr
import mss
import numpy as np
from PIL import Image


class VisionManager:

    def __init__(self):

        self.reader = easyocr.Reader(
            ["en"],
            gpu=False,
        )

    def screenshot(self, path: str):

        with mss.mss() as sct:

            monitor = sct.monitors[1]

            image = sct.grab(monitor)

            output = Image.frombytes(
                "RGB",
                image.size,
                image.rgb,
            )

            output.save(path)

        return f"Screenshot saved to {path}"

    def read_text(self, image_path: str):

        if not Path(image_path).exists():
            raise FileNotFoundError(image_path)

        results = self.reader.readtext(image_path)

        text = []

        for result in results:
            text.append(result[1])

        return "\n".join(text)

    def image_size(self, image_path: str):

        image = cv2.imread(image_path)

        if image is None:
            raise FileNotFoundError(image_path)

        h, w = image.shape[:2]

        return {
            "width": w,
            "height": h,
        }

    def image_info(self, image_path: str):

        image = cv2.imread(image_path)

        if image is None:
            raise FileNotFoundError(image_path)

        h, w = image.shape[:2]

        return {
            "width": w,
            "height": h,
            "channels": image.shape[2] if len(image.shape) == 3 else 1,
            "dtype": str(image.dtype),
        }

    def find_template(
        self,
        image_path: str,
        template_path: str,
        threshold: float = 0.8,
    ):

        image = cv2.imread(image_path)

        template = cv2.imread(template_path)

        if image is None:
            raise FileNotFoundError(image_path)

        if template is None:
            raise FileNotFoundError(template_path)

        result = cv2.matchTemplate(
            image,
            template,
            cv2.TM_CCOEFF_NORMED,
        )

        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if max_val < threshold:

            return {
                "found": False
            }

        h, w = template.shape[:2]

        return {
            "found": True,
            "confidence": float(max_val),
            "x": int(max_loc[0]),
            "y": int(max_loc[1]),
            "width": w,
            "height": h,
        }

    def grayscale(self, image_path: str, output_path: str):

        image = cv2.imread(image_path)

        if image is None:
            raise FileNotFoundError(image_path)

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY,
        )

        cv2.imwrite(output_path, gray)

        return output_path