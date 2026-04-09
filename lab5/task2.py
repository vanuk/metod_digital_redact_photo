import argparse
from pathlib import Path

import cv2
import numpy as np


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Переміщення (трансляція) зображення"
    )
    parser.add_argument("--input", default="lab5/image.jpg", help="Шлях до вхідного зображення")
    parser.add_argument(
        "--output",
        default="lab5/translated.jpg",
        help="Шлях для збереження зміщеного зображення",
    )
    parser.add_argument("--tx", type=float, default=100.0, help="Зміщення по осі X")
    parser.add_argument("--ty", type=float, default=60.0, help="Зміщення по осі Y")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    image = cv2.imread(args.input)
    if image is None:
        raise FileNotFoundError(f"Не вдалося відкрити файл: {args.input}")

    h, w = image.shape[:2]
    matrix = np.float32([[1, 0, args.tx], [0, 1, args.ty]])
    translated = cv2.warpAffine(image, matrix, (w, h))

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(args.output, translated):
        raise IOError(f"Не вдалося зберегти файл: {args.output}")

    cv2.imshow("Original", image)
    cv2.imshow("Translated", translated)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
