from PIL import Image

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






