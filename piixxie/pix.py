import argparse
import sys

from PIL import Image

from .errors import PiixxieError, DimensionError


DEFAULT_SOURCE_PIXEL = 1
DEFAULT_SCALE = 1


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
    output_im = Image.new('RGB', (source_x * scale, source_y * scale))

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

    except PiixxieError as err:
        sys.exit("fatal: {}".format(err))


if __name__ == '__main__':
    main()
