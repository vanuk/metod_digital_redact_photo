# Звіт по темі 1

## Тема
Читання, відображення та збереження зображень за допомогою функцій бібліотеки OpenCV.

## Мета
Ознайомитися із читанням, відображенням та збереженням зображень за допомогою функцій бібліотеки OpenCV, оволодіти сучасними методами проєктування та розробки комп'ютерних програм для цих операцій мовами Python та C++, зокрема з використанням об'єктно-орієнтованого підходу.

## Хід роботи

### Завдання 1
Розробити комп'ютерні програми мовами Python та C++ для:
1. Читання зображення як одноканального у відтінках сірого з файлу `image.jpeg`.
2. Збереження результату у файлі `image_grayscale.jpeg`.
3. Відображення зображення у вікні `Grayscale image`.

#### Реалізація Python (процедурний підхід)
Файл: `task1_python.py`

```python
import cv2


def main() -> None:
	image = cv2.imread("image.jpeg", cv2.IMREAD_GRAYSCALE)

	if image is None:
		raise FileNotFoundError("Не вдалося відкрити файл image.jpeg у поточній папці")

	is_saved = cv2.imwrite("image_grayscale.jpeg", image)
	if not is_saved:
		raise IOError("Не вдалося зберегти файл image_grayscale.jpeg")

	cv2.namedWindow("Grayscale image", cv2.WINDOW_AUTOSIZE)
	cv2.imshow("Grayscale image", image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()


if __name__ == "__main__":
	main()
```

#### Реалізація C++ (процедурний підхід)
Файл: `task1_cpp.cpp`

```cpp
#include <opencv2/opencv.hpp>

#include <iostream>

int main() {
	const std::string input_path = "image.jpeg";
	const std::string output_path = "image_grayscale.jpeg";
	const std::string window_name = "Grayscale image";

	cv::Mat image = cv::imread(input_path, cv::IMREAD_GRAYSCALE);

	if (image.empty()) {
		std::cerr << "Не вдалося відкрити файл " << input_path << std::endl;
		return 1;
	}

	if (!cv::imwrite(output_path, image)) {
		std::cerr << "Не вдалося зберегти файл " << output_path << std::endl;
		return 1;
	}

	cv::namedWindow(window_name, cv::WINDOW_AUTOSIZE);
	cv::imshow(window_name, image);
	cv::waitKey(0);
	cv::destroyAllWindows();

	return 0;
}
```

### Завдання 2
Розробити програми мовами Python та C++ з використанням об'єктно-орієнтованого підходу для тих самих дій:
1. Читання `image.jpeg` як одноканального у відтінках сірого.
2. Збереження у `image_grayscale.jpeg`.
3. Відображення у вікні `Grayscale image`.

#### Реалізація Python (ООП)
Файл: `task2_python_oop.py`

```python
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
		input_path="image.jpeg",
		output_path="image_grayscale.jpeg",
		window_name="Grayscale image",
	)
	processor.execute()
```

#### Реалізація C++ (ООП)
Файл: `task2_cpp_oop.cpp`

```cpp
#include <opencv2/opencv.hpp>

#include <iostream>
#include <string>

class GrayscaleImageProcessor {
   public:
	GrayscaleImageProcessor(std::string input_path, std::string output_path, std::string window_name)
		: input_path_(std::move(input_path)),
		  output_path_(std::move(output_path)),
		  window_name_(std::move(window_name)) {}

	bool Execute() {
		if (!ReadGrayscale()) {
			return false;
		}

		if (!SaveImage()) {
			return false;
		}

		ShowImage();
		return true;
	}

   private:
	bool ReadGrayscale() {
		image_ = cv::imread(input_path_, cv::IMREAD_GRAYSCALE);
		if (image_.empty()) {
			std::cerr << "Не вдалося відкрити файл " << input_path_ << std::endl;
			return false;
		}
		return true;
	}

	bool SaveImage() const {
		if (image_.empty()) {
			std::cerr << "Зображення не завантажено" << std::endl;
			return false;
		}

		if (!cv::imwrite(output_path_, image_)) {
			std::cerr << "Не вдалося зберегти файл " << output_path_ << std::endl;
			return false;
		}

		return true;
	}

	void ShowImage() const {
		cv::namedWindow(window_name_, cv::WINDOW_AUTOSIZE);
		cv::imshow(window_name_, image_);
		cv::waitKey(0);
		cv::destroyAllWindows();
	}

	std::string input_path_;
	std::string output_path_;
	std::string window_name_;
	cv::Mat image_;
};

int main() {
	GrayscaleImageProcessor processor("image.jpeg", "image_grayscale.jpeg", "Grayscale image");

	if (!processor.Execute()) {
		return 1;
	}

	return 0;
}
```

## Приклад запуску

### Python
Встановлення OpenCV:

```bash
pip install opencv-python
```

Запуск:

```bash
python task1_python.py
python task2_python_oop.py
```

### C++
Скомпілювати програми з підключенням OpenCV (залежно від вашої конфігурації компілятора та встановлення OpenCV).

Приклад для g++:

```bash
g++ task1_cpp.cpp -o task1_cpp `pkg-config --cflags --libs opencv4`
g++ task2_cpp_oop.cpp -o task2_cpp_oop `pkg-config --cflags --libs opencv4`
```

## Висновок
У межах роботи реалізовано чотири програми, що виконують читання зображення у відтінках сірого, збереження обробленого результату та відображення у вікні OpenCV. Реалізації продемонстрували як процедурний, так і об'єктно-орієнтований підходи мовами Python і C++, що відповідає меті лабораторної роботи.