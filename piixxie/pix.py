import argparse
import sys

from PIL import Image, ImageDraw

from piixxie.errors import PiixxieError, DimensionError


DEFAULT_SOURCE_PIXEL = 1
DEFAULT_SCALE = 1


def drawpixel(target: ImageDraw, x, y, size, color):
    target.rectangle((x * size, y * size, (x + 1) * size, (y + 1) * size), fill=color)


def process(input: Image, output: Image, pixel: int, scale: int):
    """
    Do the needful.
    """
    size = pixel * scale
    x = y = 0
    source_x, source_y = input.size

    draw = ImageDraw.Draw(output)

    while True:
        # color = input.getpixel((x * pixel, y * pixel)
        art_pixel = input.crop((x * pixel, y * pixel, (x + 1) * pixel, (y + 1) * pixel))
        colors = list(art_pixel.getdata())
        total_pixels = len(colors)

        r = g = b = a = 0
        for color in colors:
            r += color[0]
            g += color[1]
            b += color[2]
            a += color[3]

        r //= total_pixels
        g //= total_pixels
        b //= total_pixels
        a //= total_pixels

        drawpixel(draw, x, y, size, (r, g, b, a))

        x += 1

        if x * pixel >= source_x:
            x = 0
            y += 1

            if y * pixel >= source_y:
                break


def verify(source: Image, pixel: int):
    """
    Ensure that the given settings make sense with the input file.

    SPECIFICALLY, the dimensions of the source image must be multiples of `pixel`.
    """
    size_x, size_y = source.size

    for dimension in (size_x, size_y):
        if dimension % pixel != 0:
            raise DimensionError("Source image dimensions must be a multiple of pixel size.")

    return source


def verify_path(source_path: str, pixel:int):
    """
    Wrapper around verify that takes a path to a file.
    """
    input_im = Image.open(source_path)

    return verify(input_im, pixel)


def prepare(source: Image, scale: int):
    """
    Move from paths to images to actual image objects.
    """
    source_x, source_y = source.size
    output_im = Image.new(source.mode, (source_x * scale, source_y * scale))

    return output_im


def main(args=None):
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-p', '--pixel', dest='pixel', action='store', type=int, default=DEFAULT_SOURCE_PIXEL,
                            help="Side length of artistic pixel in source image.")
    arg_parser.add_argument('-s', '--scale', dest='scale', action='store', type=int, default=DEFAULT_SCALE,
                            help="Scaling to apply to source image.")
    arg_parser.add_argument('-i', '--input', dest='input', action='store', required=True,
                            help="Source image.")
    arg_parser.add_argument('-o', '--output', dest='output', action='store', required=True,
                            help="Output image.")
    settings = arg_parser.parse_args(args)

    try:
        input_im = verify_path(settings.input, settings.pixel)
        output_im = prepare(input_im, settings.scale)
        process(input_im, output_im, settings.pixel, settings.scale)
        output_im.save(settings.output)

    except PiixxieError as err:
        sys.exit("fatal: {}".format(err))


if __name__ == '__main__':
    main()
