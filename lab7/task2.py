import argparse
from pathlib import Path

import cv2
import numpy as np


class ImageFilterProcessor:
    def __init__(self, input_path: str, output_sharp: str, output_blur: str) -> None:
        self.input_path = input_path
        self.output_sharp = output_sharp
        self.output_blur = output_blur
        self.image = None
        self.sharpened = None
        self.blurred = None

        self.sharpen_kernel = np.array(
            [
                [0, -1, 0],
                [-1, 5, -1],
                [0, -1, 0],
            ],
            dtype=np.float32,
        )
        self.blur_kernel = np.ones((5, 5), dtype=np.float32) / 25.0

    def read(self) -> None:
        self.image = cv2.imread(self.input_path)
        if self.image is None:
            raise FileNotFoundError(f"Не вдалося відкрити файл: {self.input_path}")

    def apply_filters(self) -> None:
        if self.image is None:
            raise RuntimeError("Зображення ще не завантажено")

        self.sharpened = cv2.filter2D(self.image, ddepth=-1, kernel=self.sharpen_kernel)
        self.blurred = cv2.filter2D(self.image, ddepth=-1, kernel=self.blur_kernel)

    def save(self) -> None:
        if self.sharpened is None or self.blurred is None:
            raise RuntimeError("Фільтрація ще не виконана")

        Path(self.output_sharp).parent.mkdir(parents=True, exist_ok=True)
        Path(self.output_blur).parent.mkdir(parents=True, exist_ok=True)

        if not cv2.imwrite(self.output_sharp, self.sharpened):
            raise IOError(f"Не вдалося зберегти файл: {self.output_sharp}")
        if not cv2.imwrite(self.output_blur, self.blurred):
            raise IOError(f"Не вдалося зберегти файл: {self.output_blur}")

    def show(self) -> None:
        if self.image is None or self.sharpened is None or self.blurred is None:
            raise RuntimeError("Немає даних для відображення")

        cv2.imshow("Original", self.image)
        cv2.imshow("Sharpened (OOP)", self.sharpened)
        cv2.imshow("Blurred (OOP)", self.blurred)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def execute(self) -> None:
        self.read()
        self.apply_filters()
        self.save()
        self.show()



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "ООП: покращення зображення за рахунок коректування різкості та "
            "розмитості з використанням ядер згорток"
        )
    )
    parser.add_argument("--input", default="lab7/image.jpg", help="Шлях до вхідного зображення")
    parser.add_argument(
        "--output-sharp",
        default="lab7/sharpened_oop.jpg",
        help="Шлях до збереженого різкого зображення",
    )
    parser.add_argument(
        "--output-blur",
        default="lab7/blurred_oop.jpg",
        help="Шлях до збереженого розмитого зображення",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    app = ImageFilterProcessor(
        input_path=args.input,
        output_sharp=args.output_sharp,
        output_blur=args.output_blur,
    )
    app.execute()


if __name__ == "__main__":
    main()
