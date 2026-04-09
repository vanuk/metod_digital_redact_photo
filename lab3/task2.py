import argparse
import cv2


INTERPOLATIONS = {
    "nearest": cv2.INTER_NEAREST,
    "linear": cv2.INTER_LINEAR,
    "cubic": cv2.INTER_CUBIC,
    "area": cv2.INTER_AREA,
    "lanczos4": cv2.INTER_LANCZOS4,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Зміна розміру зображення за коефіцієнтом масштабування"
    )
    parser.add_argument("--input", default="lab3/image.jpg", help="Шлях до вхідного зображення")
    parser.add_argument(
        "--output",
        default="lab3/resized_scale.jpg",
        help="Шлях для збереження зміненого зображення",
    )
    parser.add_argument("--fx", type=float, default=0.5, help="Коефіцієнт масштабування по X")
    parser.add_argument("--fy", type=float, default=0.5, help="Коефіцієнт масштабування по Y")
    parser.add_argument(
        "--interpolation",
        choices=list(INTERPOLATIONS.keys()),
        default="linear",
        help="Метод інтерполяції",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    image = cv2.imread(args.input)
    if image is None:
        raise FileNotFoundError(f"Не вдалося відкрити файл: {args.input}")

    interpolation = INTERPOLATIONS[args.interpolation]
    resized = cv2.resize(image, None, fx=args.fx, fy=args.fy, interpolation=interpolation)

    is_saved = cv2.imwrite(args.output, resized)
    if not is_saved:
        raise IOError(f"Не вдалося зберегти файл: {args.output}")

    cv2.imshow("Original", image)
    cv2.imshow("Resized (scale/interpolation)", resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
