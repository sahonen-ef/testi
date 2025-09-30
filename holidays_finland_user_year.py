"""
Multi-Country Holidays Calculator

This module provides functions to calculate public holidays for different countries
that fall on working days (Monday-Friday) for a given year.

Supported countries: Finland, Sweden, Norway, Estonia
"""

from holidays_finland import FinnishHolidayCalculator
from holidays_sweden import SwedishHolidayCalculator
from holidays_norway import NorwegianHolidayCalculator
from holidays_estonia import EstonianHolidayCalculator


# Map of country codes to calculator classes
COUNTRY_CALCULATORS = {
    'fi': FinnishHolidayCalculator,
    'finland': FinnishHolidayCalculator,
    'se': SwedishHolidayCalculator,
    'sweden': SwedishHolidayCalculator,
    'no': NorwegianHolidayCalculator,
    'norway': NorwegianHolidayCalculator,
    'ee': EstonianHolidayCalculator,
    'estonia': EstonianHolidayCalculator,
}


def get_holiday_calculator(country='fi'):
    """
    Get the appropriate holiday calculator for a country.
    
    Args:
        country (str): Country code or name (fi, finland, se, sweden, no, norway, ee, estonia)
        
    Returns:
        HolidayCalculator: The appropriate calculator class
        
    Raises:
        ValueError: If country is not supported
    """
    country_key = country.lower()
    if country_key not in COUNTRY_CALCULATORS:
        raise ValueError(f"Unsupported country: {country}. Supported: {list(COUNTRY_CALCULATORS.keys())}")
    return COUNTRY_CALCULATORS[country_key]


def count_working_day_holidays(year, lang='en', country='fi'):
    """
    Count and list public holidays that fall on working days for a given year and country.
    
    Args:
        year (int): The year to calculate holidays for
        lang (str): Language code for holiday names (en, fi, sv, no, et)
        country (str): Country code or name (fi, se, no, ee)
        
    Returns:
        tuple: (count, list of tuples (date, holiday_name))
        
    Raises:
        ValueError: If year is out of range or country is not supported
    """
    if year < 1900 or year > 2100:
        raise ValueError(f"Year must be between 1900 and 2100, got {year}")
    
    calculator_class = get_holiday_calculator(country)
    calculator = calculator_class(year, lang)
    return calculator.get_working_day_holidays()


if __name__ == "__main__":
    print("Multi-Country Holiday Calculator")
    print("=================================")
    print("Supported countries: Finland (fi), Sweden (se), Norway (no), Estonia (ee)")
    print()
    
    year_input = input("Enter a year (1900-2100): ")
    country_input = input("Enter country code (fi/se/no/ee) [default: fi]: ") or 'fi'
    lang_input = input("Enter language (en/fi/sv/no/et) [default: en]: ") or 'en'
    
    try:
        year = int(year_input)
        count, holidays = count_working_day_holidays(year, lang=lang_input, country=country_input)
        print(f"\nIn {year}, there are {count} public holidays that fall on a working day (Mon-Fri):")
        for holiday_date, holiday_name in holidays:
            print(f"  {holiday_date.strftime('%A, %Y-%m-%d')} - {holiday_name}")
    except ValueError as e:
        print(f"Error: {e}")
