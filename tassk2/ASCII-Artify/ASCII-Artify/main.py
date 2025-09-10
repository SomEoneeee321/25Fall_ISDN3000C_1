import sys
import argparse  # Import the argparse module
from PIL import Image

# Default character ramp (used if --chars is not provided)
DEFAULT_ASCII_CHARS = " .'`^\",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

def resize_and_grayscale(image, new_width=100):
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio)
    resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return resized.convert('L')

def map_pixel_to_char(pixel_value, char_ramp):
    clamped = max(0, min(255, pixel_value))
    interval = 255 / (len(char_ramp) - 1) if len(char_ramp) > 1 else 0
    return char_ramp[int(clamped / interval)] if char_ramp else DEFAULT_ASCII_CHARS[0]

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Convert an image to ASCII art.")
    # Required positional argument: image path
    parser.add_argument("image_path", help="Path to the input image file")
    # Optional argument: custom character ramp (--chars)
    parser.add_argument(
        "--chars", 
        help=f"Custom character ramp (default: '{DEFAULT_ASCII_CHARS}')",
        default=DEFAULT_ASCII_CHARS  # Use default if not provided
    )

    # Parse the arguments
    args = parser.parse_args()

    try:
        with Image.open(args.image_path) as image:
            # 1. Resize and convert to grayscale
            processed_img = resize_and_grayscale(image)
            # 2. Get pixel data
            pixels = list(processed_img.getdata())
            # 3. Build ASCII string
            ascii_str = ""
            width = processed_img.width
            for i, pixel in enumerate(pixels):
                if i % width == 0 and i != 0:
                    ascii_str += "\n"
                ascii_str += map_pixel_to_char(pixel, args.chars)
            # 4. Print result
            print(ascii_str)
    except FileNotFoundError:
        print(f"Error: File not found at '{args.image_path}'")
    except Image.UnidentifiedImageError:
        print(f"Error: '{args.image_path}' is not a valid image file")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()