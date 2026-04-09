import cv2


def main() -> None:
    image = cv2.imread("lab1/1.jpg", cv2.IMREAD_GRAYSCALE)

    if image is None:
        raise FileNotFoundError("Не вдалося відкрити файл 1.jpg у поточній папці")

    is_saved = cv2.imwrite("lab1/image_grayscale.jpeg", image)
    if not is_saved:
        raise IOError("Не вдалося зберегти файл image_grayscale.jpeg")

    cv2.namedWindow("Grayscale image", cv2.WINDOW_AUTOSIZE)
    cv2.imshow("Grayscale image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
