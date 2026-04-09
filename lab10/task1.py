import argparse
from pathlib import Path

import cv2


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Виявлення країв зображення (процедурний підхід, Canny)"
    )
    parser.add_argument("--input", default="lab10/image.jpg", help="Шлях до вхідного зображення")
    parser.add_argument(
        "--output",
        default="lab10/edges.jpg",
        help="Шлях до збереженого зображення з краями",
    )
    parser.add_argument("--threshold1", type=float, default=80.0, help="Нижній поріг Canny")
    parser.add_argument("--threshold2", type=float, default=160.0, help="Верхній поріг Canny")
    parser.add_argument("--blur-kernel", type=int, default=5, help="Розмір ядра GaussianBlur (непарний)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.blur_kernel < 1 or args.blur_kernel % 2 == 0:
        raise ValueError("blur-kernel має бути непарним додатним числом")

    image = cv2.imread(args.input)
    if image is None:
        raise FileNotFoundError(f"Не вдалося відкрити файл: {args.input}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (args.blur_kernel, args.blur_kernel), 0)
    edges = cv2.Canny(blurred, args.threshold1, args.threshold2)

    overlay = image.copy()
    overlay[edges > 0] = (0, 255, 255)

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(args.output, edges):
        raise IOError(f"Не вдалося зберегти файл: {args.output}")

    cv2.imshow("Original", image)
    cv2.imshow("Edges (Canny)", edges)
    cv2.imshow("Edges overlay", overlay)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
