import argparse
from pathlib import Path

import cv2


WINDOW_NAME = "Interactive Processing"


def _noop(_: int) -> None:
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Процедурна OpenCV-програма з GUI-взаємодією"
    )
    parser.add_argument("--input", default="lab11/image.jpg", help="Шлях до вхідного зображення")
    parser.add_argument(
        "--output",
        default="lab11/interactive_result.jpg",
        help="Куди зберегти результат (клавіша s)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    image = cv2.imread(args.input)
    if image is None:
        raise FileNotFoundError(f"Не вдалося відкрити файл: {args.input}")

    state: dict[str, object] = {
        "click": None,
        "pixel_text": "",
    }

    def on_mouse(event: int, x: int, y: int, _flags: int, _param: object) -> None:
        if event != cv2.EVENT_LBUTTONDOWN:
            return

        b, g, r = image[y, x]
        state["click"] = (x, y)
        state["pixel_text"] = f"x={x}, y={y}, BGR=({int(b)},{int(g)},{int(r)})"

    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(WINDOW_NAME, on_mouse)

    cv2.createTrackbar("Mode:0-Orig 1-Gray 2-Canny", WINDOW_NAME, 0, 2, _noop)
    cv2.createTrackbar("Blur", WINDOW_NAME, 2, 20, _noop)
    cv2.createTrackbar("Canny low", WINDOW_NAME, 80, 255, _noop)
    cv2.createTrackbar("Canny high", WINDOW_NAME, 160, 255, _noop)

    current = image.copy()

    while True:
        mode = cv2.getTrackbarPos("Mode:0-Orig 1-Gray 2-Canny", WINDOW_NAME)
        blur_raw = cv2.getTrackbarPos("Blur", WINDOW_NAME)
        blur_size = blur_raw * 2 + 1
        canny_low = cv2.getTrackbarPos("Canny low", WINDOW_NAME)
        canny_high = cv2.getTrackbarPos("Canny high", WINDOW_NAME)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (blur_size, blur_size), 0)

        if mode == 0:
            current = image.copy()
        elif mode == 1:
            current = cv2.cvtColor(blurred, cv2.COLOR_GRAY2BGR)
        else:
            edges = cv2.Canny(blurred, canny_low, max(canny_low + 1, canny_high))
            current = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        click = state["click"]
        text = state["pixel_text"]
        if click is not None:
            x, y = click
            cv2.circle(current, (x, y), 4, (0, 255, 255), -1)
            cv2.putText(
                current,
                str(text),
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 255),
                2,
                cv2.LINE_AA,
            )

        cv2.putText(
            current,
            "q: exit | s: save | click: pixel info",
            (10, current.shape[0] - 15),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            1,
            cv2.LINE_AA,
        )

        cv2.imshow(WINDOW_NAME, current)

        key = cv2.waitKey(30) & 0xFF
        if key == ord("q"):
            break
        if key == ord("s"):
            Path(args.output).parent.mkdir(parents=True, exist_ok=True)
            if not cv2.imwrite(args.output, current):
                raise IOError(f"Не вдалося зберегти файл: {args.output}")

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
