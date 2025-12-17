# RobotFramework MCP Server - Setup Instructions

## 🚀 Quick Start Guide

### Prerequisites
- Docker installed and running
- PowerShell (Windows) or Bash (Linux/macOS)

### Step 1: Environment Configuration

The `.env` file is already configured for this project with:
- **Tests Directory**: `./acceptance_tests` (mounted read-only at `/tests`)
- **Results Directory**: `./robot_results` (mounted read-write at `/results`)
- **Browser**: Chromium in headless mode
- **Base URL**: `http://app:5000` (Flask app)
- **Container Name**: `RobotFramework-mcp-persistent`

### Step 2: Build and Start Services

**PowerShell (Windows):**
```powershell
# Build all services (Flask app + MCP server)
docker-compose build

# Start all services in detached mode
docker-compose up -d

# Verify MCP server is running
docker ps --filter name=RobotFramework-mcp-persistent

# Check logs
docker logs RobotFramework-mcp-persistent
```

**Bash (Linux/macOS):**
```bash
# Build all services
docker-compose build

# Start all services in detached mode
docker-compose up -d

# Verify MCP server is running
docker ps --filter name=RobotFramework-mcp-persistent

# Check logs
docker logs RobotFramework-mcp-persistent
```

### Step 3: Configure AI Assistant

Add the MCP server to your AI assistant configuration:

#### GitHub Copilot (.vscode/agents/default.json)
Already configured at: `RobotFramework-MCP-server/.vscode/agents/default.json`

#### Amazon Q (amazonq/agents/default.json)
Already configured at: `RobotFramework-MCP-server/amazonq/agents/default.json`

#### GitLab Duo (.gitlab/agents/default.json)
Already configured at: `RobotFramework-MCP-server/.gitlab/agents/default.json`

**MCP Server Command:**
```bash
docker exec -i RobotFramework-mcp-persistent python /app/server.py
```

## 📋 Available MCP Tools

Once configured, AI assistants can use these tools:

### 1. list_tests
List all test cases in the test suite.
```
list_tests(suite_path="/tests")
```

### 2. run_suite
Execute entire test suite with optional filtering.
```
run_suite(
  suite_path="/tests",
  include_tags="smoke",
  exclude_tags="slow",
  variables={"BROWSER": "chromium", "HEADLESS": "true", "BASE_URL": "http://app:5000"}
)
```

**Note**: If UI tests fail with `ERR_SSL_PROTOCOL_ERROR`, use the container IP address as a workaround:
```
# Get the Flask app IP address
docker inspect flask_app --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'

# Run tests with IP-based URL
run_suite(
  suite_path="/tests/holidays_acceptance.robot",
  variables={"BASE_URL": "http://172.20.0.2:5000"}
)
```

### 3. run_test_by_name
Run specific test by name or pattern.
```
run_test_by_name(
  test_name="Verify Finnish Holidays",
  suite_path="/tests",
  variables={"BASE_URL": "http://app:5000"}
)
```

## 🧪 Manual Test Execution

You can also run tests manually without AI assistants:

**PowerShell:**
```powershell
# Run all tests
docker exec RobotFramework-mcp-persistent robot --outputdir /tmp/results /tests

# Run smoke tests only
docker exec RobotFramework-mcp-persistent robot --outputdir /tmp/results -i smoke /tests

# Run specific test
docker exec RobotFramework-mcp-persistent robot --outputdir /tmp/results -t "Verify Finnish Holidays" /tests

# Run with custom variables
docker exec RobotFramework-mcp-persistent robot --outputdir /tmp/results -v BASE_URL:http://app:5000 /tests
```

## 📁 Directory Structure

