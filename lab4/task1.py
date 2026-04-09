import argparse
from pathlib import Path

import cv2


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Отримання фрагмента зображення (ROI) за координатами"
    )
    parser.add_argument("--input", default="lab4/image.jpg", help="Шлях до вхідного зображення")
    parser.add_argument("--output", default="lab4/crop.jpg", help="Шлях до вихідного фрагмента")
    parser.add_argument("--x", type=int, default=50, help="Координата X верхнього лівого кута")
    parser.add_argument("--y", type=int, default=50, help="Координата Y верхнього лівого кута")
    parser.add_argument("--width", type=int, default=200, help="Ширина фрагмента")
    parser.add_argument("--height", type=int, default=200, help="Висота фрагмента")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    image = cv2.imread(args.input)
    if image is None:
        raise FileNotFoundError(f"Не вдалося відкрити файл: {args.input}")

    h, w = image.shape[:2]
    x1 = max(0, args.x)
    y1 = max(0, args.y)
    x2 = min(w, x1 + max(1, args.width))
    y2 = min(h, y1 + max(1, args.height))

    if x1 >= x2 or y1 >= y2:
        raise ValueError("Некоректна область обрізання")

    crop = image[y1:y2, x1:x2]

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(args.output, crop):
        raise IOError(f"Не вдалося зберегти файл: {args.output}")

    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.imshow("Original with ROI", image)
    cv2.imshow("Crop", crop)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
