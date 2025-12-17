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

    def test_leap_year_2000(self):
        count, holidays = count_working_day_holidays(2000, lang='en')
        self.assertIsInstance(count, int)
        self.assertGreater(count, 0)
        self.assertTrue(any(name == "Good Friday" for _, name in holidays))

    def test_boundary_year_1900(self):
        count, holidays = count_working_day_holidays(1900, lang='en')
        self.assertIsInstance(count, int)
        self.assertGreater(count, 0)

    def test_boundary_year_2100(self):
        count, holidays = count_working_day_holidays(2100, lang='en')
        self.assertIsInstance(count, int)
        self.assertGreater(count, 0)

    def test_swedish_language(self):
        count, holidays = count_working_day_holidays(2025, lang='sv')
        self.assertIsInstance(count, int)
        self.assertGreater(count, 0)
        self.assertTrue(any(name == "Långfredagen" for _, name in holidays))

    def test_norwegian_language(self):
        count, holidays = count_working_day_holidays(2025, lang='no')
        self.assertIsInstance(count, int)
        self.assertGreater(count, 0)
        self.assertTrue(any(name == "Langfredag" for _, name in holidays))

    def test_estonian_language(self):
        count, holidays = count_working_day_holidays(2025, lang='et')
        self.assertIsInstance(count, int)
        self.assertGreater(count, 0)
        self.assertTrue(any(name == "Suur Reede" for _, name in holidays))

if __name__ == '__main__':
    unittest.main()
