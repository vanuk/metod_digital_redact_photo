import argparse
from pathlib import Path

import cv2


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Розбиття зображення на менші фрагменти (сітка rows x cols)"
    )
    parser.add_argument("--input", default="lab4/image.jpg", help="Шлях до вхідного зображення")
    parser.add_argument(
        "--output-dir",
        default="lab4/fragments",
        help="Папка для збереження фрагментів",
    )
    parser.add_argument("--rows", type=int, default=2, help="Кількість рядків сітки")
    parser.add_argument("--cols", type=int, default=3, help="Кількість стовпців сітки")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.rows <= 0 or args.cols <= 0:
        raise ValueError("rows і cols мають бути більше 0")

    image = cv2.imread(args.input)
    if image is None:
        raise FileNotFoundError(f"Не вдалося відкрити файл: {args.input}")

    h, w = image.shape[:2]
    tile_h = h // args.rows
    tile_w = w // args.cols

    if tile_h == 0 or tile_w == 0:
        raise ValueError("Занадто велика кількість фрагментів для цього зображення")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    preview = image.copy()

    for row in range(args.rows):
        for col in range(args.cols):
            y1 = row * tile_h
            x1 = col * tile_w

            # Останній рядок/стовпець забирає залишок пікселів.
            y2 = (row + 1) * tile_h if row < args.rows - 1 else h
            x2 = (col + 1) * tile_w if col < args.cols - 1 else w

            tile = image[y1:y2, x1:x2]
            tile_name = output_dir / f"fragment_r{row}_c{col}.jpg"
            if not cv2.imwrite(str(tile_name), tile):
                raise IOError(f"Не вдалося зберегти фрагмент: {tile_name}")

            cv2.rectangle(preview, (x1, y1), (x2, y2), (0, 255, 255), 1)

    cv2.imshow("Image split preview", preview)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
