import argparse
import cv2


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Читання та відображення відеофайлу за допомогою OpenCV"
    )
    parser.add_argument(
        "--video",
        default="lab2/video.mp4",
        help="Шлях до вхідного відеофайлу (за замовчуванням: lab2/video.mp4)",
    )
    parser.add_argument(
        "--window",
        default="Video file",
        help="Назва вікна для відображення",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    cap = cv2.VideoCapture(args.video)
    if not cap.isOpened():
        raise FileNotFoundError(f"Не вдалося відкрити відеофайл: {args.video}")

    cv2.namedWindow(args.window, cv2.WINDOW_NORMAL)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow(args.window, frame)

        # Натисніть q для завершення перегляду.
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