```
testi/
├── .env                              # Environment configuration
├── docker-compose.yml                # Docker services definition
├── acceptance_tests/                 # Robot Framework tests (→ /tests in container)
│   ├── holidays_acceptance.robot
│   └── api_tests.robot
├── robot_results/                    # Test results (→ /results in container)
├── RobotFramework-MCP-server/        # MCP server implementation
│   ├── Dockerfile                    # MCP server image
│   ├── server.py                     # FastMCP server code
│   ├── .vscode/agents/               # GitHub Copilot config
│   ├── .gitlab/agents/               # GitLab Duo config
│   └── amazonq/agents/               # Amazon Q config
├── app.py                            # Flask application
└── MCP_SERVER_SETUP.md              # This file
```

## 📊 Accessing Test Results

### Location 1: Inside Container
Results are stored at `/tmp/results/`:
- `output.xml` - Detailed execution data
- `log.html` - Execution log with details
- `report.html` - Summary report

### Location 2: Host Machine
Results are also available at `./robot_results/` (configured in `.env`)

### Copy Results from Container
```powershell
docker cp RobotFramework-mcp-persistent:/tmp/results/report.html ./
docker cp RobotFramework-mcp-persistent:/tmp/results/log.html ./
docker cp RobotFramework-mcp-persistent:/tmp/results/output.xml ./
```

## 🔧 Configuration Details

### Environment Variables (from .env)

| Variable | Value | Purpose |
|----------|-------|---------|
| `TESTS_DIR` | `./acceptance_tests` | Source directory for tests |
| `RESULTS_DIR` | `./robot_results` | Destination for test results |
| `CONTAINER_NAME` | `RobotFramework-mcp-persistent` | Docker container name |
| `IMAGE_NAME` | `robotframework-mcp:latest` | Docker image name |
| `BROWSER` | `chromium` | Browser for UI tests |
| `HEADLESS` | `true` | Run browser without GUI |
| `BASE_URL` | `http://app:5000` | Flask app URL |
| `TZ` | `Europe/Helsinki` | Container timezone |

### Network Configuration

All services are connected to `app-network` (bridge mode):
- **Flask App**: Accessible at `http://app:5000` from MCP container
- **MCP Server**: Can reach Flask app using service name `app`
- **Legacy Robot**: One-time test execution container

## 🛑 Stop and Cleanup

**Stop all services:**
```powershell
docker-compose down
```

**Stop only MCP server:**
```powershell
docker stop RobotFramework-mcp-persistent
```

**Remove all containers and volumes:**
```powershell
docker-compose down -v
```

**Rebuild after changes:**
```powershell
docker-compose build --no-cache robotframework-mcp
docker-compose up -d robotframework-mcp
```

## 🔍 Troubleshooting

### MCP Server Not Starting
```powershell
# Check logs
docker logs RobotFramework-mcp-persistent

# Inspect container
docker inspect RobotFramework-mcp-persistent

# Check if container is running
docker ps -a --filter name=RobotFramework-mcp-persistent
```

### Cannot Access Flask App from Tests
```powershell
# Verify network
docker network inspect testi_app-network

# Test connectivity from MCP container
docker exec RobotFramework-mcp-persistent curl http://app:5000

# Check Flask app logs
docker logs flask_app
```

### Test Results Not Appearing
```powershell
# Check volume mount
docker inspect RobotFramework-mcp-persistent | Select-String -Pattern "Mounts" -Context 0,20

# Verify results directory exists
ls .\robot_results\

# Check permissions
docker exec RobotFramework-mcp-persistent ls -la /tmp/results
```

### Browser Not Found Error
The container comes pre-installed with Chromium. If you see browser errors:
```powershell
# Verify browser installation
docker exec RobotFramework-mcp-persistent rfbrowser show-trace --help

# Reinstall browser (if needed)
docker exec RobotFramework-mcp-persistent rfbrowser init
```

## 📝 Notes

- The MCP server runs as a persistent container (uses `tail -f /dev/null` to stay alive)
- Tests are mounted read-only to prevent accidental modifications
- Results directory is read-write for storing test outputs
- The container uses a non-root user (`appuser`) for security
- All services share the same Docker network for easy communication

## 🔗 Additional Resources

- [Robot Framework Documentation](https://robotframework.org/)
- [Browser Library Documentation](https://marketsquare.github.io/robotframework-browser/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)

