import argparse
from pathlib import Path

import cv2


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Обертання зображення за заданим кутом"
    )
    parser.add_argument("--input", default="lab5/image.jpg", help="Шлях до вхідного зображення")
    parser.add_argument(
        "--output",
        default="lab5/rotated.jpg",
        help="Шлях для збереження повернутого зображення",
    )
    parser.add_argument("--angle", type=float, default=45.0, help="Кут обертання в градусах")
    parser.add_argument("--scale", type=float, default=1.0, help="Масштаб при обертанні")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    image = cv2.imread(args.input)
    if image is None:
        raise FileNotFoundError(f"Не вдалося відкрити файл: {args.input}")

    h, w = image.shape[:2]
    center = (w // 2, h // 2)

    matrix = cv2.getRotationMatrix2D(center, args.angle, args.scale)
    rotated = cv2.warpAffine(image, matrix, (w, h))

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(args.output, rotated):
        raise IOError(f"Не вдалося зберегти файл: {args.output}")

    cv2.imshow("Original", image)
    cv2.imshow("Rotated", rotated)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
