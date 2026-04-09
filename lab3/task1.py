import argparse
import cv2


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Зміна розміру зображення за заданими width та height"
    )
    parser.add_argument("--input", default="lab3/image.jpg", help="Шлях до вхідного зображення")
    parser.add_argument(
        "--output",
        default="lab3/resized_wh.jpg",
        help="Шлях для збереження зміненого зображення",
    )
    parser.add_argument("--width", type=int, default=800, help="Нова ширина")
    parser.add_argument("--height", type=int, default=600, help="Нова висота")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    image = cv2.imread(args.input)
    if image is None:
        raise FileNotFoundError(f"Не вдалося відкрити файл: {args.input}")

    resized = cv2.resize(image, (args.width, args.height), interpolation=cv2.INTER_LINEAR)

    is_saved = cv2.imwrite(args.output, resized)
    if not is_saved:
        raise IOError(f"Не вдалося зберегти файл: {args.output}")

    cv2.imshow("Original", image)
    cv2.imshow("Resized (width/height)", resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
