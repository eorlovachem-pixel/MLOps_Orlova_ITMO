import unittest

from validation import validate_binary


class ValidationTests(unittest.TestCase):
    def test_valid(self) -> None:
        validate_binary([0, 1, 1])

    def test_invalid(self) -> None:
        with self.assertRaises(ValueError):
            validate_binary([0, 3])


if __name__ == "__main__":
    unittest.main()
