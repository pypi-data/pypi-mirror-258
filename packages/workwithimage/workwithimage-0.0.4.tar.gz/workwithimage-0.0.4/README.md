### Work With Image

#### English

This Python library, `workwithimage`, allows you to work with images. Features available in this version:
- Converting an image into ASKII art
- Image resolution adjustment
- Changing the image format

#### Installation

```bash
pip install workwithimage
```

#### Converting an image to ASKII art

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

#### Image resolution adjustment

```python
from workwithimage import resize_image

# Example usage
image_path = "your_image.jpg"
new_width = 800
new_height = 600
resized_image = resize_image(image_path, new_width, new_height)
```

#### Changing the image format

```python
from workwithimage import convert_image_format

# Example usage
input_image_path = "your_image.jpg"
desired_output_format = "png"

output_image_path = convert_image_format(input_image_path, desired_output_format)
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

#### Important Note

- The library supports various image formats; check Pillow documentation for the complete list.
---

#### Russian

Библиотека на Python, `workwithimage`, позволяет работать с изображениями. Функции доступные в данной версии:
- Перобразование изображения в ASKII-арт
- Изменение разрешения изображения
- Изменение разрешения изображения


#### Установка

```bash
pip install workwithimage
```

#### Перобразование изображения в ASKII-арт

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

#### Изменение разрешения изображения

```python
from workwithimage import resize_image

# Пример использования
image_path = "ваше_изображение.jpg"
new_width = 800
new_height = 600
resized_image = resize_image(image_path, new_width, new_height)
```

#### Изменение формата изображения

```python
from workwithimage import convert_image_format

# Пример использования
input_image_path = "ваше_изображение.jpg"
desired_output_format = "png"

output_image_path = convert_image_format(input_image_path, desired_output_format)
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

#### Важное замечания

- Библиотека поддерживает различные форматы изображений; проверьте документацию Pillow для полного списка.
