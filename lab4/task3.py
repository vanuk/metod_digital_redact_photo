import argparse
from pathlib import Path

import cv2


class ImageCropper:
    def __init__(
        self,
        input_path: str,
        output_path: str,
        x: int,
        y: int,
        width: int,
        height: int,
    ) -> None:
        self.input_path = input_path
        self.output_path = output_path
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = None
        self.crop = None
        self.bounds = None

    def read(self) -> None:
        self.image = cv2.imread(self.input_path)
        if self.image is None:
            raise FileNotFoundError(f"Не вдалося відкрити файл: {self.input_path}")

    def crop_image(self) -> None:
        if self.image is None:
            raise RuntimeError("Зображення не прочитано")

        h, w = self.image.shape[:2]
        x1 = max(0, self.x)
        y1 = max(0, self.y)
        x2 = min(w, x1 + max(1, self.width))
        y2 = min(h, y1 + max(1, self.height))

        if x1 >= x2 or y1 >= y2:
            raise ValueError("Некоректна область обрізання")

        self.crop = self.image[y1:y2, x1:x2]
        self.bounds = (x1, y1, x2, y2)

    def save(self) -> None:
        if self.crop is None:
            raise RuntimeError("Фрагмент ще не отримано")

        Path(self.output_path).parent.mkdir(parents=True, exist_ok=True)
        if not cv2.imwrite(self.output_path, self.crop):
            raise IOError(f"Не вдалося зберегти файл: {self.output_path}")

    def show(self) -> None:
        if self.image is None or self.crop is None or self.bounds is None:
            raise RuntimeError("Дані для відображення відсутні")

        x1, y1, x2, y2 = self.bounds
        preview = self.image.copy()
        cv2.rectangle(preview, (x1, y1), (x2, y2), (0, 255, 0), 2)

        cv2.imshow("Original with ROI", preview)
        cv2.imshow("Crop (OOP)", self.crop)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def execute(self) -> None:
        self.read()
        self.crop_image()
        self.save()
        self.show()



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="ООП: отримання фрагмента зображення")
    parser.add_argument("--input", default="lab4/image.jpg", help="Шлях до вхідного зображення")
    parser.add_argument("--output", default="lab4/crop_oop.jpg", help="Шлях до вихідного фрагмента")
    parser.add_argument("--x", type=int, default=80, help="Координата X верхнього лівого кута")
    parser.add_argument("--y", type=int, default=80, help="Координата Y верхнього лівого кута")
    parser.add_argument("--width", type=int, default=250, help="Ширина фрагмента")
    parser.add_argument("--height", type=int, default=250, help="Висота фрагмента")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    app = ImageCropper(
        input_path=args.input,
        output_path=args.output,
        x=args.x,
        y=args.y,
        width=args.width,
        height=args.height,
    )
    app.execute()


if __name__ == "__main__":
    main()
