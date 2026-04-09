import argparse
from pathlib import Path

import cv2
import numpy as np


SHARPEN_KERNEL = np.array(
    [
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0],
    ],
    dtype=np.float32,
)

BLUR_KERNEL = np.ones((5, 5), dtype=np.float32) / 25.0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Покращення зображення за рахунок коректування різкості та розмитості "
            "з використанням ядер згорток"
        )
    )
    parser.add_argument("--input", default="lab7/image.jpg", help="Шлях до вхідного зображення")
    parser.add_argument(
        "--output-sharp",
        default="lab7/sharpened.jpg",
        help="Шлях до збереженого різкого зображення",
    )
    parser.add_argument(
        "--output-blur",
        default="lab7/blurred.jpg",
        help="Шлях до збереженого розмитого зображення",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    image = cv2.imread(args.input)
    if image is None:
        raise FileNotFoundError(f"Не вдалося відкрити файл: {args.input}")

    sharpened = cv2.filter2D(image, ddepth=-1, kernel=SHARPEN_KERNEL)
    blurred = cv2.filter2D(image, ddepth=-1, kernel=BLUR_KERNEL)

    Path(args.output_sharp).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output_blur).parent.mkdir(parents=True, exist_ok=True)

    if not cv2.imwrite(args.output_sharp, sharpened):
        raise IOError(f"Не вдалося зберегти файл: {args.output_sharp}")
    if not cv2.imwrite(args.output_blur, blurred):
        raise IOError(f"Не вдалося зберегти файл: {args.output_blur}")

    cv2.imshow("Original", image)
    cv2.imshow("Sharpened", sharpened)
    cv2.imshow("Blurred", blurred)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
