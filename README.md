# Multi-Country Holidays Calculator# testi



This repository contains a multi-country public holidays calculator that determines which public holidays fall on working days (Monday–Friday) for any year between 1900 and 2100.This repository contains a Python script `holidays_finland_user_year.py` for calculating Finnish public holidays that fall on working days (Monday–Friday) for any user-specified year between 1900 and 2100.



## Supported Countries## Script Overview



- **Finland** (fi) - Finnish public holidays- **Fixed Holidays:**  

- **Sweden** (se) - Swedish public holidays  The script includes Finnish public holidays that always fall on the same date, such as New Year's Day, Epiphany, May Day, Independence Day, Christmas, and St. Stephen's Day.

- **Norway** (no) - Norwegian public holidays

- **Estonia** (ee) - Estonian public holidays- **Movable Holidays:**  

  The script calculates holidays that change each year, including:

## Features  - Easter (and related holidays: Good Friday, Easter Monday, Ascension Day)

  - Midsummer Eve and Midsummer Day (based on specific weekdays in June)

### Web Application  - All Saints’ Day (based on a specific Saturday in late October or early November)

- Modern web interface built with Flask

- Multi-language support: English, Finnish, Swedish, Norwegian, Estonian- **Usage:**  

- Country selection dropdown  Run the script and enter a year when prompted. The script will display:

- Year input (1900-2100)  - The number of Finnish public holidays that fall on a weekday (Monday–Friday) for the specified year.

- Beautiful gradient UI with responsive design  - A list of those holidays with their respective dates and day names.

- Holiday display in styled tables

## Example

### Command-Line Interface

- Run `holidays_finland_user_year.py` directly```

- Interactive prompts for year, country, and language selectionEnter the year for which to calculate Finnish working day holidays: 2025

- Output displays all working day holidays with dates and namesIn 2025, there are X public holidays in Finland that fall on a working day (Mon-Fri):

- Monday, 2025-01-06

### API Testing- Friday, 2025-04-18

- Comprehensive Robot Framework acceptance tests- ...

- Browser-based UI tests using Browser library (Playwright)```

- HTTP API tests using RequestsLibrary

- Tests organized with Gherkin syntax (Given/When/Then)## Purpose

- Proper tagging for test categorization (smoke, regression, country-specific)

This script is useful for anyone who needs to know which Finnish holidays impact working days in a given year, such as payroll, HR, or personal planning.

## Architecture

---

### Object-Oriented Design
- **HolidayCalculator**: Abstract base class defining the interface for all country calculators
- **Country-Specific Calculators**: FinnishHolidayCalculator, SwedishHolidayCalculator, NorwegianHolidayCalculator, EstonianHolidayCalculator
- **Factory Pattern**: `get_holiday_calculator()` function returns appropriate calculator based on country code

### Holiday Types
- **Fixed Holidays**: Holidays that always fall on the same date (e.g., New Year's Day, National Days)
- **Movable Holidays**: Holidays calculated based on Easter or specific weekday rules (e.g., Good Friday, Midsummer Eve, All Saints' Day)

## Running the Application

### Using Docker (Recommended)

```bash
docker-compose up --build
```

Access the web application at: `http://localhost:5000`

### Locally with Python

```bash
# Install dependencies
pip install flask

# Run the web application
python app.py

# Or run the command-line script
python holidays_finland_user_year.py
```

## Running Tests

### All Tests (Browser + API)

```bash
docker-compose up --build
```

Test results will be generated in the `acceptance_tests/` directory:
- `output.xml` - Raw test output
- `log.html` - Detailed test log
- `report.html` - Test summary report

### Specific Test Suites

```bash
# Run only smoke tests
robot --include smoke acceptance_tests/

# Run only Finland-specific tests  
robot --include finland acceptance_tests/

# Run only API tests
robot --include api acceptance_tests/api_tests.robot
```

## Example Usage

### Web Interface
1. Open http://localhost:5000
2. Select a year (1900-2100)
3. Choose a country (Finland, Sweden, Norway, Estonia)
4. Select your preferred language
5. Click "Show Holidays"

### Command-Line
```bash
$ python holidays_finland_user_year.py
Multi-Country Holiday Calculator
=================================
Supported countries: Finland (fi), Sweden (se), Norway (no), Estonia (ee)

Enter a year (1900-2100): 2025
Enter country code (fi/se/no/ee) [default: fi]: se
Enter language (en/fi/sv/no/et) [default: en]: en

In 2025, there are 10 public holidays that fall on a working day (Mon-Fri):
  Wednesday, 2025-01-01 - New Year's Day
  Monday, 2025-01-06 - Epiphany
  Friday, 2025-04-18 - Good Friday
  ...
```

## File Structure

```
.
├── app.py                          # Flask web application
├── holidays_finland_user_year.py   # Main entry point & factory functions
├── holiday_calculator.py           # Abstract base class
├── holidays_finland.py             # Finnish holiday calculator
├── holidays_sweden.py              # Swedish holiday calculator
├── holidays_norway.py              # Norwegian holiday calculator
├── holidays_estonia.py             # Estonian holiday calculator
├── test_holidays.py                # Unit tests
├── Dockerfile                      # Docker configuration for Flask app
├── docker-compose.yml              # Multi-container orchestration
├── acceptance_tests/
│   ├── holidays_acceptance.robot   # Browser-based UI tests
│   ├── api_tests.robot             # HTTP API tests
│   └── Dockerfile                  # Robot Framework test container
├── TESTING_GUIDELINES.md           # Testing documentation
└── .github/
    └── copilot-instructions.md     # Development guidelines
```

## Purpose

This application is useful for:
- Payroll and HR departments planning working days across multiple countries
- International teams coordinating schedules
- Personal planning for multi-country operations
- Educational purposes to understand holiday calculation algorithms

## Documentation

- **TESTING_GUIDELINES.md** - Comprehensive testing documentation
- **.github/copilot-instructions.md** - Development guidelines and AI assistant instructions

---
