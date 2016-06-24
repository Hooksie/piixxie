import argparse


DEFAULT_SOURCE_PIXEL = 1
DEFAULT_SCALE = 1


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


if __name__ == '__main__':
    main()
