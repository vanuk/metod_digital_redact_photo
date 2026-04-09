import argparse
from pathlib import Path

import cv2
import numpy as np


class ImageTranslator:
    def __init__(self, input_path: str, output_path: str, tx: float, ty: float) -> None:
        self.input_path = input_path
        self.output_path = output_path
        self.tx = tx
        self.ty = ty
        self.image = None
        self.translated = None

    def read(self) -> None:
        self.image = cv2.imread(self.input_path)
        if self.image is None:
            raise FileNotFoundError(f"Не вдалося відкрити файл: {self.input_path}")

    def translate(self) -> None:
        if self.image is None:
            raise RuntimeError("Зображення не прочитано")

        h, w = self.image.shape[:2]
        matrix = np.float32([[1, 0, self.tx], [0, 1, self.ty]])
        self.translated = cv2.warpAffine(self.image, matrix, (w, h))

    def save(self) -> None:
        if self.translated is None:
            raise RuntimeError("Зміщене зображення ще не створено")

        Path(self.output_path).parent.mkdir(parents=True, exist_ok=True)
        if not cv2.imwrite(self.output_path, self.translated):
            raise IOError(f"Не вдалося зберегти файл: {self.output_path}")

    def show(self) -> None:
        if self.image is None or self.translated is None:
            raise RuntimeError("Дані для відображення відсутні")

        cv2.imshow("Original", self.image)
        cv2.imshow("Translated (OOP)", self.translated)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def execute(self) -> None:
        self.read()
        self.translate()
        self.save()
        self.show()



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="ООП: переміщення зображення")
    parser.add_argument("--input", default="lab5/image.jpg", help="Шлях до вхідного зображення")
    parser.add_argument(
        "--output",
        default="lab5/translated_oop.jpg",
        help="Шлях для збереження зміщеного зображення",
    )
    parser.add_argument("--tx", type=float, default=120.0, help="Зміщення по осі X")
    parser.add_argument("--ty", type=float, default=80.0, help="Зміщення по осі Y")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    app = ImageTranslator(
        input_path=args.input,
        output_path=args.output,
        tx=args.tx,
        ty=args.ty,
    )
    app.execute()


if __name__ == "__main__":
    main()
