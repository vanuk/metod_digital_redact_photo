import argparse
from pathlib import Path

import cv2


class InteractiveImageApp:
    def __init__(self, input_path: str, output_path: str) -> None:
        self.input_path = input_path
        self.output_path = output_path
        self.window_name = "Interactive Processing (OOP)"
        self.image = None
        self.current = None
        self.click = None
        self.pixel_text = ""

    @staticmethod
    def _noop(_: int) -> None:
        pass

    def read(self) -> None:
        self.image = cv2.imread(self.input_path)
        if self.image is None:
            raise FileNotFoundError(f"Не вдалося відкрити файл: {self.input_path}")

    def on_mouse(self, event: int, x: int, y: int, _flags: int, _param: object) -> None:
        if event != cv2.EVENT_LBUTTONDOWN:
            return
        if self.image is None:
            return

        b, g, r = self.image[y, x]
        self.click = (x, y)
        self.pixel_text = f"x={x}, y={y}, BGR=({int(b)},{int(g)},{int(r)})"

    def setup_gui(self) -> None:
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.setMouseCallback(self.window_name, self.on_mouse)

        cv2.createTrackbar("Brightness", self.window_name, 100, 200, self._noop)
        cv2.createTrackbar("Contrast x100", self.window_name, 100, 300, self._noop)
        cv2.createTrackbar("Blur", self.window_name, 2, 20, self._noop)
        cv2.createTrackbar("Show edges", self.window_name, 0, 1, self._noop)

    def process_frame(self) -> None:
        if self.image is None:
            raise RuntimeError("Зображення не прочитано")

        brightness_raw = cv2.getTrackbarPos("Brightness", self.window_name)
        contrast_raw = cv2.getTrackbarPos("Contrast x100", self.window_name)
        blur_raw = cv2.getTrackbarPos("Blur", self.window_name)
        show_edges = cv2.getTrackbarPos("Show edges", self.window_name)

        beta = brightness_raw - 100
        alpha = max(0.01, contrast_raw / 100.0)
        blur_size = blur_raw * 2 + 1

        adjusted = cv2.convertScaleAbs(self.image, alpha=alpha, beta=beta)
        blurred = cv2.GaussianBlur(adjusted, (blur_size, blur_size), 0)

        if show_edges:
            gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 80, 160)
            self.current = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        else:
            self.current = blurred

        if self.click is not None:
            x, y = self.click
            cv2.circle(self.current, (x, y), 4, (0, 255, 255), -1)
            cv2.putText(
                self.current,
                self.pixel_text,
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 255),
                2,
                cv2.LINE_AA,
            )

        cv2.putText(
            self.current,
            "q: exit | s: save | click: pixel info",
            (10, self.current.shape[0] - 15),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            1,
            cv2.LINE_AA,
        )

    def save(self) -> None:
        if self.current is None:
            raise RuntimeError("Немає зображення для збереження")

        Path(self.output_path).parent.mkdir(parents=True, exist_ok=True)
        if not cv2.imwrite(self.output_path, self.current):
            raise IOError(f"Не вдалося зберегти файл: {self.output_path}")

    def run(self) -> None:
        self.read()
        self.setup_gui()

        while True:
            self.process_frame()
            cv2.imshow(self.window_name, self.current)

            key = cv2.waitKey(30) & 0xFF
            if key == ord("q"):
                break
            if key == ord("s"):
                self.save()

        cv2.destroyAllWindows()



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="ООП OpenCV-програма з GUI-взаємодією"
    )
    parser.add_argument("--input", default="lab11/image.jpg", help="Шлях до вхідного зображення")
    parser.add_argument(
        "--output",
        default="lab11/interactive_result_oop.jpg",
        help="Куди зберегти результат (клавіша s)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    app = InteractiveImageApp(input_path=args.input, output_path=args.output)
    app.run()


if __name__ == "__main__":
    main()
