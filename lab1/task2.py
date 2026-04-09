import cv2


class GrayscaleImageProcessor:
    def __init__(self, input_path: str, output_path: str, window_name: str) -> None:
        self.input_path = input_path
        self.output_path = output_path
        self.window_name = window_name
        self.image = None

    def read_grayscale(self) -> None:
        self.image = cv2.imread(self.input_path, cv2.IMREAD_GRAYSCALE)
        if self.image is None:
            raise FileNotFoundError(f"Не вдалося відкрити файл {self.input_path}")

    def save_image(self) -> None:
        if self.image is None:
            raise ValueError("Зображення не завантажено")

        is_saved = cv2.imwrite(self.output_path, self.image)
        if not is_saved:
            raise IOError(f"Не вдалося зберегти файл {self.output_path}")

    def show_image(self) -> None:
        if self.image is None:
            raise ValueError("Зображення не завантажено")

        cv2.namedWindow(self.window_name, cv2.WINDOW_AUTOSIZE)
        cv2.imshow(self.window_name, self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def execute(self) -> None:
        self.read_grayscale()
        self.save_image()
        self.show_image()


if __name__ == "__main__":
    processor = GrayscaleImageProcessor(
        input_path="lab1/2.jpg",
        output_path="lab1/2image_grayscale.jpeg",
        window_name="Grayscale image",
    )
    processor.execute()
