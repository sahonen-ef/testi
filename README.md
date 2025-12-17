# Finnish Holidays Application

> **Note**: This project calculates and displays Finnish midweek holidays for a given year, supporting multiple languages and robust error handling.

## Features

- **Holiday Calculation**: Displays public holidays that fall on weekdays (Monday-Friday).
- **Multi-language Support**: English and Finnish.
- **Boundary Testing**: Supports years between 1900 and 2100.
- **Error Handling**: Validates input and provides meaningful error messages.
- **Acceptance Tests**: Comprehensive Robot Framework test suite.

## Project Structure

```plaintext
.
├── app.py                        # Flask application
├── holidays_finland_user_year.py # Core logic for holiday calculation
├── acceptance_tests/             # Robot Framework acceptance tests
│   ├── holidays_acceptance.robot
│   ├── api_tests.robot
│   └── Dockerfile                # Docker setup for running tests
├── test_holidays.py              # Unit tests
├── Dockerfile                    # Docker setup for the application
├── docker-compose.yml            # Docker Compose configuration
└── README.md                     # Project documentation
```

## Getting Started

### Prerequisites

- Python 3.10+
- Docker (optional, for containerized setup)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/sahonen-ef/testi.git
   cd testi
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. Start the Flask application:

   ```bash
   python app.py
   ```

2. Open your browser and navigate to:

   ```
   http://127.0.0.1:5000
   ```

### Running Tests

#### Unit Tests

Run the unit tests using:

```bash
python -m unittest test_holidays.py
```

#### Acceptance Tests

Run the Robot Framework tests using Docker:

```bash
cd acceptance_tests
docker build -t rf-tests .
docker run --rm rf-tests
```

Or run directly:

```bash
robot acceptance_tests/holidays_acceptance.robot
```

## Docker Setup

### Build and Run the Application

1. Build the Docker image:

   ```bash
   docker build -t finnish-holidays .
   ```

2. Run the container:

   ```bash
   docker run -p 5000:5000 finnish-holidays
   ```

### Using Docker Compose

1. Start the services:

   ```bash
   docker-compose up
   ```

2. The application will be available at:

   ```
   http://127.0.0.1:5000
   ```

## Acknowledgments

- [Robot Framework](https://robotframework.org/)
- [Flask](https://flask.palletsprojects.com/)
- [Docker](https://www.docker.com/)