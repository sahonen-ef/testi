# testi

This repository contains a Python script `holidays_finland_user_year.py` for calculating Finnish public holidays that fall on working days (Monday–Friday) for any user-specified year between 1900 and 2100.

## Script Overview

- **Fixed Holidays:**  
  The script includes Finnish public holidays that always fall on the same date, such as New Year's Day, Epiphany, May Day, Independence Day, Christmas, and St. Stephen's Day.

- **Movable Holidays:**  
  The script calculates holidays that change each year, including:
  - Easter (and related holidays: Good Friday, Easter Monday, Ascension Day)
  - Midsummer Eve and Midsummer Day (based on specific weekdays in June)
  - All Saints’ Day (based on a specific Saturday in late October or early November)

- **Usage:**  
  Run the script and enter a year when prompted. The script will display:
  - The number of Finnish public holidays that fall on a weekday (Monday–Friday) for the specified year.
  - A list of those holidays with their respective dates and day names.

## Example

```
Enter the year for which to calculate Finnish working day holidays: 2025
In 2025, there are X public holidays in Finland that fall on a working day (Mon-Fri):
- Monday, 2025-01-06
- Friday, 2025-04-18
- ...
```

## Purpose

This script is useful for anyone who needs to know which Finnish holidays impact working days in a given year, such as payroll, HR, or personal planning.

---
