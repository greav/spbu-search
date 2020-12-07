import unittest

from src.encoding import elias_gamma_encode, elias_delta_encode


class TestEncoding(unittest.TestCase):

    # Test for elias_gamma_encode()
    def test_elias_gamma_encode(self):
        self.assertEqual(elias_gamma_encode(15), "0001111")

    # Test for elias_delta_encode()
    def test_elias_delta_encode(self):
        self.assertEqual(elias_delta_encode(10), "00100010")


if __name__ == "__main__":
    unittest.main()
