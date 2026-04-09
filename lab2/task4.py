import argparse
import cv2


class WebcamRecorder:
    def __init__(
        self,
        camera_index: int,
        output_path: str,
        fps: float,
        window_name: str,
    ) -> None:
        self.camera_index = camera_index
        self.output_path = output_path
        self.fps = fps
        self.window_name = window_name
        self.capture: cv2.VideoCapture | None = None
        self.writer: cv2.VideoWriter | None = None

    def open(self) -> None:
        self.capture = cv2.VideoCapture(self.camera_index)
        if not self.capture.isOpened():
            raise RuntimeError(
                f"Не вдалося відкрити вебкамеру з індексом {self.camera_index}"
            )

        width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        if width <= 0 or height <= 0:
            width, height = 640, 480

        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        self.writer = cv2.VideoWriter(self.output_path, fourcc, self.fps, (width, height))
        if not self.writer.isOpened():
            self.capture.release()
            self.capture = None
            raise RuntimeError(f"Не вдалося створити файл для запису: {self.output_path}")

    def run(self) -> None:
        if self.capture is None or self.writer is None:
            raise RuntimeError("Вебкамера або відеозапис не ініціалізовані")

        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)

        while True:
            ret, frame = self.capture.read()
            if not ret:
                break

            self.writer.write(frame)
            cv2.imshow(self.window_name, frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    def close(self) -> None:
        if self.writer is not None:
            self.writer.release()
        if self.capture is not None:
            self.capture.release()
        cv2.destroyAllWindows()

    def execute(self) -> None:
        self.open()
        try:
            self.run()
        finally:
            self.close()



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="ООП: читання, відображення та збереження відео з вебкамери"
    )
    parser.add_argument(
        "--camera-index",
        type=int,
        default=0,
        help="Індекс вебкамери (за замовчуванням: 0)",
    )
    parser.add_argument(
        "--output",
        default="lab2/webcam_output_oop.mp4",
        help="Шлях до вихідного відеофайлу (за замовчуванням: lab2/webcam_output_oop.mp4)",
    )
    parser.add_argument(
        "--fps",
        type=float,
        default=20.0,
        help="FPS для збереження відео (за замовчуванням: 20.0)",
    )
    parser.add_argument(
        "--window",
        default="Webcam (OOP)",
        help="Назва вікна для відображення",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    recorder = WebcamRecorder(
        camera_index=args.camera_index,
        output_path=args.output,
        fps=args.fps,
        window_name=args.window,
    )
    recorder.execute()


if __name__ == "__main__":
    main()
