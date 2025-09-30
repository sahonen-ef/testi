"""
Estonian Holiday Calculator

Calculates Estonian public holidays for a given year.
"""

from datetime import date, timedelta
from holiday_calculator import HolidayCalculator


class EstonianHolidayCalculator(HolidayCalculator):
    """Calculator for Estonian public holidays."""
    
    # Fixed holidays (month, day)
    FIXED_HOLIDAYS = [
        (1, 1),   # New Year's Day
        (2, 24),  # Independence Day
        (5, 1),   # Spring Day
        (6, 23),  # Victory Day
        (6, 24),  # St. John's Day / Midsummer Day
        (8, 20),  # Restoration of Independence Day
        (12, 24), # Christmas Eve
        (12, 25), # Christmas Day
        (12, 26), # Boxing Day
    ]
    
    # Holiday names in different languages
    HOLIDAY_NAMES = {
        'en': {
            (1, 1): "New Year's Day",
            (2, 24): "Independence Day",
            (5, 1): "Spring Day",
            (6, 23): "Victory Day",
            (6, 24): "St. John's Day",
            (8, 20): "Restoration of Independence Day",
            (12, 24): "Christmas Eve",
            (12, 25): "Christmas Day",
            (12, 26): "Boxing Day",
            'Good Friday': "Good Friday",
            'Easter Sunday': "Easter Sunday",
            'Whit Sunday': "Whit Sunday",
        },
        'et': {
            (1, 1): "Uusaasta",
            (2, 24): "Iseseisvuspäev",
            (5, 1): "Kevadpüha",
            (6, 23): "Võidupüha",
            (6, 24): "Jaanipäev",
            (8, 20): "Taasiseseisvumispäev",
            (12, 24): "Jõululaupäev",
            (12, 25): "Esimene jõulupüha",
            (12, 26): "Teine jõulupüha",
            'Good Friday': "Suur reede",
            'Easter Sunday': "Ülestõusmispühade 1. püha",
            'Whit Sunday': "Nelipühade 1. püha",
        }
    }
    
    def get_fixed_holidays(self):
        """
        Get Estonian fixed holidays.
        
        Returns:
            list: List of tuples (date, holiday_name)
        """
        holidays = []
        names = self.HOLIDAY_NAMES.get(self.lang, self.HOLIDAY_NAMES['en'])
        
        for month, day in self.FIXED_HOLIDAYS:
            holiday_date = date(self.year, month, day)
            holiday_name = names.get((month, day), "Holiday")
            holidays.append((holiday_date, holiday_name))
        
        return holidays
    
    def get_movable_holidays(self):
        """
        Get Estonian movable holidays.
        
        Returns:
            list: List of tuples (date, holiday_name)
        """
        holidays = []
        names = self.HOLIDAY_NAMES.get(self.lang, self.HOLIDAY_NAMES['en'])
        
        # Easter-based holidays
        easter = self.get_easter(self.year)
        holidays.append((easter - timedelta(days=2), names['Good Friday']))
        holidays.append((easter, names['Easter Sunday']))
        holidays.append((easter + timedelta(days=49), names['Whit Sunday']))
        
        return holidays
