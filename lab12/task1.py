import argparse
from pathlib import Path

import cv2


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Визначення контурів об'єктів на зображенні (процедурний підхід)"
    )
    parser.add_argument("--input", default="lab12/image.jpg", help="Шлях до вхідного зображення")
    parser.add_argument(
        "--output",
        default="lab12/contours.jpg",
        help="Шлях до зображення з контурами",
    )
    parser.add_argument(
        "--min-area",
        type=float,
        default=50.0,
        help="Мінімальна площа контуру для відображення",
    )
    parser.add_argument(
        "--invert",
        action="store_true",
        help="Інвертувати поріг для темних об'єктів на світлому фоні",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    image = cv2.imread(args.input)
    if image is None:
        raise FileNotFoundError(f"Не вдалося відкрити файл: {args.input}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    thresh_type = cv2.THRESH_BINARY_INV if args.invert else cv2.THRESH_BINARY
    _, binary = cv2.threshold(blurred, 0, 255, thresh_type | cv2.THRESH_OTSU)

    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    filtered = [cnt for cnt in contours if cv2.contourArea(cnt) >= args.min_area]

    result = image.copy()
    cv2.drawContours(result, filtered, -1, (0, 255, 0), 2)

    for i, contour in enumerate(filtered, start=1):
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(result, (x, y), (x + w, y + h), (255, 0, 0), 1)
        cv2.putText(
            result,
            str(i),
            (x, y - 5 if y > 15 else y + 15),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 255),
            1,
            cv2.LINE_AA,
        )

    cv2.putText(
        result,
        f"Contours: {len(filtered)}",
        (15, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 255),
        2,
        cv2.LINE_AA,
    )

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(args.output, result):
        raise IOError(f"Не вдалося зберегти файл: {args.output}")

    cv2.imshow("Binary", binary)
    cv2.imshow("Contours", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
