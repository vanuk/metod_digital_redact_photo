import argparse
import cv2


class VideoFilePlayer:
    def __init__(self, video_path: str, window_name: str) -> None:
        self.video_path = video_path
        self.window_name = window_name
        self.capture: cv2.VideoCapture | None = None

    def open(self) -> None:
        self.capture = cv2.VideoCapture(self.video_path)
        if not self.capture.isOpened():
            raise FileNotFoundError(f"Не вдалося відкрити відеофайл: {self.video_path}")

    def show(self) -> None:
        if self.capture is None:
            raise RuntimeError("Відеофайл не ініціалізовано")

        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)

        while True:
            ret, frame = self.capture.read()
            if not ret:
                break

            cv2.imshow(self.window_name, frame)

            # Натисніть q для завершення перегляду.
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    def close(self) -> None:
        if self.capture is not None:
            self.capture.release()
        cv2.destroyAllWindows()

    def execute(self) -> None:
        self.open()
        try:
            self.show()
        finally:
            self.close()



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="ООП: читання та відображення відеофайлу за допомогою OpenCV"
    )
    parser.add_argument(
        "--video",
        default="lab2/video.mp4",
        help="Шлях до вхідного відеофайлу (за замовчуванням: lab2/video.mp4)",
    )
    parser.add_argument(
        "--window",
        default="Video file (OOP)",
        help="Назва вікна для відображення",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    player = VideoFilePlayer(video_path=args.video, window_name=args.window)
    player.execute()


if __name__ == "__main__":
    main()
