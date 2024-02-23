from PIL import Image
import os

def convert_to_ascii(image_path, columns):
    image = Image.open(image_path)
    width, height = image.size
    aspect_ratio = height / width / 2
    new_width = columns
    new_height = int(aspect_ratio * new_width * 0.55)
    resized_image = image.resize((new_width, new_height))
    grayscale_image = resized_image.convert("L")

    ascii_chars = "⠁⠃⠉⠙⠑⠋⠛⠓⠊⠚⠅⠇⠍⠝⠕⠏⠟"
    ascii_image = ""
    for i, pixel_value in enumerate(grayscale_image.getdata()):
        ascii_image += ascii_chars[pixel_value // 16]
        if (i + 1) % columns == 0:
            ascii_image += "\n"

    return ascii_image

def resize_image(image_path, new_width, new_height):
    image = Image.open(image_path)

    resized_image = image.resize((new_width, new_height))

    return resized_image


from PIL import Image
import os


def convert_image_format(input_path, output_format):
    try:
        with Image.open(input_path) as img:
            if img.mode == 'RGBA':
                img = img.convert('RGB')

            if output_format.lower() == 'jpg':
                output_format = 'jpeg'

            output_path = os.path.splitext(input_path)[0] + '.' + output_format.lower()

            img.save(output_path, format=output_format)

            print(f"Image successfully converted to {output_format} format and saved at {output_path}")
            return output_path
    except Exception as e:
        print(f"Error converting image: {e}")