"""
Base Holiday Calculator Module

This module provides the base structure for calculating holidays across different countries.
Each country-specific implementation should inherit from the base HolidayCalculator class.
"""

from datetime import date, timedelta
from abc import ABC, abstractmethod


class HolidayCalculator(ABC):
    """
    Abstract base class for country-specific holiday calculators.
    
    Each country implementation should override the get_fixed_holidays and
    get_movable_holidays methods to provide country-specific holiday data.
    """
    
    def __init__(self, year, lang='en'):
        """
        Initialize the holiday calculator.
        
        Args:
            year (int): The year for which to calculate holidays
            lang (str): Language code for holiday names ('en', 'fi', 'sv', etc.)
        """
        self.year = year
        self.lang = lang
    
    @abstractmethod
    def get_fixed_holidays(self):
        """
        Get fixed holidays (same date every year).
        
        Returns:
            list: List of tuples (date, holiday_name)
        """
        pass
    
    @abstractmethod
    def get_movable_holidays(self):
        """
        Get movable holidays (dates that change each year).
        
        Returns:
            list: List of tuples (date, holiday_name)
        """
        pass
    
    def get_all_holidays(self):
        """
        Get all holidays for the year.
        
        Returns:
            list: List of tuples (date, holiday_name)
        """
        holidays = []
        holidays.extend(self.get_fixed_holidays())
        holidays.extend(self.get_movable_holidays())
        return holidays
    
    def get_working_day_holidays(self):
        """
        Get holidays that fall on working days (Monday-Friday).
        
        Returns:
            tuple: (count, list of tuples (date, holiday_name))
        """
        all_holidays = self.get_all_holidays()
        working_day_holidays = [(d, name) for d, name in all_holidays if d.weekday() < 5]
        working_day_holidays.sort()
        return len(working_day_holidays), working_day_holidays
    
    @staticmethod
    def get_easter(year):
        """
        Calculate Easter Sunday using the Meeus/Jones/Butcher algorithm.
        
        Args:
            year (int): Year for which to calculate Easter
            
        Returns:
            date: Date of Easter Sunday
        """
        a = year % 19
        b = year // 100
        c = year % 100
        d = b // 4
        e = b % 4
        f = (b + 8) // 25
        g = (b - f + 1) // 3
        h = (19 * a + b - d - g + 15) % 30
        i = c // 4
        k = c % 4
        l = (32 + 2 * e + 2 * i - h - k) % 7
        m = (a + 11 * h + 22 * l) // 451
        month = (h + l - 7 * m + 114) // 31
        day = ((h + l - 7 * m + 114) % 31) + 1
        return date(year, month, day)
