import argparse
from pathlib import Path

import cv2
import numpy as np


class DropletDetector:
    def __init__(
        self,
        input_path: str,
        output_path: str,
        min_area: float,
        max_area: float,
        min_circularity: float,
        invert: bool,
    ) -> None:
        self.input_path = input_path
        self.output_path = output_path
        self.min_area = min_area
        self.max_area = max_area
        self.min_circularity = min_circularity
        self.invert = invert

        self.image = None
        self.binary = None
        self.droplets: list[np.ndarray] = []
        self.result = None

    def read(self) -> None:
        self.image = cv2.imread(self.input_path)
        if self.image is None:
            raise FileNotFoundError(f"Не вдалося відкрити файл: {self.input_path}")

    def preprocess(self) -> None:
        if self.image is None:
            raise RuntimeError("Зображення не прочитано")

        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh_type = cv2.THRESH_BINARY_INV if self.invert else cv2.THRESH_BINARY
        _, binary = cv2.threshold(blurred, 0, 255, thresh_type | cv2.THRESH_OTSU)

        kernel = np.ones((3, 3), dtype=np.uint8)
        self.binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)

    def detect(self) -> None:
        if self.binary is None:
            raise RuntimeError("Бінаризація ще не виконана")

        contours, _ = cv2.findContours(self.binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        filtered: list[np.ndarray] = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < self.min_area or area > self.max_area:
                continue

            perimeter = cv2.arcLength(contour, True)
            if perimeter <= 0:
                continue

            circularity = 4.0 * np.pi * area / (perimeter * perimeter)
            if circularity < self.min_circularity:
                continue

            filtered.append(contour)

        self.droplets = filtered

    def draw(self) -> None:
        if self.image is None:
            raise RuntimeError("Зображення не прочитано")

        result = self.image.copy()
        cv2.drawContours(result, self.droplets, -1, (0, 255, 0), 2)

        for contour in self.droplets:
            moments = cv2.moments(contour)
            if moments["m00"] == 0:
                continue
            cx = int(moments["m10"] / moments["m00"])
            cy = int(moments["m01"] / moments["m00"])
            cv2.circle(result, (cx, cy), 2, (0, 0, 255), -1)

        cv2.putText(
            result,
            f"Droplets: {len(self.droplets)}",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (0, 255, 255),
            2,
            cv2.LINE_AA,
        )

        self.result = result

    def save(self) -> None:
        if self.result is None:
            raise RuntimeError("Результат ще не сформовано")

        Path(self.output_path).parent.mkdir(parents=True, exist_ok=True)
        if not cv2.imwrite(self.output_path, self.result):
            raise IOError(f"Не вдалося зберегти файл: {self.output_path}")

    def show(self) -> None:
        if self.binary is None or self.result is None:
            raise RuntimeError("Немає даних для відображення")

        cv2.imshow("Binary", self.binary)
        cv2.imshow("Droplets detected (OOP)", self.result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def execute(self) -> None:
        self.read()
        self.preprocess()
        self.detect()
        self.draw()
        self.save()
        self.show()



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="ООП: виявлення крапель на зображенні"
    )
    parser.add_argument("--input", default="lab9/image.jpg", help="Шлях до вхідного зображення")
    parser.add_argument(
        "--output",
        default="lab9/droplets_detected_oop.jpg",
        help="Шлях до зображення з виявленими краплями",
    )
    parser.add_argument("--min-area", type=float, default=30.0, help="Мінімальна площа краплі")
    parser.add_argument("--max-area", type=float, default=10000.0, help="Максимальна площа краплі")
    parser.add_argument(
        "--min-circularity",
        type=float,
        default=0.3,
        help="Мінімальна круглість краплі (0..1)",
    )
    parser.add_argument(
        "--invert",
        action="store_true",
        help="Інвертувати поріг, якщо краплі темні на світлому фоні",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    app = DropletDetector(
        input_path=args.input,
        output_path=args.output,
        min_area=args.min_area,
        max_area=args.max_area,
        min_circularity=args.min_circularity,
        invert=args.invert,
    )
    app.execute()


if __name__ == "__main__":
    main()
