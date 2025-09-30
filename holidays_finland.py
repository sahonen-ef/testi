"""
Finnish Holiday Calculator

Calculates Finnish public holidays for a given year.
"""

from datetime import date, timedelta
from holiday_calculator import HolidayCalculator


class FinnishHolidayCalculator(HolidayCalculator):
    """Calculator for Finnish public holidays."""
    
    # Fixed holidays (month, day)
    FIXED_HOLIDAYS = [
        (1, 1),   # New Year's Day
        (1, 6),   # Epiphany
        (5, 1),   # May Day
        (12, 6),  # Independence Day
        (12, 25), # Christmas Day
        (12, 26), # St. Stephen's Day
    ]
    
    # Holiday names in different languages
    HOLIDAY_NAMES = {
        'en': {
            (1, 1): "New Year's Day",
            (1, 6): "Epiphany",
            (5, 1): "May Day",
            (12, 6): "Independence Day",
            (12, 25): "Christmas Day",
            (12, 26): "St. Stephen's Day",
            'Good Friday': "Good Friday",
            'Easter Monday': "Easter Monday",
            'Ascension Day': "Ascension Day",
            'Midsummer Eve': "Midsummer Eve",
            'Midsummer Day': "Midsummer Day",
            "All Saints' Day": "All Saints' Day",
        },
        'fi': {
            (1, 1): "Uudenvuodenpäivä",
            (1, 6): "Loppiainen",
            (5, 1): "Vappu",
            (12, 6): "Itsenäisyyspäivä",
            (12, 25): "Joulupäivä",
            (12, 26): "Tapaninpäivä",
            'Good Friday': "Pitkäperjantai",
            'Easter Monday': "2. pääsiäispäivä",
            'Ascension Day': "Helatorstai",
            'Midsummer Eve': "Juhannusaatto",
            'Midsummer Day': "Juhannuspäivä",
            "All Saints' Day": "Pyhäinpäivä",
        }
    }
    
    def get_fixed_holidays(self):
        """
        Get Finnish fixed holidays.
        
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
        Get Finnish movable holidays.
        
        Returns:
            list: List of tuples (date, holiday_name)
        """
        holidays = []
        names = self.HOLIDAY_NAMES.get(self.lang, self.HOLIDAY_NAMES['en'])
        
        # Easter-based holidays
        easter = self.get_easter(self.year)
        holidays.append((easter - timedelta(days=2), names['Good Friday']))
        holidays.append((easter + timedelta(days=1), names['Easter Monday']))
        holidays.append((easter + timedelta(days=39), names['Ascension Day']))
        
        # Midsummer (Friday and Saturday between June 19-25)
        midsummer_eve = self._get_midsummer_eve()
        if midsummer_eve:
            holidays.append((midsummer_eve, names['Midsummer Eve']))
        
        midsummer_day = self._get_midsummer_day()
        if midsummer_day:
            holidays.append((midsummer_day, names['Midsummer Day']))
        
        # All Saints' Day (Saturday between October 31 - November 6)
        all_saints = self._get_all_saints_day()
        if all_saints:
            holidays.append((all_saints, names["All Saints' Day"]))
        
        return holidays
    
    def _get_midsummer_eve(self):
        """Get Midsummer Eve (Friday between June 19-25)."""
        for day in range(19, 26):
            d = date(self.year, 6, day)
            if d.weekday() == 4:  # Friday
                return d
        return None
    
    def _get_midsummer_day(self):
        """Get Midsummer Day (Saturday between June 20-26)."""
        for day in range(20, 27):
            d = date(self.year, 6, day)
            if d.weekday() == 5:  # Saturday
                return d
        return None
    
    def _get_all_saints_day(self):
        """Get All Saints' Day (Saturday between October 31 - November 6)."""
        for month, day in [(10, 31)] + [(11, d) for d in range(1, 7)]:
            d = date(self.year, month, day)
            if d.weekday() == 5:  # Saturday
                return d
        return None
