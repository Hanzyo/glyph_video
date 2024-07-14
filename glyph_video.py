import cv2
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

PIXEL_LIMIT = 500

char_array = np.array([' ',
                       '.',
                       '/',
                       '+',
                       '*',
                       '&',
                       '#',
                       '@'])

def img2glyph(img_path):
    input_path = "input/"+img_path
    input_img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    compression_ratio = int(max(input_img.shape[:2]) / PIXEL_LIMIT)
    resized_img = cv2.resize(input_img, (int(input_img.shape[1]/compression_ratio), int(input_img.shape[0]/compression_ratio)))

    mask_0 = (resized_img >= 0) & (resized_img < 256/8)
    mask_1 = (resized_img >= 256/8) & (resized_img < 2 * 256/8)
    mask_2 = (resized_img >= 2 * 256/8) & (resized_img < 3 * 256/8)
    mask_3 = (resized_img >= 3 * 256/8) & (resized_img < 4 * 256/8)
    mask_4 = (resized_img >= 4 * 256/8) & (resized_img < 5 * 256/8)
    mask_5 = (resized_img >= 5 * 256/8) & (resized_img < 6 * 256/8)
    mask_6 = (resized_img >= 6 * 256/8) & (resized_img < 7 * 256/8)
    mask_7 = (resized_img >= 7 * 256/8) & (resized_img < 8 * 256/8)
    mask_array = [mask_0, mask_1, mask_2, mask_3, mask_4, mask_5, mask_6, mask_7]

    output_arr = np.empty(resized_img.shape, dtype=str)
    for i, mask in enumerate(mask_array):
        output_arr[mask] = char_array[i]

    try:
        font = ImageFont.truetype("arial.ttf", 20)  # You can change the font and size
    except IOError:
        font = ImageFont.load_default()
        
    temp_image = Image.new('RGB', (1, 1))
    draw = ImageDraw.Draw(temp_image)

    # Calculate character dimensions
    char_bbox = draw.textbbox((0, 0), 'A', font=font)
    char_width = char_bbox[2] - char_bbox[0]
    char_height = char_bbox[3] - char_bbox[1]

    img_width = char_width * len(output_arr[0])
    img_height = char_height * len(output_arr)
    image = Image.new('RGB', (img_width, img_height), color='black')
    draw = ImageDraw.Draw(image)
    for y, row in enumerate(output_arr):
        for x, char in enumerate(row):
            draw.text((x * char_width, y * char_height), char, fill='white', font=font)
    image.save("output/"+img_path)

files = os.listdir("input")
jpeg_files = [file for file in files if file.lower().endswith(('.jpg', '.jpeg'))]
for img in jpeg_files:
    print(img)
    img2glyph(img)