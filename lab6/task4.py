import argparse
from pathlib import Path

import cv2


class TextAnnotator:
    def __init__(
        self,
        input_path: str,
        output_path: str,
        text: str,
        x: int,
        y: int,
        scale: float,
        thickness: int,
    ) -> None:
        self.input_path = input_path
        self.output_path = output_path
        self.text = text
        self.x = x
        self.y = y
        self.scale = scale
        self.thickness = thickness
        self.image = None

    def read(self) -> None:
        self.image = cv2.imread(self.input_path)
        if self.image is None:
            raise FileNotFoundError(f"Не вдалося відкрити файл: {self.input_path}")

    def annotate(self) -> None:
        if self.image is None:
            raise RuntimeError("Зображення не прочитано")

        cv2.putText(
            self.image,
            self.text,
            (self.x, self.y),
            cv2.FONT_HERSHEY_COMPLEX,
            self.scale,
            (0, 255, 255),
            self.thickness,
            cv2.LINE_AA,
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

        cv2.imshow("Annotated by text (OOP)", self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def execute(self) -> None:
        self.read()
        self.annotate()
        self.save()
        self.show()



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="ООП: коментування зображення текстом")
    parser.add_argument("--input", default="lab6/image.jpg", help="Шлях до вхідного зображення")
    parser.add_argument(
        "--output",
        default="lab6/annotated_text_oop.jpg",
        help="Шлях для збереження зображення з текстом",
    )
    parser.add_argument("--text", default="OpenCV OOP annotation", help="Текст для нанесення")
    parser.add_argument("--x", type=int, default=50, help="Позиція X тексту")
    parser.add_argument("--y", type=int, default=80, help="Позиція Y тексту")
    parser.add_argument("--scale", type=float, default=1.0, help="Масштаб шрифту")
    parser.add_argument("--thickness", type=int, default=2, help="Товщина тексту")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    app = TextAnnotator(
        input_path=args.input,
        output_path=args.output,
        text=args.text,
        x=args.x,
        y=args.y,
        scale=args.scale,
        thickness=args.thickness,
    )
    app.execute()


if __name__ == "__main__":
    main()
