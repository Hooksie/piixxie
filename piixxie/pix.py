import argparse
import sys

from PIL import Image

from .errors import PiixxieError, DimensionError


DEFAULT_SOURCE_PIXEL = 1
DEFAULT_SCALE = 1


def verify(input: Image, pixel: int):
    """
    Ensure that the given settings make sense with the input file.

    SPECIFICALLY, the dimensions of the source image must be multiples of `pixel`.
    """
    size_x, size_y = input.size

    for dimension in (size_x, size_y):
        if dimension % pixel != 0:
            raise DimensionError("Source image dimensions must be a multiple of pixel size.")


def prepare(source: str, output: str, pixel: int, scale: int):
    """
    Move from paths to images to actual image objects.
    """
    input_im = Image.open(source)
    verify(input_im, pixel)


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
        prepare(settings.input, settings.output, settings.pixel, settings.scale)
    except PiixxieError as err:
        sys.exit("fatal: {}".format(err))


if __name__ == '__main__':
    main()
