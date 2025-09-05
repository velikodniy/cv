#!/usr/bin/env python3
"""Favicon generator for web applications.

This script generates a complete favicon set from a source image,
including all standard sizes and formats for modern web browsers
and mobile devices.
"""

# /// script
# dependencies = [
#     "pillow",
# ]
# ///

import argparse
import sys
from pathlib import Path
from typing import List, Tuple

from PIL import Image, ImageEnhance, ImageFilter

# Standard favicon sizes and filenames
FAVICON_SPECS: List[Tuple[int, str]] = [
    (16, "favicon-16x16.png"),
    (32, "favicon-32x32.png"),
    (180, "apple-touch-icon.png"),
    (192, "android-chrome-192x192.png"),
    (512, "android-chrome-512x512.png"),
]

# ICO file sizes
ICO_SIZES: List[int] = [16, 32]


def load_and_prepare_image(image_path: Path) -> Image.Image:
    """Load and prepare the source image.

    Args:
        image_path: Path to source image file

    Returns:
        Prepared PIL Image object (square, RGB)

    Raises:
        FileNotFoundError: If image file doesn't exist
        ValueError: If image cannot be processed
    """
    try:
        img = Image.open(image_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Image file not found: {image_path}")
    except Exception as e:
        raise ValueError(f"Cannot open image {image_path}: {e}")

    # Convert to RGB if needed
    if img.mode != "RGB":
        img = img.convert("RGB")

    # Crop to square (center crop)
    width, height = img.size
    size = min(width, height)
    left = (width - size) // 2
    top = (height - size) // 2
    img = img.crop((left, top, left + size, top + size))

    return img


def enhance_image(img: Image.Image, enhance_contrast: bool = True) -> Image.Image:
    """Apply enhancements for better favicon visibility.

    Args:
        img: Source image
        enhance_contrast: Whether to enhance contrast and sharpness

    Returns:
        Enhanced image
    """
    if not enhance_contrast:
        return img

    # Slight contrast boost for better visibility at small sizes
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.2)

    # Slight sharpness boost
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(1.1)

    return img


def resize_with_sharpening(img: Image.Image, size: int) -> Image.Image:
    """Resize image with appropriate sharpening for small sizes.

    Args:
        img: Source image
        size: Target size in pixels

    Returns:
        Resized image
    """
    resized = img.resize((size, size), Image.Resampling.LANCZOS)

    # Apply unsharp masking for very small sizes to maintain clarity
    if size <= 32:
        resized = resized.filter(ImageFilter.UnsharpMask(radius=0.5, percent=50))

    return resized


def generate_png_favicons(img: Image.Image, output_dir: Path) -> None:
    """Generate PNG favicon files.

    Args:
        img: Prepared source image
        output_dir: Output directory
    """
    for size, filename in FAVICON_SPECS:
        resized = resize_with_sharpening(img, size)
        filepath = output_dir / filename
        resized.save(filepath, "PNG", optimize=True)


def generate_ico_favicon(img: Image.Image, output_dir: Path) -> None:
    """Generate ICO favicon file with multiple sizes.

    Args:
        img: Prepared source image
        output_dir: Output directory
    """
    ico_images = []
    for size in ICO_SIZES:
        resized = resize_with_sharpening(img, size)
        ico_images.append(resized)

    ico_path = output_dir / "favicon.ico"
    ico_images[0].save(
        ico_path,
        format="ICO",
        sizes=[(img.size[0], img.size[1]) for img in ico_images],
    )


def generate_favicon_set(
    input_image_path: Path, output_dir: Path, enhance_contrast: bool = True
) -> None:
    """Generate complete favicon set from source image.

    Args:
        input_image_path: Path to source image
        output_dir: Directory to save favicon files
        enhance_contrast: Whether to enhance contrast for better small-size visibility

    Raises:
        FileNotFoundError: If source image doesn't exist
        ValueError: If image processing fails
        OSError: If output directory cannot be created
    """
    # Ensure output directory exists
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        raise OSError(f"Cannot create output directory {output_dir}: {e}")

    # Load, prepare and enhance image
    img = load_and_prepare_image(input_image_path)
    img = enhance_image(img, enhance_contrast)

    # Generate favicon files
    generate_png_favicons(img, output_dir)
    generate_ico_favicon(img, output_dir)


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate favicon set from a source image",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s photo.jpg
  %(prog)s photo.jpg --output-dir build/
  %(prog)s photo.jpg --no-enhance --output-dir favicons/

Generated files:
  • favicon.ico (16x16, 32x32 combined)
  • favicon-16x16.png
  • favicon-32x32.png
  • apple-touch-icon.png (180x180)
  • android-chrome-192x192.png
  • android-chrome-512x512.png
        """.strip(),
    )

    parser.add_argument("input_image", type=Path, help="Path to source image file")
    parser.add_argument(
        "--output-dir",
        "-o",
        type=Path,
        default=Path("."),
        help="Output directory (default: current directory)",
    )
    parser.add_argument(
        "--no-enhance", action="store_true", help="Skip contrast/sharpness enhancement"
    )

    args = parser.parse_args()

    try:
        generate_favicon_set(args.input_image, args.output_dir, not args.no_enhance)
    except (FileNotFoundError, ValueError, OSError):
        sys.exit(1)
    except Exception:
        # Catch any unexpected errors and exit gracefully
        sys.exit(1)


if __name__ == "__main__":
    main()
