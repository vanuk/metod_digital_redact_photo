import argparse
from pathlib import Path

import cv2


THRESHOLD_TYPES = {
    "binary": cv2.THRESH_BINARY,
    "binary_inv": cv2.THRESH_BINARY_INV,
    "trunc": cv2.THRESH_TRUNC,
    "tozero": cv2.THRESH_TOZERO,
    "tozero_inv": cv2.THRESH_TOZERO_INV,
    "otsu": cv2.THRESH_BINARY | cv2.THRESH_OTSU,
}


class ThresholdProcessor:
    def __init__(
        self,
        input_path: str,
        output_path: str,
        threshold_type_name: str,
        threshold_value: float,
        max_value: float,
    ) -> None:
        self.input_path = input_path
        self.output_path = output_path
        self.threshold_type_name = threshold_type_name
        self.threshold_value = threshold_value
        self.max_value = max_value

        self.image = None
        self.result = None
        self.used_threshold = None

    def read(self) -> None:
        self.image = cv2.imread(self.input_path, cv2.IMREAD_GRAYSCALE)
        if self.image is None:
            raise FileNotFoundError(f"Не вдалося відкрити файл: {self.input_path}")

    def apply_threshold(self) -> None:
        if self.image is None:
            raise RuntimeError("Зображення не прочитано")

        threshold_type = THRESHOLD_TYPES[self.threshold_type_name]
        threshold_value = 0.0 if self.threshold_type_name == "otsu" else self.threshold_value

        self.used_threshold, self.result = cv2.threshold(
            self.image,
            threshold_value,
            self.max_value,
            threshold_type,
        )

    def save(self) -> None:
        if self.result is None:
            raise RuntimeError("Порогове перетворення ще не виконано")

        Path(self.output_path).parent.mkdir(parents=True, exist_ok=True)
        if not cv2.imwrite(self.output_path, self.result):
            raise IOError(f"Не вдалося зберегти файл: {self.output_path}")

    def show(self) -> None:
        if self.image is None or self.result is None or self.used_threshold is None:
            raise RuntimeError("Дані для відображення відсутні")

        cv2.imshow("Original (grayscale)", self.image)
        cv2.imshow(
            f"Threshold result (OOP: {self.threshold_type_name}, t={self.used_threshold:.2f})",
            self.result,
        )
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def execute(self) -> None:
        self.read()
        self.apply_threshold()
        self.save()
        self.show()



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="ООП: застосування порогового перетворення до зображення"
    )
    parser.add_argument("--input", default="lab8/image.jpg", help="Шлях до вхідного зображення")
    parser.add_argument(
        "--output",
        default="lab8/threshold_result_oop.jpg",
        help="Шлях до збереженого результату",
    )
    parser.add_argument(
        "--type",
        choices=list(THRESHOLD_TYPES.keys()),
        default="otsu",
        help="Тип порогового перетворення",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=127.0,
        help="Порогове значення (для otsu ігнорується)",
    )
    parser.add_argument(
        "--max-value",
        type=float,
        default=255.0,
        help="Максимальне значення для пікселів після перетворення",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    app = ThresholdProcessor(
        input_path=args.input,
        output_path=args.output,
        threshold_type_name=args.type,
        threshold_value=args.threshold,
        max_value=args.max_value,
    )
    app.execute()


if __name__ == "__main__":
    main()
