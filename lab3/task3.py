import argparse
import cv2


class ImageResizerBySize:
    def __init__(self, input_path: str, output_path: str, width: int, height: int) -> None:
        self.input_path = input_path
        self.output_path = output_path
        self.width = width
        self.height = height
        self.image = None
        self.resized = None

    def read(self) -> None:
        self.image = cv2.imread(self.input_path)
        if self.image is None:
            raise FileNotFoundError(f"Не вдалося відкрити файл: {self.input_path}")

    def resize(self) -> None:
        if self.image is None:
            raise RuntimeError("Зображення ще не прочитано")
        self.resized = cv2.resize(
            self.image,
            (self.width, self.height),
            interpolation=cv2.INTER_LINEAR,
        )

    def save(self) -> None:
        if self.resized is None:
            raise RuntimeError("Змінене зображення ще не отримано")
        is_saved = cv2.imwrite(self.output_path, self.resized)
        if not is_saved:
            raise IOError(f"Не вдалося зберегти файл: {self.output_path}")

    def show(self) -> None:
        if self.image is None or self.resized is None:
            raise RuntimeError("Дані для відображення відсутні")
        cv2.imshow("Original", self.image)
        cv2.imshow("Resized (OOP width/height)", self.resized)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def execute(self) -> None:
        self.read()
        self.resize()
        self.save()
        self.show()



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="ООП: зміна розміру зображення за width та height"
    )
    parser.add_argument("--input", default="lab3/image.jpg", help="Шлях до вхідного зображення")
    parser.add_argument(
        "--output",
        default="lab3/resized_wh_oop.jpg",
        help="Шлях для збереження зміненого зображення",
    )
    parser.add_argument("--width", type=int, default=1024, help="Нова ширина")
    parser.add_argument("--height", type=int, default=768, help="Нова висота")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    processor = ImageResizerBySize(
        input_path=args.input,
        output_path=args.output,
        width=args.width,
        height=args.height,
    )
    processor.execute()


if __name__ == "__main__":
    main()
