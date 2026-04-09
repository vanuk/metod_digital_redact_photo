import argparse
from pathlib import Path

import cv2


class ShapeAnnotator:
    def __init__(self, input_path: str, output_path: str) -> None:
        self.input_path = input_path
        self.output_path = output_path
        self.image = None

    def read(self) -> None:
        self.image = cv2.imread(self.input_path)
        if self.image is None:
            raise FileNotFoundError(f"Не вдалося відкрити файл: {self.input_path}")

    def annotate(self) -> None:
        if self.image is None:
            raise RuntimeError("Зображення не прочитано")

        h, w = self.image.shape[:2]
        cv2.line(self.image, (int(0.05 * w), int(0.12 * h)), (int(0.95 * w), int(0.12 * h)), (255, 255, 0), 2)
        cv2.rectangle(self.image, (int(0.08 * w), int(0.2 * h)), (int(0.4 * w), int(0.55 * h)), (0, 255, 0), 2)
        cv2.circle(self.image, (int(0.72 * w), int(0.38 * h)), int(0.1 * min(w, h)), (0, 0, 255), 2)
        cv2.ellipse(
            self.image,
            (int(0.7 * w), int(0.75 * h)),
            (int(0.15 * w), int(0.08 * h)),
            0,
            0,
            300,
            (255, 0, 255),
            2,
        )

    def save(self) -> None:
        if self.image is None:
            raise RuntimeError("Немає даних для збереження")

        Path(self.output_path).parent.mkdir(parents=True, exist_ok=True)
        if not cv2.imwrite(self.output_path, self.image):
            raise IOError(f"Не вдалося зберегти файл: {self.output_path}")

    def show(self) -> None:
        if self.image is None:
            raise RuntimeError("Немає даних для відображення")

        cv2.imshow("Annotated by shapes (OOP)", self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def execute(self) -> None:
        self.read()
        self.annotate()
        self.save()
        self.show()



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="ООП: коментування зображення фігурами OpenCV"
    )
    parser.add_argument("--input", default="lab6/image.jpg", help="Шлях до вхідного зображення")
    parser.add_argument(
        "--output",
        default="lab6/annotated_shapes_oop.jpg",
        help="Шлях для збереження зображення з коментарями",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    app = ShapeAnnotator(input_path=args.input, output_path=args.output)
    app.execute()


if __name__ == "__main__":
    main()
