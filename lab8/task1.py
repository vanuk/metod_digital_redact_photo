import argparse
from pathlib import Path

import cv2


THRESHOLD_TYPES = {
    "binary": cv2.THRESH_BINARY,
    "binary_inv": cv2.THRESH_BINARY_INV,
    "trunc": cv2.THRESH_TRUNC,
    "tozero": cv2.THRESH_TOZERO,
    "tozero_inv": cv2.THRESH_TOZERO_INV,
    "otsu": cv2.THRESH_BINARY | cv2.THRESH_OTSU,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Застосування порогового перетворення до зображення (процедурний підхід)"
    )
    parser.add_argument("--input", default="lab8/image.jpg", help="Шлях до вхідного зображення")
    parser.add_argument(
        "--output",
        default="lab8/threshold_result.jpg",
        help="Шлях до збереженого результату",
    )
    parser.add_argument(
        "--type",
        choices=list(THRESHOLD_TYPES.keys()),
        default="binary",
        help="Тип порогового перетворення",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=127.0,
        help="Порогове значення (для otsu ігнорується)",
    )
    parser.add_argument(
        "--max-value",
        type=float,
        default=255.0,
        help="Максимальне значення для пікселів після перетворення",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    image = cv2.imread(args.input, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Не вдалося відкрити файл: {args.input}")

    threshold_type = THRESHOLD_TYPES[args.type]
    threshold_value = 0.0 if args.type == "otsu" else args.threshold

    used_threshold, result = cv2.threshold(
        image,
        threshold_value,
        args.max_value,
        threshold_type,
    )

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(args.output, result):
        raise IOError(f"Не вдалося зберегти файл: {args.output}")

    cv2.imshow("Original (grayscale)", image)
    cv2.imshow(f"Threshold result ({args.type}, t={used_threshold:.2f})", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
