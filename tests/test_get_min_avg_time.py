import unittest
from application.apis.utils import get_min_avg_time


class TestMinAvgTime(unittest.TestCase):

    def test_get_min_avg_time(self):
        data = {12: [[1616154160, 1616154460]], 22: [[1616154160, 1616154360], [1616155160, 1616155260]]}
        self.assertEqual(get_min_avg_time(data), 300)


if __name__ == '__main__':
    unittest.main()
