import unittest

from base import Diapason
from exceptions import PointNotNumberException, PointNotInDiapasonException, SplitByNotOverlapsDiapason


class DiapasonTestCase(unittest.TestCase):

    def test_diapason_str(self):
        diapason = Diapason([2, 3])
        self.assertEqual(
            str(diapason),
            'Diapason([2.0, 3.0])'
        )
        diapason = Diapason([1, 2, 3, 4, 5, 6, 7, 8])
        self.assertEqual(
            str(diapason),
            "Diapason([1.0, 2.0, 3.0, 4.0, 5.0...])"
        )

    def test_validate_points(self):
        with self.assertRaises(PointNotNumberException):
            Diapason([2, 3, 'i am string'])

    def test_is_point(self):
        diapason = Diapason([0, 1.77])
        self.assertFalse(
            diapason.is_point
        )
        diapason = Diapason([1, 1.0000000])
        self.assertTrue(
            diapason.is_point
        )

    def test_touch_diapasons(self):
        diapason_1 = Diapason([0, 1.77])
        diapason_2 = Diapason([0, -1])
        self.assertTrue(diapason_1.touch(diapason_2))

    def test_equal_diapasons(self):
        diapason_1 = Diapason([0, 1.77])
        diapason_3 = Diapason([0, 1.77, 1])
        diapason_2 = Diapason([0, -1])
        self.assertFalse(diapason_3 == diapason_2)
        self.assertTrue(diapason_1 == diapason_3)

    def test_in_diapason(self):
        diapason_1 = Diapason([0, 1.77])
        diapason_2 = Diapason([0, 1.77, 1])
        diapason_3 = Diapason([-2, 5])
        self.assertTrue(diapason_1 in diapason_2)
        self.assertFalse(diapason_3 in diapason_1)
        self.assertTrue(diapason_1 in diapason_3)

    def test_diapason_length(self):
        diapason_1 = Diapason([0, 1.77])
        diapason_2 = Diapason([-2, 2])
        self.assertEqual(
            diapason_1.length,
            1.77
        )
        self.assertEqual(
            diapason_2.length,
            4
        )

    def test_diapason_plus(self):
        diapason_1 = Diapason([0, 5])
        diapason_2 = Diapason([-2, 2])
        diapason = diapason_1 + diapason_2
        self.assertEqual(
            diapason.start_point,
            -2
        )
        self.assertEqual(
            diapason.end_point,
            5
        )
        self.assertEqual(
            len(diapason.points),
            4
        )

    def test_diapason_crosses(self):
        diapason_1 = Diapason([0, 5])
        diapason_2 = Diapason([5, 88])
        diapason_3 = Diapason([4, 88])
        self.assertTrue(diapason_1.crosses(diapason_2))
        self.assertFalse(diapason_1.crosses(diapason_3))
        self.assertFalse(diapason_3.crosses(diapason_2))

    def test_diapason_intersects(self):
        d_1 = Diapason([1, 3])
        d_2 = Diapason([2, 4])
        d_3 = Diapason([3, 4])
        self.assertTrue(d_1.intersects(d_2))
        self.assertFalse(d_3.intersects(d_1))

    def test_diapason_distance(self):
        d_1 = Diapason([1, 3])
        d_2 = Diapason([2, 4])
        d_3 = Diapason([5, 6])
        self.assertEqual(
            d_2.distance(d_1),
            0
        )
        self.assertEqual(
            d_3.distance(d_1),
            2
        )

    def test_move(self):
        d_1 = Diapason([1, 3])
        d_1.move(5)
        self.assertEqual(
            d_1.length,
            2
        )
        self.assertEqual(
            d_1.start_point,
            6
        )
        self.assertEqual(
            d_1.end_point,
            8
        )
        d_1.move(-1)
        self.assertEqual(
            d_1.points,
            [5, 7]
        )

    def test_split_by_point(self):
        d_1 = Diapason([1, 3])
        left_d, right_d = d_1.split_by_point(2)
        self.assertEqual(
            left_d.length,
            1
        )
        self.assertEqual(
            left_d.start_point,
            1
        )
        self.assertEqual(
            left_d.end_point,
            2
        )
        self.assertEqual(
            right_d.start_point,
            2
        )
        self.assertEqual(
            right_d.end_point,
            3
        )
        with self.assertRaises(PointNotInDiapasonException):
            d_1.split_by_point(8)

    def test_overlaps(self):
        d_1 = Diapason([1, 5])
        d_2 = Diapason([2, 4])
        d_3 = Diapason([5, 6])
        self.assertTrue(
            d_1.overlaps(d_2)
        )
        self.assertFalse(
            d_1.overlaps(d_3)
        )

    def test_split_by_diapason(self):
        d_1 = Diapason([1, 5])
        d_2 = Diapason([2, 3])
        d_3 = Diapason([5, 6])
        left_d, right_d = d_1.split_by_diapason(d_2)
        self.assertEqual(
            left_d.start_point,
            1
        )
        self.assertEqual(
            left_d.end_point,
            2
        )
        self.assertEqual(
            right_d.start_point,
            3
        )
        self.assertEqual(
            right_d.end_point,
            5
        )
        with self.assertRaises(SplitByNotOverlapsDiapason):
            d_1.split_by_diapason(d_3)

    def test_common(self):
        d_1 = Diapason([1, 5])
        d_2 = Diapason([2, 3])
        d_3 = Diapason([5, 6])
        common = d_1.common(d_2)
        self.assertEqual(
            common.start_point,
            2
        )
        self.assertEqual(
            common.end_point,
            3
        )
        self.assertIsNone(d_1.common(d_3))

    def test_add_point(self):
        d_1 = Diapason([1, 5])
        d_1.add_point(6)
        self.assertEqual(
            d_1.end_point,
            6
        )
        self.assertEqual(
            d_1.length,
            5
        )
        with self.assertRaises(PointNotNumberException):
            d_1.add_point('I am string')

    def test_add_points(self):
        d_1 = Diapason([1, 5])
        d_1.add_points([6, 8])
        self.assertEqual(
            d_1.end_point,
            8
        )
        self.assertEqual(
            d_1.length,
            7
        )
        with self.assertRaises(PointNotNumberException):
            d_1.add_points([5, 6, 'I am string'])

    def test_different(self):
        d_1 = Diapason([1, 5])
        d_2 = Diapason([6, 8])
        d_3 = Diapason([3, 7])
        diff = d_1.different(d_2)
        self.assertEqual(
            diff[0],
            d_1
        )
        self.assertEqual(
            diff[1],
            d_2
        )
        diff = d_3.different(d_2)
        self.assertEqual(
            diff[0],
            Diapason([3, 6])
        )
        self.assertEqual(
            diff[1],
            Diapason([7, 8])
        )
        self.assertIsNone(
            Diapason([1, 2]).different(Diapason([1, 2]))
        )
