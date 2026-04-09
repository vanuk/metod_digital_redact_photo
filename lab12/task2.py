import argparse
from pathlib import Path

import cv2


class ContourDetector:
    def __init__(self, input_path: str, output_path: str, min_area: float, invert: bool) -> None:
        self.input_path = input_path
        self.output_path = output_path
        self.min_area = min_area
        self.invert = invert

        self.image = None
        self.binary = None
        self.filtered_contours = []
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
        _, self.binary = cv2.threshold(blurred, 0, 255, thresh_type | cv2.THRESH_OTSU)

    def detect(self) -> None:
        if self.binary is None:
            raise RuntimeError("Бінаризація ще не виконана")

        contours, _ = cv2.findContours(self.binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) >= self.min_area]

    def draw(self) -> None:
        if self.image is None:
            raise RuntimeError("Зображення не прочитано")

        result = self.image.copy()
        cv2.drawContours(result, self.filtered_contours, -1, (0, 255, 0), 2)

        for i, contour in enumerate(self.filtered_contours, start=1):
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(result, (x, y), (x + w, y + h), (255, 0, 0), 1)
            cv2.putText(
                result,
                str(i),
                (x, y - 5 if y > 15 else y + 15),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 255),
                1,
                cv2.LINE_AA,
            )

        cv2.putText(
            result,
            f"Contours: {len(self.filtered_contours)}",
            (15, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
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
        cv2.imshow("Contours (OOP)", self.result)
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
        description="ООП: визначення контурів об'єктів на зображенні"
    )
    parser.add_argument("--input", default="lab12/image.jpg", help="Шлях до вхідного зображення")
    parser.add_argument(
        "--output",
        default="lab12/contours_oop.jpg",
        help="Шлях до зображення з контурами",
    )
    parser.add_argument(
        "--min-area",
        type=float,
        default=50.0,
        help="Мінімальна площа контуру для відображення",
    )
    parser.add_argument(
        "--invert",
        action="store_true",
        help="Інвертувати поріг для темних об'єктів на світлому фоні",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    app = ContourDetector(
        input_path=args.input,
        output_path=args.output,
        min_area=args.min_area,
        invert=args.invert,
    )
    app.execute()


if __name__ == "__main__":
    main()
