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



HOLIDAY_NAMES_EN = {
    (1, 1): "New Year's Day",
    (1, 6): "Epiphany",
    (5, 1): "May Day",
    (12, 6): "Independence Day",
    (12, 25): "Christmas Day",
    (12, 26): "St. Stephen's Day",
}

HOLIDAY_NAMES_FI = {
    (1, 1): "Uudenvuodenpäivä",
    (1, 6): "Loppiainen",
    (5, 1): "Vappu",
    (12, 6): "Itsenäisyyspäivä",
    (12, 25): "Joulupäivä",
    (12, 26): "Tapaninpäivä",
}

def get_finnish_holidays(year, lang='en'):
    holidays = []
    if lang == 'fi':
        names = HOLIDAY_NAMES_FI
        movable = {
            'Good Friday': 'Pitkäperjantai',
            'Easter Monday': '2. pääsiäispäivä',
            'Ascension Day': 'Helatorstai',
            'Midsummer Eve': 'Juhannusaatto',
            'Midsummer Day': 'Juhannuspäivä',
            "All Saints' Day": 'Pyhäinpäivä',
        }
    else:
        names = HOLIDAY_NAMES_EN
        movable = {
            'Good Friday': 'Good Friday',
            'Easter Monday': 'Easter Monday',
            'Ascension Day': 'Ascension Day',
            'Midsummer Eve': 'Midsummer Eve',
            'Midsummer Day': 'Midsummer Day',
            "All Saints' Day": "All Saints' Day",
        }
    # Fixed holidays
    for m, d in FIXED_HOLIDAYS:
        holidays.append((date(year, m, d), names.get((m, d), "Holiday")))
    # Movable holidays
    easter = get_easter(year)
    holidays.append((easter - timedelta(days=2), movable['Good Friday']))
    holidays.append((easter + timedelta(days=1), movable['Easter Monday']))
    holidays.append((easter + timedelta(days=39), movable['Ascension Day']))
    midsummer_eve = get_midsummer_eve(year)
    if midsummer_eve:
        holidays.append((midsummer_eve, movable['Midsummer Eve']))
    midsummer_day = get_midsummer_day(year)
    if midsummer_day:
        holidays.append((midsummer_day, movable['Midsummer Day']))
    all_saints = get_all_saints_day(year)
    if all_saints:
        holidays.append((all_saints, movable["All Saints' Day"]))
    return holidays

def count_working_day_holidays(year, lang='en'):
    holidays = get_finnish_holidays(year, lang=lang)
    working_day_holidays = [(d, name) for d, name in holidays if d.weekday() < 5]
    working_day_holidays.sort()
    return len(working_day_holidays), working_day_holidays

def main():
    while True:
        year_input = input("Enter the year for which to calculate Finnish midweek holidays: ")
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