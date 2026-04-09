import argparse
from pathlib import Path

import cv2


class ImageSplitter:
    def __init__(self, input_path: str, output_dir: str, rows: int, cols: int) -> None:
        self.input_path = input_path
        self.output_dir = Path(output_dir)
        self.rows = rows
        self.cols = cols
        self.image = None

    def read(self) -> None:
        self.image = cv2.imread(self.input_path)
        if self.image is None:
            raise FileNotFoundError(f"Не вдалося відкрити файл: {self.input_path}")

    def split_and_save(self) -> None:
        if self.image is None:
            raise RuntimeError("Зображення не прочитано")
        if self.rows <= 0 or self.cols <= 0:
            raise ValueError("rows і cols мають бути більше 0")

        h, w = self.image.shape[:2]
        tile_h = h // self.rows
        tile_w = w // self.cols

        if tile_h == 0 or tile_w == 0:
            raise ValueError("Занадто велика кількість фрагментів для цього зображення")

        self.output_dir.mkdir(parents=True, exist_ok=True)

        for row in range(self.rows):
            for col in range(self.cols):
                y1 = row * tile_h
                x1 = col * tile_w
                y2 = (row + 1) * tile_h if row < self.rows - 1 else h
                x2 = (col + 1) * tile_w if col < self.cols - 1 else w

                tile = self.image[y1:y2, x1:x2]
                tile_path = self.output_dir / f"fragment_r{row}_c{col}.jpg"
                if not cv2.imwrite(str(tile_path), tile):
                    raise IOError(f"Не вдалося зберегти фрагмент: {tile_path}")

    def show_preview(self) -> None:
        if self.image is None:
            raise RuntimeError("Зображення не прочитано")

        h, w = self.image.shape[:2]
        tile_h = h // self.rows
        tile_w = w // self.cols

        preview = self.image.copy()
        for row in range(self.rows):
            for col in range(self.cols):
                y1 = row * tile_h
                x1 = col * tile_w
                y2 = (row + 1) * tile_h if row < self.rows - 1 else h
                x2 = (col + 1) * tile_w if col < self.cols - 1 else w
                cv2.rectangle(preview, (x1, y1), (x2, y2), (255, 255, 0), 1)

        cv2.imshow("Image split preview (OOP)", preview)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def execute(self) -> None:
        self.read()
        self.split_and_save()
        self.show_preview()



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="ООП: розбиття зображення на менші фрагменти"
    )
    parser.add_argument("--input", default="lab4/image.jpg", help="Шлях до вхідного зображення")
    parser.add_argument(
        "--output-dir",
        default="lab4/fragments_oop",
        help="Папка для збереження фрагментів",
    )
    parser.add_argument("--rows", type=int, default=3, help="Кількість рядків сітки")
    parser.add_argument("--cols", type=int, default=3, help="Кількість стовпців сітки")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    app = ImageSplitter(
        input_path=args.input,
        output_dir=args.output_dir,
        rows=args.rows,
        cols=args.cols,
    )
    app.execute()


if __name__ == "__main__":
    main()
