import argparse
from pathlib import Path

import cv2


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Коментування зображення фігурами OpenCV (лінія, прямокутник, коло, стрілка)"
    )
    parser.add_argument("--input", default="lab6/image.jpg", help="Шлях до вхідного зображення")
    parser.add_argument(
        "--output",
        default="lab6/annotated_shapes.jpg",
        help="Шлях для збереження зображення з коментарями",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    image = cv2.imread(args.input)
    if image is None:
        raise FileNotFoundError(f"Не вдалося відкрити файл: {args.input}")

    h, w = image.shape[:2]

    cv2.line(image, (int(0.05 * w), int(0.1 * h)), (int(0.95 * w), int(0.1 * h)), (0, 0, 255), 2)
    cv2.rectangle(image, (int(0.1 * w), int(0.2 * h)), (int(0.45 * w), int(0.55 * h)), (0, 255, 0), 2)
    cv2.circle(image, (int(0.75 * w), int(0.35 * h)), int(0.12 * min(w, h)), (255, 0, 0), 2)
    cv2.arrowedLine(
        image,
        (int(0.15 * w), int(0.8 * h)),
        (int(0.45 * w), int(0.6 * h)),
        (0, 255, 255),
        3,
        tipLength=0.15,
    )

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(args.output, image):
        raise IOError(f"Не вдалося зберегти файл: {args.output}")

    cv2.imshow("Annotated by shapes", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
