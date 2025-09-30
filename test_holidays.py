import unittest
from holidays_finland_user_year import count_working_day_holidays

class TestFinnishHolidays(unittest.TestCase):
    def test_2024_english(self):
        count, holidays = count_working_day_holidays(2024, lang='en')
        self.assertIsInstance(count, int)
        self.assertGreater(count, 0)
        self.assertTrue(any(name == "Good Friday" for _, name in holidays))

    def test_2024_finnish(self):
        count, holidays = count_working_day_holidays(2024, lang='fi')
        self.assertIsInstance(count, int)
        self.assertGreater(count, 0)
        self.assertTrue(any(name == "Pitkäperjantai" for _, name in holidays))

    def test_invalid_year(self):
        with self.assertRaises(Exception):
            count_working_day_holidays(1800, lang='en')

if __name__ == '__main__':
    unittest.main()
