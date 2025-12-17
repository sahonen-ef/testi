# Project Structure Guide

This document shows recommended directory structures for integrating the RobotFramework MCP Server into your project.

## Option 1: MCP Server in Project Root

Place the MCP server directly in your project alongside your tests:

```
your-project/
├── RobotFramework-MCP-server/     # This MCP server template
│   ├── .env                        # Your configuration (create from .env.example)
│   ├── .env.example                # Configuration template
│   ├── Dockerfile
│   ├── server.py
│   ├── setup_container.sh
│   ├── start-container.sh
│   ├── SETUP.md
│   ├── README.md
│   └── PROJECT_STRUCTURE.md        # This file
│
├── tests/                          # Your Robot Framework tests
│   ├── __init__.robot              # Suite setup (optional)
│   ├── api/
│   │   ├── test_api_endpoints.robot
│   │   └── test_authentication.robot
│   ├── ui/
│   │   ├── test_login.robot
│   │   ├── test_dashboard.robot
│   │   └── test_forms.robot
│   └── resources/                  # Shared resources
│       ├── keywords.robot
│       └── variables.robot
│
├── results/                        # Test execution results (auto-created)
│   ├── output.xml
│   ├── log.html
│   └── report.html
│
├── src/                            # Your application code
│   └── ...
│
└── README.md                       # Your project README
```

**Configuration in .env:**
```bash
TESTS_DIR=./tests
RESULTS_DIR=./results
```

## Option 2: MCP Server in Subdirectory

Keep the MCP server in a dedicated automation/testing directory:

```
your-project/
├── src/                            # Your application
│   └── ...
│
├── automation/                     # Test automation directory
│   ├── RobotFramework-MCP-server/ # MCP server
│   │   ├── .env
│   │   ├── .env.example
│   │   ├── Dockerfile
│   │   ├── server.py
│   │   ├── setup_container.sh
│   │   ├── start-container.sh
│   │   └── ...
│   │
│   ├── tests/                      # Robot tests
│   │   ├── smoke/
│   │   │   └── test_smoke.robot
│   │   ├── regression/
│   │   │   └── test_regression.robot
│   │   └── resources/
│   │       └── common.robot
│   │
│   └── results/                    # Test results
│       └── ...
│
└── README.md
```

**Configuration in .env:**
```bash
TESTS_DIR=../tests
RESULTS_DIR=../results
```

## Option 3: Monorepo Structure

For larger projects with multiple components:

```
monorepo/
├── services/
│   ├── api/
│   │   └── ...
│   ├── frontend/
│   │   └── ...
│   └── backend/
│       └── ...
│
├── testing/
│   ├── RobotFramework-MCP-server/ # MCP server
│   │   ├── .env
│   │   ├── .env.example
│   │   └── ...
│   │
│   ├── e2e-tests/                  # End-to-end tests
│   │   ├── api/
│   │   ├── ui/
│   │   └── integration/
│   │
│   ├── unit-tests/                 # Unit tests (separate)
│   │   └── ...
│   │
│   └── results/                    # All test results
│       ├── e2e/
│       ├── unit/
│       └── integration/
│
└── docs/
    └── ...
```

**Configuration in .env:**
```bash
TESTS_DIR=../e2e-tests
RESULTS_DIR=../results/e2e
```

## Option 4: Tests Outside Project

Keep tests in a separate repository or directory:

```
/home/user/
├── my-application/                 # Your app
│   ├── src/
│   └── ...
│
└── my-application-tests/           # Test repository
    ├── RobotFramework-MCP-server/
    │   ├── .env
    │   └── ...
    │
    ├── robot-tests/
    │   ├── smoke/
    │   ├── regression/
    │   └── performance/
    │
    └── results/
        └── ...
```

**Configuration in .env (use absolute paths):**
```bash
TESTS_DIR=/home/user/my-application-tests/robot-tests
RESULTS_DIR=/home/user/my-application-tests/results

# Or on Windows:
# TESTS_DIR=C:\Users\myuser\my-application-tests\robot-tests
# RESULTS_DIR=C:\Users\myuser\my-application-tests\results
```

## Recommended Test Organization

Regardless of where you place the MCP server, organize your Robot tests like this:

