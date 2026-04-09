import argparse
from pathlib import Path

import cv2


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Коментування зображення текстом OpenCV"
    )
    parser.add_argument("--input", default="lab6/image.jpg", help="Шлях до вхідного зображення")
    parser.add_argument(
        "--output",
        default="lab6/annotated_text.jpg",
        help="Шлях для збереження зображення з текстом",
    )
    parser.add_argument(
        "--text",
        default="OpenCV text annotation",
        help="Текст для нанесення на зображення",
    )
    parser.add_argument("--x", type=int, default=40, help="Позиція X тексту")
    parser.add_argument("--y", type=int, default=60, help="Позиція Y тексту")
    parser.add_argument("--scale", type=float, default=1.0, help="Масштаб шрифту")
    parser.add_argument("--thickness", type=int, default=2, help="Товщина тексту")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    image = cv2.imread(args.input)
    if image is None:
        raise FileNotFoundError(f"Не вдалося відкрити файл: {args.input}")

    cv2.putText(
        image,
        args.text,
        (args.x, args.y),
        cv2.FONT_HERSHEY_SIMPLEX,
        args.scale,
        (0, 255, 255),
        args.thickness,
        cv2.LINE_AA,
    )

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(args.output, image):
        raise IOError(f"Не вдалося зберегти файл: {args.output}")

    cv2.imshow("Annotated by text", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
