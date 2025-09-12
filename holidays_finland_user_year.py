import datetime
from datetime import date, timedelta

FIXED_HOLIDAYS = [
    (1, 1),    # New Year's Day
    (1, 6),    # Epiphany
    (5, 1),    # May Day
    (12, 6),   # Independence Day
    (12, 25),  # Christmas Day
    (12, 26),  # St. Stephen's Day
]

def get_easter(year):
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

def get_midsummer_eve(year):
    for day in range(19, 26):
        d = date(year, 6, day)
        if d.weekday() == 4:
            return d
    return None

def get_midsummer_day(year):
    for day in range(20, 27):
        d = date(year, 6, day)
        if d.weekday() == 5:
            return d
    return None

def get_all_saints_day(year):
    for day in range(31, 38):
        try:
            d = date(year, 10, day)
        except ValueError:
            d = date(year, 11, day - 31)
        if d.weekday() == 5:
            return d
    return None

def get_finnish_holidays(year):
    holidays = set()
    for m, d in FIXED_HOLIDAYS:
        holidays.add(date(year, m, d))
    easter = get_easter(year)
    holidays.add(easter - timedelta(days=2))   # Good Friday
    holidays.add(easter + timedelta(days=1))   # Easter Monday
    holidays.add(easter + timedelta(days=39))  # Ascension Day
    midsummer_eve = get_midsummer_eve(year)
    midsummer_day = get_midsummer_day(year)
    if midsummer_eve: holidays.add(midsummer_eve)
    if midsummer_day: holidays.add(midsummer_day)
    all_saints = get_all_saints_day(year)
    if all_saints: holidays.add(all_saints)
    return holidays

def count_working_day_holidays(year):
    holidays = get_finnish_holidays(year)
    working_day_holidays = [d for d in holidays if d.weekday() < 5]
    return len(working_day_holidays), sorted(working_day_holidays)

def main():
    while True:
        year_input = input("Enter the year for which to calculate Finnish working day holidays: ")
        try:
            year = int(year_input)
            if year < 1900 or year > 2100:
                print("Please enter a valid year between 1900 and 2100.")
                continue
            break
        except ValueError:
            print("Please enter a valid integer year.")
    count, days = count_working_day_holidays(year)
    print(f"In {year}, there are {count} public holidays in Finland that fall on a working day (Mon-Fri):")
    for d in days:
        print(f"- {d.strftime('%A, %Y-%m-%d')}")

if __name__ == "__main__":
    main()