```
tests/
├── __init__.robot                  # Suite-level setup/teardown
├── api/                            # API tests
│   ├── __init__.robot              # API suite setup
│   ├── test_users.robot
│   ├── test_products.robot
│   └── test_orders.robot
│
├── ui/                             # UI tests
│   ├── __init__.robot              # UI suite setup
│   ├── test_login.robot
│   ├── test_dashboard.robot
│   └── test_checkout.robot
│
├── integration/                    # Integration tests
│   └── test_full_workflow.robot
│
├── resources/                      # Shared resources
│   ├── keywords/                   # Keyword libraries
│   │   ├── api_keywords.robot
│   │   └── ui_keywords.robot
│   ├── variables/                  # Variables
│   │   ├── common.robot
│   │   └── test_data.robot
│   └── libraries/                  # Custom Python libraries
│       └── custom_lib.py
│
└── data/                           # Test data files
    ├── users.csv
    └── products.json
```

## Example Test File Structure

### tests/api/test_users.robot
```robotframework
*** Settings ***
Documentation     API tests for user management
Resource          ../resources/keywords/api_keywords.robot
Resource          ../resources/variables/common.robot
Library           RequestsLibrary

*** Variables ***
${BASE_URL}       http://localhost:8000
${API_PATH}       /api/v1/users

*** Test Cases ***
Get All Users
    [Tags]    api    smoke
    Create Session    api    ${BASE_URL}
    ${response}=    GET On Session    api    ${API_PATH}
    Should Be Equal As Numbers    ${response.status_code}    200

Create New User
    [Tags]    api    crud
    ${user_data}=    Create Dictionary    name=John Doe    email=john@example.com
    ${response}=    POST    ${BASE_URL}${API_PATH}    json=${user_data}
    Should Be Equal As Numbers    ${response.status_code}    201
```

### tests/ui/test_login.robot
```robotframework
*** Settings ***
Documentation     UI tests for login functionality
Resource          ../resources/keywords/ui_keywords.robot
Library           Browser

Suite Setup       Open Browser To Login Page
Suite Teardown    Close Browser

*** Variables ***
${LOGIN_URL}      http://localhost:8000/login
${VALID_USER}     testuser@example.com
${VALID_PASS}     Password123

*** Test Cases ***
Successful Login
    [Tags]    ui    smoke
    Enter Username    ${VALID_USER}
    Enter Password    ${VALID_PASS}
    Click Login Button
    User Should Be Logged In

Failed Login With Invalid Password
    [Tags]    ui    negative
    Enter Username    ${VALID_USER}
    Enter Password    wrong_password
    Click Login Button
    Error Message Should Be Visible
```

## Results Directory Structure

The results directory will be auto-populated:

```
results/
├── output.xml                      # Robot Framework XML output
├── log.html                        # Detailed execution log
├── report.html                     # Summary report
├── selenium-screenshot-*.png       # Screenshots (if any)
└── browser/                        # Browser library artifacts
    ├── traces/
    └── videos/
```

## .gitignore Recommendations

Add to your `.gitignore`:

```gitignore
# Robot Framework Results
results/
*.xml
*.html
*-screenshot-*.png

# MCP Server Configuration
RobotFramework-MCP-server/.env

# Docker
.docker/

# Python
__pycache__/
*.py[cod]
*.so
.Python
venv/
```

## Environment-Specific Configurations

### Development
```bash
# .env (development)
TESTS_DIR=./tests
RESULTS_DIR=./results
NETWORK_MODE=host
BASE_URL=http://localhost:8000
HEADLESS=false
```

### CI/CD
```bash
# .env.ci (for continuous integration)
TESTS_DIR=/ci/tests
RESULTS_DIR=/ci/results
NETWORK_MODE=bridge
BASE_URL=http://test-server:8000
HEADLESS=true
BROWSER=chromium
```

### Production Testing
```bash
# .env.prod (for production smoke tests)
TESTS_DIR=/prod/tests/smoke
RESULTS_DIR=/prod/results
NETWORK_MODE=bridge
BASE_URL=https://production.example.com
HEADLESS=true
```

## Tips

1. **Use relative paths** when possible - makes the setup portable
2. **Use absolute paths** when tests are in a different repository
3. **Keep tests organized** by type (api, ui, integration)
4. **Version control** your `.env.example` but not `.env`
5. **Create multiple .env files** for different environments
6. **Use tags consistently** for easier filtering (`smoke`, `regression`, `api`, `ui`)
7. **Share resources** in the `resources/` directory
8. **Keep test data** in a separate `data/` directory

## Next Steps

1. Choose a structure that fits your project
2. Create the necessary directories
3. Copy `.env.example` to `.env`
4. Update paths in `.env`
5. Follow [SETUP.md](SETUP.md) for detailed configuration
