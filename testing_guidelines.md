# Testing Guidelines

This project includes both unit and acceptance tests to ensure the correctness of Finnish holiday calculations.

## 1. Unit Testing

- **Test File:** [`test_holidays.py`](test_holidays.py)
- **How to Run:**
  ```sh
  python -m unittest test_holidays.py
  ```
- **Purpose:**  
  Unit tests should cover all functions in [`holidays_finland_user_year.py`](holidays_finland_user_year.py), especially:
  - `get_easter`
  - `get_midsummer_eve`
  - `get_midsummer_day`
  - `get_all_saints_day`
  - `get_finnish_holidays`
  - `count_working_day_holidays`

## 2. Acceptance Testing

- **Test Directory:** [`acceptance_tests/`](acceptance_tests/)
- **Test File:** [`holidays_acceptance.robot`](acceptance_tests/holidays_acceptance.robot)
- **How to Run (with Docker Compose):**
  ```sh
  docker-compose up --build
  ```
- **Purpose:**  
  Acceptance tests use Robot Framework to verify the application's web interface (if present) and end-to-end functionality.

## 3. Common Issues

- Ensure the Flask app (if used) is running and accessible at the correct host and port before running acceptance tests.
- If using Docker Compose, verify that services are on the same network and use service names in test URLs.
- If you encounter `ERR_CONNECTION_REFUSED`, check that the app is listening on `0.0.0.0` and not just `127.0.0.1`.

## 4. Output Files

- Test results are saved as `output.xml`, `log.html`, and `report.html` in the project root.

---
