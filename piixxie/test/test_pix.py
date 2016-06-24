from unittest import TestCase

from PIL import Image

from piixxie import pix, errors


class PixTests(TestCase):

    def test_dimension_verification_valid(self):
        """
        Input image has dimensions X by Y, with a given pixel size k, such that
        X = x * k, and Y = y * k
        """
        pixel_size = 5
        input_im = Image.new('RGB', (20, 25))
        pix.verify(input_im, pixel_size)

    def test_dimension_verification_invalid_x(self):
        """
        Input image DOES NOT have dimension X, with a given pixel size k, such that
        X = x * k.
        """
        pixel_size = 5
        input_im = Image.new('RGB', (20, 28))
        with self.assertRaises(errors.DimensionError):
            pix.verify(input_im, pixel_size)

    def test_dimension_verification_invalid_y(self):
        """
        Input image DOES NOT have dimension Y, with a given pixel size k, such that
        Y = y * k.
        """
        pixel_size = 5
        input_im = Image.new('RGB', (31, 30))
        with self.assertRaises(errors.DimensionError):
            pix.verify(input_im, pixel_size)


    def test_dimension_verification_invalid_xy(self):
        """
        Input image DOES NOT have dimensions X by Y, with a given pixel size k, such that
        X = x * k, and Y = y * k
        """
        pixel_size = 5
        input_im = Image.new('RGB', (24, 88))
        with self.assertRaises(errors.DimensionError):
            pix.verify(input_im, pixel_size)

    def test_prepare_scaling(self):
        """
        Ensure image preparation scaled the output image properly.
        """
        input_im = Image.new('RGB', (24, 88))
        output_im = pix.prepare(input_im, 2)

        output_x, output_y = output_im.size
        self.assertEqual(output_x, 48)
        self.assertEqual(output_y, 176)
