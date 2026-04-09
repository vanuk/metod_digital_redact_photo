import argparse
import cv2


INTERPOLATIONS = {
    "nearest": cv2.INTER_NEAREST,
    "linear": cv2.INTER_LINEAR,
    "cubic": cv2.INTER_CUBIC,
    "area": cv2.INTER_AREA,
    "lanczos4": cv2.INTER_LANCZOS4,
}


class ImageResizerByScale:
    def __init__(
        self,
        input_path: str,
        output_path: str,
        fx: float,
        fy: float,
        interpolation_name: str,
    ) -> None:
        self.input_path = input_path
        self.output_path = output_path
        self.fx = fx
        self.fy = fy
        self.interpolation_name = interpolation_name
        self.image = None
        self.resized = None

    def read(self) -> None:
        self.image = cv2.imread(self.input_path)
        if self.image is None:
            raise FileNotFoundError(f"Не вдалося відкрити файл: {self.input_path}")

    def resize(self) -> None:
        if self.image is None:
            raise RuntimeError("Зображення ще не прочитано")
        interpolation = INTERPOLATIONS[self.interpolation_name]
        self.resized = cv2.resize(
            self.image,
            None,
            fx=self.fx,
            fy=self.fy,
            interpolation=interpolation,
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
        cv2.imshow("Resized (OOP scale/interpolation)", self.resized)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def execute(self) -> None:
        self.read()
        self.resize()
        self.save()
        self.show()



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="ООП: зміна розміру за коефіцієнтом масштабування та інтерполяцією"
    )
    parser.add_argument("--input", default="lab3/image.jpg", help="Шлях до вхідного зображення")
    parser.add_argument(
        "--output",
        default="lab3/resized_scale_oop.jpg",
        help="Шлях для збереження зміненого зображення",
    )
    parser.add_argument("--fx", type=float, default=1.5, help="Коефіцієнт масштабування по X")
    parser.add_argument("--fy", type=float, default=1.5, help="Коефіцієнт масштабування по Y")
    parser.add_argument(
        "--interpolation",
        choices=list(INTERPOLATIONS.keys()),
        default="cubic",
        help="Метод інтерполяції",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    processor = ImageResizerByScale(
        input_path=args.input,
        output_path=args.output,
        fx=args.fx,
        fy=args.fy,
        interpolation_name=args.interpolation,
    )
    processor.execute()


if __name__ == "__main__":
    main()
