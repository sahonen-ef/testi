"""
Norwegian Holiday Calculator

Calculates Norwegian public holidays for a given year.
"""

from datetime import date, timedelta
from holiday_calculator import HolidayCalculator


class NorwegianHolidayCalculator(HolidayCalculator):
    """Calculator for Norwegian public holidays."""
    
    # Fixed holidays (month, day)
    FIXED_HOLIDAYS = [
        (1, 1),   # New Year's Day
        (5, 1),   # Labour Day
        (5, 17),  # Constitution Day
        (12, 25), # Christmas Day
        (12, 26), # Boxing Day
    ]
    
    # Holiday names in different languages
    HOLIDAY_NAMES = {
        'en': {
            (1, 1): "New Year's Day",
            (5, 1): "Labour Day",
            (5, 17): "Constitution Day",
            (12, 25): "Christmas Day",
            (12, 26): "Boxing Day",
            'Maundy Thursday': "Maundy Thursday",
            'Good Friday': "Good Friday",
            'Easter Sunday': "Easter Sunday",
            'Easter Monday': "Easter Monday",
            'Ascension Day': "Ascension Day",
            'Whit Sunday': "Whit Sunday",
            'Whit Monday': "Whit Monday",
        },
        'no': {
            (1, 1): "Første nyttårsdag",
            (5, 1): "Arbeidernes dag",
            (5, 17): "Grunnlovsdag",
            (12, 25): "Første juledag",
            (12, 26): "Andre juledag",
            'Maundy Thursday': "Skjærtorsdag",
            'Good Friday': "Langfredag",
            'Easter Sunday': "Første påskedag",
            'Easter Monday': "Andre påskedag",
            'Ascension Day': "Kristi himmelfartsdag",
            'Whit Sunday': "Første pinsedag",
            'Whit Monday': "Andre pinsedag",
        }
    }
    
    def get_fixed_holidays(self):
        """
        Get Norwegian fixed holidays.
        
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
        Get Norwegian movable holidays.
        
        Returns:
            list: List of tuples (date, holiday_name)
        """
        holidays = []
        names = self.HOLIDAY_NAMES.get(self.lang, self.HOLIDAY_NAMES['en'])
        
        # Easter-based holidays
        easter = self.get_easter(self.year)
        holidays.append((easter - timedelta(days=3), names['Maundy Thursday']))
        holidays.append((easter - timedelta(days=2), names['Good Friday']))
        holidays.append((easter, names['Easter Sunday']))
        holidays.append((easter + timedelta(days=1), names['Easter Monday']))
        holidays.append((easter + timedelta(days=39), names['Ascension Day']))
        holidays.append((easter + timedelta(days=49), names['Whit Sunday']))
        holidays.append((easter + timedelta(days=50), names['Whit Monday']))
        
        return holidays
