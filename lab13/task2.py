import argparse
from pathlib import Path

import cv2
import numpy as np


class BackgroundMotionDetector:
    def __init__(
        self,
        input_path: str,
        output_path: str,
        samples: int,
        threshold: int,
        min_area: float,
    ) -> None:
        self.input_path = input_path
        self.output_path = output_path
        self.samples = samples
        self.threshold = threshold
        self.min_area = min_area

        self.cap = None
        self.writer = None
        self.background_gray = None

    def open(self) -> None:
        self.cap = cv2.VideoCapture(self.input_path)
        if not self.cap.isOpened():
            raise FileNotFoundError(f"Не вдалося відкрити відео: {self.input_path}")

    def estimate_background(self) -> None:
        if self.cap is None:
            raise RuntimeError("Відео не відкрито")

        frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if frame_count <= 0:
            raise RuntimeError("Не вдалося визначити кількість кадрів у відео")

        sample_count = max(1, min(self.samples, frame_count))
        indices = np.linspace(0, frame_count - 1, sample_count, dtype=np.int32)

        sampled_frames: list[np.ndarray] = []
        for idx in indices:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, int(idx))
            ok, frame = self.cap.read()
            if ok and frame is not None:
                sampled_frames.append(frame)

        if not sampled_frames:
            raise RuntimeError("Не вдалося зчитати кадри для оцінки фону")

        background = np.median(np.stack(sampled_frames, axis=0), axis=0).astype(np.uint8)
        self.background_gray = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)

    def setup_writer(self) -> None:
        if self.cap is None:
            raise RuntimeError("Відео не відкрито")

        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        if fps <= 0:
            fps = 25.0

        Path(self.output_path).parent.mkdir(parents=True, exist_ok=True)
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.writer = cv2.VideoWriter(self.output_path, fourcc, fps, (width, height))
        if not self.writer.isOpened():
            raise RuntimeError(f"Не вдалося створити вихідний файл: {self.output_path}")

    def process(self) -> None:
        if self.cap is None or self.writer is None or self.background_gray is None:
            raise RuntimeError("Система не ініціалізована")

        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        kernel = np.ones((3, 3), dtype=np.uint8)

        while True:
            ok, frame = self.cap.read()
            if not ok:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            diff = cv2.absdiff(gray, self.background_gray)
            _, mask = cv2.threshold(diff, self.threshold, 255, cv2.THRESH_BINARY)

            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
            mask = cv2.dilate(mask, kernel, iterations=2)

            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            result = frame.copy()
            count = 0
            for contour in contours:
                if cv2.contourArea(contour) < self.min_area:
                    continue
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(result, (x, y), (x + w, y + h), (0, 255, 0), 2)
                count += 1

            cv2.putText(
                result,
                f"Objects: {count}",
                (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 255, 255),
                2,
                cv2.LINE_AA,
            )

            self.writer.write(result)
            cv2.imshow("Foreground mask", mask)
            cv2.imshow("Detection (OOP)", result)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    def close(self) -> None:
        if self.writer is not None:
            self.writer.release()
        if self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()

    def execute(self) -> None:
        self.open()
        try:
            self.estimate_background()
            self.setup_writer()
            self.process()
        finally:
            self.close()



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "ООП: виявлення об'єктів у відео із використанням простої "
            "фонової оцінки"
        )
    )
    parser.add_argument("--input", default="lab13/input.mp4", help="Шлях до вхідного відео")
    parser.add_argument(
        "--output",
        default="lab13/output_detected_oop.mp4",
        help="Шлях до вихідного відео з детекцією",
    )
    parser.add_argument(
        "--samples",
        type=int,
        default=25,
        help="Кількість кадрів для медіанної оцінки фону",
    )
    parser.add_argument("--threshold", type=int, default=30, help="Поріг для foreground-маски")
    parser.add_argument("--min-area", type=float, default=500.0, help="Мінімальна площа об'єкта")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    app = BackgroundMotionDetector(
        input_path=args.input,
        output_path=args.output,
        samples=args.samples,
        threshold=args.threshold,
        min_area=args.min_area,
    )
    app.execute()


if __name__ == "__main__":
    main()
