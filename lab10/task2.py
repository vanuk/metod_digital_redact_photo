import argparse
from pathlib import Path

import cv2


class EdgeDetector:
    def __init__(
        self,
        input_path: str,
        output_path: str,
        threshold1: float,
        threshold2: float,
        blur_kernel: int,
    ) -> None:
        self.input_path = input_path
        self.output_path = output_path
        self.threshold1 = threshold1
        self.threshold2 = threshold2
        self.blur_kernel = blur_kernel

        self.image = None
        self.edges = None
        self.overlay = None

    def read(self) -> None:
        self.image = cv2.imread(self.input_path)
        if self.image is None:
            raise FileNotFoundError(f"Не вдалося відкрити файл: {self.input_path}")

    def detect(self) -> None:
        if self.image is None:
            raise RuntimeError("Зображення не прочитано")
        if self.blur_kernel < 1 or self.blur_kernel % 2 == 0:
            raise ValueError("blur-kernel має бути непарним додатним числом")

        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (self.blur_kernel, self.blur_kernel), 0)
        self.edges = cv2.Canny(blurred, self.threshold1, self.threshold2)

    def build_overlay(self) -> None:
        if self.image is None or self.edges is None:
            raise RuntimeError("Немає даних для створення накладання")

        overlay = self.image.copy()
        overlay[self.edges > 0] = (0, 255, 255)
        self.overlay = overlay

    def save(self) -> None:
        if self.edges is None:
            raise RuntimeError("Краї ще не виявлено")

        Path(self.output_path).parent.mkdir(parents=True, exist_ok=True)
        if not cv2.imwrite(self.output_path, self.edges):
            raise IOError(f"Не вдалося зберегти файл: {self.output_path}")

    def show(self) -> None:
        if self.image is None or self.edges is None or self.overlay is None:
            raise RuntimeError("Немає даних для відображення")

        cv2.imshow("Original", self.image)
        cv2.imshow("Edges (Canny, OOP)", self.edges)
        cv2.imshow("Edges overlay (OOP)", self.overlay)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def execute(self) -> None:
        self.read()
        self.detect()
        self.build_overlay()
        self.save()
        self.show()



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="ООП: виявлення країв зображення (Canny)"
    )
    parser.add_argument("--input", default="lab10/image.jpg", help="Шлях до вхідного зображення")
    parser.add_argument(
        "--output",
        default="lab10/edges_oop.jpg",
        help="Шлях до збереженого зображення з краями",
    )
    parser.add_argument("--threshold1", type=float, default=80.0, help="Нижній поріг Canny")
    parser.add_argument("--threshold2", type=float, default=160.0, help="Верхній поріг Canny")
    parser.add_argument("--blur-kernel", type=int, default=5, help="Розмір ядра GaussianBlur (непарний)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    app = EdgeDetector(
        input_path=args.input,
        output_path=args.output,
        threshold1=args.threshold1,
        threshold2=args.threshold2,
        blur_kernel=args.blur_kernel,
    )
    app.execute()


if __name__ == "__main__":
    main()
