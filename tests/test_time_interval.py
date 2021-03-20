import unittest
from application.model.time_interval import convert_time_str_to_int, convert_time_int_to_str


class TestConvertTime(unittest.TestCase):

    def test_str_to_int(self):  # "09:00-18:00" -> [540, 1080]
        self.assertEqual(convert_time_str_to_int(["09:00", "18:00"]), [540, 1080])

    def test_int_to_str(self):  # [540, 1080] -> "09:00-18:00"
        self.assertEqual(convert_time_int_to_str([540, 1080]), "09:00-18:00")


if __name__ == '__main__':
    unittest.main()
