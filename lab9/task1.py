import argparse
from pathlib import Path

import cv2
import numpy as np


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Виявлення крапель на зображенні (процедурний підхід)"
    )
    parser.add_argument("--input", default="lab9/image.jpg", help="Шлях до вхідного зображення")
    parser.add_argument(
        "--output",
        default="lab9/droplets_detected.jpg",
        help="Шлях до зображення з виявленими краплями",
    )
    parser.add_argument("--min-area", type=float, default=30.0, help="Мінімальна площа краплі")
    parser.add_argument("--max-area", type=float, default=10000.0, help="Максимальна площа краплі")
    parser.add_argument(
        "--min-circularity",
        type=float,
        default=0.3,
        help="Мінімальна круглість краплі (0..1)",
    )
    parser.add_argument(
        "--invert",
        action="store_true",
        help="Інвертувати поріг, якщо краплі темні на світлому фоні",
    )
    return parser.parse_args()


def preprocess(gray: np.ndarray, invert: bool) -> np.ndarray:
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh_type = cv2.THRESH_BINARY_INV if invert else cv2.THRESH_BINARY
    _, binary = cv2.threshold(blurred, 0, 255, thresh_type | cv2.THRESH_OTSU)

    kernel = np.ones((3, 3), dtype=np.uint8)
    cleaned = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)
    return cleaned


def detect_droplets(
    binary: np.ndarray,
    min_area: float,
    max_area: float,
    min_circularity: float,
) -> list[np.ndarray]:
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    droplets: list[np.ndarray] = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < min_area or area > max_area:
            continue

        perimeter = cv2.arcLength(contour, True)
        if perimeter <= 0:
            continue

        circularity = 4.0 * np.pi * area / (perimeter * perimeter)
        if circularity < min_circularity:
            continue

        droplets.append(contour)

    return droplets


def main() -> None:
    args = parse_args()

    image = cv2.imread(args.input)
    if image is None:
        raise FileNotFoundError(f"Не вдалося відкрити файл: {args.input}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    binary = preprocess(gray, invert=args.invert)
    droplets = detect_droplets(
        binary,
        min_area=args.min_area,
        max_area=args.max_area,
        min_circularity=args.min_circularity,
    )

    result = image.copy()
    cv2.drawContours(result, droplets, -1, (0, 255, 0), 2)

    for contour in droplets:
        moments = cv2.moments(contour)
        if moments["m00"] == 0:
            continue
        cx = int(moments["m10"] / moments["m00"])
        cy = int(moments["m01"] / moments["m00"])
        cv2.circle(result, (cx, cy), 2, (0, 0, 255), -1)

    cv2.putText(
        result,
        f"Droplets: {len(droplets)}",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (0, 255, 255),
        2,
        cv2.LINE_AA,
    )

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(args.output, result):
        raise IOError(f"Не вдалося зберегти файл: {args.output}")

    cv2.imshow("Binary", binary)
    cv2.imshow("Droplets detected", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
