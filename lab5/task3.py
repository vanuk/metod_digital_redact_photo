import argparse
from pathlib import Path

import cv2


class ImageRotator:
    def __init__(self, input_path: str, output_path: str, angle: float, scale: float) -> None:
        self.input_path = input_path
        self.output_path = output_path
        self.angle = angle
        self.scale = scale
        self.image = None
        self.rotated = None

    def read(self) -> None:
        self.image = cv2.imread(self.input_path)
        if self.image is None:
            raise FileNotFoundError(f"Не вдалося відкрити файл: {self.input_path}")

    def rotate(self) -> None:
        if self.image is None:
            raise RuntimeError("Зображення не прочитано")

        h, w = self.image.shape[:2]
        center = (w // 2, h // 2)
        matrix = cv2.getRotationMatrix2D(center, self.angle, self.scale)
        self.rotated = cv2.warpAffine(self.image, matrix, (w, h))

    def save(self) -> None:
        if self.rotated is None:
            raise RuntimeError("Повернуте зображення ще не створено")

        Path(self.output_path).parent.mkdir(parents=True, exist_ok=True)
        if not cv2.imwrite(self.output_path, self.rotated):
            raise IOError(f"Не вдалося зберегти файл: {self.output_path}")

    def show(self) -> None:
        if self.image is None or self.rotated is None:
            raise RuntimeError("Дані для відображення відсутні")

        cv2.imshow("Original", self.image)
        cv2.imshow("Rotated (OOP)", self.rotated)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def execute(self) -> None:
        self.read()
        self.rotate()
        self.save()
        self.show()



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="ООП: обертання зображення")
    parser.add_argument("--input", default="lab5/image.jpg", help="Шлях до вхідного зображення")
    parser.add_argument(
        "--output",
        default="lab5/rotated_oop.jpg",
        help="Шлях для збереження повернутого зображення",
    )
    parser.add_argument("--angle", type=float, default=30.0, help="Кут обертання в градусах")
    parser.add_argument("--scale", type=float, default=1.0, help="Масштаб при обертанні")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    app = ImageRotator(
        input_path=args.input,
        output_path=args.output,
        angle=args.angle,
        scale=args.scale,
    )
    app.execute()


if __name__ == "__main__":
    main()
