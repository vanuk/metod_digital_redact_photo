import argparse
import cv2


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Читання, відображення та збереження відеопотоку з вебкамери"
    )
    parser.add_argument(
        "--camera-index",
        type=int,
        default=0,
        help="Індекс вебкамери (за замовчуванням: 0)",
    )
    parser.add_argument(
        "--output",
        default="lab2/webcam_output.avi",
        help="Шлях до вихідного відеофайлу (за замовчуванням: lab2/webcam_output.avi)",
    )
    parser.add_argument(
        "--fps",
        type=float,
        default=20.0,
        help="FPS для збереження відео (за замовчуванням: 20.0)",
    )
    parser.add_argument(
        "--window",
        default="Webcam",
        help="Назва вікна для відображення",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    cap = cv2.VideoCapture(args.camera_index)
    if not cap.isOpened():
        raise RuntimeError(
            f"Не вдалося відкрити вебкамеру з індексом {args.camera_index}"
        )

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if width <= 0 or height <= 0:
        width, height = 640, 480

    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    writer = cv2.VideoWriter(args.output, fourcc, args.fps, (width, height))
    if not writer.isOpened():
        cap.release()
        raise RuntimeError(f"Не вдалося створити файл для запису: {args.output}")

    cv2.namedWindow(args.window, cv2.WINDOW_NORMAL)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        writer.write(frame)
        cv2.imshow(args.window, frame)

        # Натисніть q для завершення зйомки.
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    writer.release()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
