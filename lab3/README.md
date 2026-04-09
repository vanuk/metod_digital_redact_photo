# Лабораторна робота 3

## Тема
Зміна розміру зображення за допомогою OpenCV.

## Мета
Ознайомитися зі зміною розміру зображення: за заданими width/height та за коефіцієнтами масштабування з різними методами інтерполяції (Python і C++), включно з ООП-підходом.

## Підготовка
### Python
Встановлення залежності:

```bash
pip install opencv-python
```

### C++
Потрібна встановлена OpenCV для C++ та налаштований компілятор.

## Завдання 1
Зміна розміру за width/height (процедурно).

Python:
```bash
python lab3/task1_python.py --input lab3/image.jpg --output lab3/resized_wh.jpg --width 800 --height 600
```

C++:
```bash
g++ lab3/task1_cpp.cpp -o lab3/task1_cpp `pkg-config --cflags --libs opencv4`
./lab3/task1_cpp lab3/image.jpg lab3/resized_wh_cpp.jpg 800 600
```

## Завдання 2
Зміна розміру за масштабом та інтерполяцією (процедурно).

Python:
```bash
python lab3/task2_python.py --input lab3/image.jpg --output lab3/resized_scale.jpg --fx 0.5 --fy 0.5 --interpolation cubic
```

C++:
```bash
g++ lab3/task2_cpp.cpp -o lab3/task2_cpp `pkg-config --cflags --libs opencv4`
./lab3/task2_cpp lab3/image.jpg lab3/resized_scale_cpp.jpg 0.5 0.5 cubic
```

Підтримувані методи інтерполяції: nearest, linear, cubic, area, lanczos4.

## Завдання 3
ООП: зміна розміру за width/height.

Python:
```bash
python lab3/task3_python_oop.py --input lab3/image.jpg --output lab3/resized_wh_oop.jpg --width 1024 --height 768
```

C++:
```bash
g++ lab3/task3_cpp_oop.cpp -o lab3/task3_cpp_oop `pkg-config --cflags --libs opencv4`
./lab3/task3_cpp_oop lab3/image.jpg lab3/resized_wh_cpp_oop.jpg 1024 768
```

## Завдання 4
ООП: зміна розміру за масштабом та інтерполяцією.

Python:
```bash
python lab3/task4_python_oop.py --input lab3/image.jpg --output lab3/resized_scale_oop.jpg --fx 1.5 --fy 1.5 --interpolation area
```

C++:
```bash
g++ lab3/task4_cpp_oop.cpp -o lab3/task4_cpp_oop `pkg-config --cflags --libs opencv4`
./lab3/task4_cpp_oop lab3/image.jpg lab3/resized_scale_cpp_oop.jpg 1.5 1.5 area
```
