
# GitHub Copilot Instructions

This project uses GitHub Copilot to assist with code completion and suggestions. Follow these guidelines to ensure Copilot works effectively in this workspace:

## 1. Code Style
- Use clear and descriptive function and variable names.
- Add docstrings to all public functions.
- Keep functions small and focused on a single task.

## 2. File Structure
- Main logic: `holidays_finland_user_year.py`
- Unit tests: `test_holidays.py`
- Acceptance tests: `acceptance_tests/holidays_acceptance.robot`

## 3. Copilot Prompts & Test Guidelines
- When asking Copilot for help, specify the function or file you are working on.
- For test generation, specify if you want unit or acceptance tests.
- For Docker or deployment help, mention the relevant file (`Dockerfile`, `docker-compose.yml`).
- For Robot Framework acceptance tests:
	- Always add suitable tags (such as smoke, regression, language, or feature area) to each test case for easier categorization and filtering. Example:
		[Tags]    smoke    english
	- Write test cases using Gherkin syntax (Given, When, Then, And, But) for clarity and BDD-style readability. Each test case should describe user behavior and expected outcomes in a scenario format.
  - In Keywords section, use User as a subject.

## 4. Best Practices
- Review Copilot suggestions for correctness and security.
- Do not commit sensitive information or credentials.
- Use Copilot to generate code, comments, and documentation, but always verify the output.

## Robot Framework Acceptance Tests

- Always add suitable tags (such as smoke, regression, language, or feature area) to each test case for easier categorization and filtering. Example:
    [Tags]    smoke    english
- Write test cases using Gherkin syntax (Given, When, Then, And, But) for clarity and BDD-style readability. Each test case should describe user behavior and expected outcomes in a scenario format.
