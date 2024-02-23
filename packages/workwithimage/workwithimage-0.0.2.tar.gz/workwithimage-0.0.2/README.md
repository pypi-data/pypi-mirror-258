### Work With Image

#### English

This Python library, `workwithimage`, enables converting images into ASCII art with uniform character width. It utilizes the Pillow library for image processing.

#### Installation

```bash
pip install workwithimage
```

#### Usage

```python
from workwithimage import convert_to_ascii

# Example usage
image_path = "your_image.jpg"
columns = 150
ascii_image = convert_to_ascii(image_path, columns)
print(ascii_image)

# Save to file
with open("output.txt", "w") as file:
    file.write(ascii_image)
```

#### Supported Image Formats

- JPEG
- PNG
- GIF
- BMP
- TIFF
- WebP
- ICO
- and more

#### Important Notes

- The library supports various image formats; check Pillow documentation for the complete list.
- Adjust the `columns` parameter for desired output width.

---

#### Russian

Эта библиотека на Python, `workwithimage`, позволяет преобразовывать изображения в ASCII-арт с символами одинаковой длины, используя библиотеку Pillow для обработки изображений.

#### Установка

```bash
pip install workwithimage
```

#### Использование

```python
from workwithimage import convert_to_ascii

# Пример использования
image_path = "ваше_изображение.jpg"
columns = 150
ascii_image = convert_to_ascii(image_path, columns)
print(ascii_image)

# Сохранение в файл
with open("output.txt", "w") as file:
    file.write(ascii_image)
```

#### Поддерживаемые форматы изображений

- JPEG
- PNG
- GIF
- BMP
- TIFF
- WebP
- ICO
- и другие

#### Важные замечания

- Библиотека поддерживает различные форматы изображений; проверьте документацию Pillow для полного списка.
- Измените параметр `columns` для получения нужной ширины вывода.