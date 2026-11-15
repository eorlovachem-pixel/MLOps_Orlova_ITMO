"""Standard-library tests: no dependency manager required for HW2."""

import unittest

from metrics import accuracy, binary_precision


class MetricsTests(unittest.TestCase):
    def test_correct_predictions(self) -> None:
        self.assertEqual(accuracy([0, 1, 0], [0, 1, 0]), 1.0)

    def test_empty_inputs(self) -> None:
        with self.assertRaises(ValueError):
            accuracy([], [])

    def test_unequal_lengths(self) -> None:
        with self.assertRaises(ValueError):
            accuracy([0, 1], [0])

    def test_empty_precision(self) -> None:
        with self.assertRaises(ValueError):
            binary_precision([], [])


if __name__ == "__main__":
    unittest.main()
