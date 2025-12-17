# RobotFramework MCP Server - Setup Guide

This guide will help you set up the RobotFramework MCP Server for your project.

## What This Template Provides

This is a plug-and-play MCP (Model Context Protocol) server that allows AI assistants to:
- Run Robot Framework tests in a containerized environment
- Execute test suites with tags and variables
- List available tests in your project
- Access test results (reports, logs, XML output)

## Prerequisites

- Docker installed and running
- Your Robot Framework tests organized in a directory
- Basic familiarity with Docker and Robot Framework

## Quick Start

### Step 1: Clone or Copy This Template

Copy this entire `RobotFramework-MCP-server` directory to your project.

### Step 2: Configure Your Paths

1. Copy the example configuration file:

```bash
# Linux/macOS
cp .env.example .env

# Windows (PowerShell)
Copy-Item .env.example .env

# Windows (Command Prompt)
copy .env.example .env
```

2. Edit the `.env` file and update the paths to match your project:

```bash
# Example for Linux/macOS
TESTS_DIR=/home/myuser/myproject/tests
RESULTS_DIR=/home/myuser/myproject/results

# Example for Windows
TESTS_DIR=C:\Users\myuser\myproject\tests
RESULTS_DIR=C:\Users\myuser\myproject\results

# Or use relative paths (relative to this directory)
TESTS_DIR=../tests
RESULTS_DIR=../results
```

**Important Configuration Options:**

- `TESTS_DIR` - Path to your Robot Framework test files (mounted read-only at `/tests`)
- `RESULTS_DIR` - Path where test results will be saved (mounted read-write at `/results`)
- `CONTAINER_NAME` - Name for the Docker container (default: `RobotFramework-mcp-persistent`)
- `IMAGE_NAME` - Name for the Docker image (default: `robotframework-mcp:latest`)
- `NETWORK_MODE` - Docker network mode (default: `host`)

### Step 3: Build the Docker Image

```bash
# Linux/macOS
chmod +x setup_container.sh
./setup_container.sh

# Windows (PowerShell)
docker build -t robotframework-mcp:latest .
```

### Step 4: Start the Container

```bash
# Linux/macOS
chmod +x start-container.sh
./start-container.sh

# Windows (PowerShell) - The start-container.sh script works in Git Bash
# Or manually:
docker stop RobotFramework-mcp-persistent 2>$null
docker rm RobotFramework-mcp-persistent 2>$null

docker run -d `
  --name RobotFramework-mcp-persistent `
  --network host `
  --init `
  --entrypoint tail `
  -v "${PWD}\path\to\your\tests:/tests:ro" `
  -v "${PWD}\path\to\your\results:/results" `
  robotframework-mcp:latest -f /dev/null
```

### Step 5: Verify Setup

Check that the container is running:

```bash
docker ps --filter name=RobotFramework-mcp-persistent
```

You should see output like:

```
CONTAINER ID   IMAGE                        COMMAND               STATUS
abc123def456   robotframework-mcp:latest   "tail -f /dev/null"   Up 5 seconds
```

### Step 6: Configure Your AI Tool

Add the MCP server to your AI tool's configuration:

#### For Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "robotframework": {
      "command": "docker",
      "args": ["exec", "-i", "RobotFramework-mcp-persistent", "python", "/app/server.py"]
    }
  }
}
```

#### For VS Code AI Toolkit

Add to your AI Toolkit settings:

```json
{
  "mcp": {
    "servers": {
      "robotframework": {
        "command": "docker",
        "args": ["exec", "-i", "RobotFramework-mcp-persistent", "python", "/app/server.py"]
      }
    }
  }
}
```

#### For GitHub Copilot / Amazon Q

See the configuration files in `.vscode/agents/`, `.gitlab/agents/`, or `amazonq/agents/` directories for examples.

## Directory Structure

After setup, your project should look like this:

```
your-project/
├── RobotFramework-MCP-server/     # This MCP server
│   ├── .env                        # Your configuration (create from .env.example)
│   ├── .env.example                # Configuration template
│   ├── Dockerfile                  # Docker image definition
│   ├── server.py                   # MCP server implementation
│   ├── setup_container.sh          # Build script
│   ├── start-container.sh          # Start script
│   ├── SETUP.md                    # This file
│   └── README.md                   # General documentation
├── tests/                          # Your Robot Framework tests
│   ├── test_suite_1.robot
│   ├── test_suite_2.robot
│   └── ...
└── results/                        # Test results (created automatically)
    ├── output.xml
    ├── log.html
    └── report.html
```

## Configuration Details

### Environment Variables

The `.env` file supports these variables:

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `TESTS_DIR` | Path to your Robot tests | `./robot_tests` | `/home/user/project/tests` |
| `RESULTS_DIR` | Path for test results | `./robot_results` | `/home/user/project/results` |
| `CONTAINER_NAME` | Docker container name | `RobotFramework-mcp-persistent` | `my-rf-mcp` |
| `IMAGE_NAME` | Docker image name | `robotframework-mcp:latest` | `my-rf-mcp:v1` |
| `NETWORK_MODE` | Docker network mode | `host` | `bridge` |
| `BROWSER` | Default browser | `chromium` | `firefox` |
| `HEADLESS` | Headless browser mode | `true` | `false` |

### Network Configuration

- **`host` mode** (default): Container shares host's network. Use this if your tests need to access `localhost:PORT` services.
- **`bridge` mode**: Container gets its own network. Use if you have networking conflicts.
- **Custom network**: Set `NETWORK_MODE=your_network_name` to use an existing Docker network.

### Connecting to Your Application Under Test

**IMPORTANT**: The MCP server runs in its own separate Docker container. If your application also runs in Docker (via docker-compose or standalone), you need to ensure network connectivity between them.

#### Scenario 1: Application Running Directly on Host (Not in Docker)

**Example**: Your app runs via `npm start`, `python app.py`, or similar on `localhost:8000`

**Solution**: Use `host` network mode (default)

```bash
# .env
NETWORK_MODE=host
```

The MCP server container can access `http://localhost:8000` directly.

#### Scenario 2: Application Running in Docker Compose

**Example**: You have a `docker-compose.yml` for your application

```yaml
# Your application's docker-compose.yml
version: '3.8'
services:
  app:
    image: my-app:latest
    ports:
      - "8000:8000"
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

**Solution Option A**: Connect MCP container to the same network

1. Update your `.env`:
```bash
NETWORK_MODE=your-project_app-network
```

2. Start your application:
```bash
docker-compose up -d
```

3. Start the MCP server (it will join the network):
```bash
./start-container.sh
```

4. In your tests, use the service name:
```robotframework
*** Variables ***
${BASE_URL}    http://app:8000
```

**Solution Option B**: Use published ports with host network

Keep the default `NETWORK_MODE=host` and ensure your docker-compose publishes ports:

```yaml
services:
  app:
    ports:
      - "8000:8000"  # This makes the app available at localhost:8000
```

Then in tests use:
```robotframework
*** Variables ***
${BASE_URL}    http://localhost:8000
```

**Solution Option C**: Add MCP server to your docker-compose.yml

Instead of using the standalone scripts, add the MCP server as a service:

```yaml
# Add to your docker-compose.yml
services:
  app:
    image: my-app:latest
    ports:
      - "8000:8000"
    networks:
      - app-network

  robotframework-mcp:
    build: ./RobotFramework-MCP-server
    container_name: RobotFramework-mcp-persistent
    entrypoint: ["tail", "-f", "/dev/null"]
    volumes:
      - ./tests:/tests:ro
      - ./results:/results:rw
    networks:
      - app-network
    depends_on:
      - app

networks:
  app-network:
    driver: bridge
```

Then start everything together:
```bash
docker-compose up -d
```

Tests can use the service name:
```robotframework
*** Variables ***
${BASE_URL}    http://app:8000
```

#### Scenario 3: Application on Docker Desktop (Windows/Mac)

**Solution**: Use the special hostname `host.docker.internal`

```bash
# .env
NETWORK_MODE=bridge
```

In your tests:
```robotframework
*** Variables ***
${BASE_URL}    http://host.docker.internal:8000
```

#### Scenario 4: Application in a Custom Docker Network

**Example**: You created a network manually

```bash
docker network create my-test-network
docker run --name my-app --network my-test-network -p 8000:8000 my-app:latest
```

**Solution**: Use the custom network

```bash
# .env
NETWORK_MODE=my-test-network
```

Tests can use container names:
```robotframework
*** Variables ***
${BASE_URL}    http://my-app:8000
```

#### Quick Reference Table

| Your Application Runs In | NETWORK_MODE Setting | URL in Tests |
|--------------------------|---------------------|--------------|
| Host directly (npm, python, etc.) | `host` | `http://localhost:8000` |
| Docker Compose (published ports) | `host` | `http://localhost:8000` |
| Docker Compose (same network) | `your-project_app-network` | `http://service-name:8000` |
| Docker with custom network | `your-network-name` | `http://container-name:8000` |
| Docker Desktop (Win/Mac) | `bridge` | `http://host.docker.internal:8000` |

### Path Configuration

Paths can be:
- **Absolute**: `/home/user/project/tests` or `C:\Users\user\project\tests`
- **Relative**: `../tests` or `../../my-tests` (relative to this directory)

The `start-container.sh` script will automatically convert relative paths to absolute paths.

### Browser Configuration and Headless Mode

#### Default Test Library: Browser Library

This MCP server uses **Robot Framework Browser Library** (Playwright-based) as the default browser automation library.

**Why Browser Library?**
- Modern, faster, more reliable than SeleniumLibrary
- Built on Playwright (Microsoft)
- Better wait mechanisms and auto-waiting
- Native support for modern web features
- Better performance in containers

**Pre-installed browsers:**
- Chromium (default)
- Firefox
- Webkit

#### Headless Mode: Docker Requirement

**IMPORTANT: Headless mode MUST be `true` in Docker environments.**

Docker containers run without a graphical display server (no X11). Attempting to run browsers in non-headless mode will fail with errors like:
- `Failed to launch browser`
- `Display :0 not found`
- `Cannot open display`

**Configuration in `.env`:**
```bash
# This MUST be true for Docker (default and recommended)
HEADLESS=true

# Do NOT change to false unless you set up X11 forwarding
BROWSER=chromium
```

**In your Robot Framework tests:**
```robotframework
*** Settings ***
Library    Browser

*** Variables ***
# These can be overridden via MCP tools or command line
${BROWSER}     chromium
${HEADLESS}    true

*** Test Cases ***
My UI Test
    New Browser    ${BROWSER}    headless=${HEADLESS}
    New Page       http://example.com
    Get Title      ==    Example Domain
```

#### Running Non-Headless (Advanced - Not Recommended)

If you absolutely need to see the browser (for debugging), you have two options:

**Option 1: Use Playwright's Trace Viewer (Recommended)**
Instead of running non-headless, use tracing:

```robotframework
*** Settings ***
Library    Browser

*** Test Cases ***
Debug Test With Trace
    New Browser    chromium    headless=true
    New Context    # Enable tracing
    ...    recordVideo={'dir': '/results/videos'}
    ...    tracing={'screenshots': True, 'snapshots': True}
    New Page       http://example.com
    # Your test steps
    Close Browser
```

View traces afterward with: `npx playwright show-trace trace.zip`

**Option 2: X11 Forwarding (Linux Only - Advanced)**

1. Update `docker-compose.example.yml` or start script:
   ```yaml
   robotframework-mcp:
     environment:
       - DISPLAY=${DISPLAY}
       - HEADLESS=false
     volumes:
       - /tmp/.X11-unix:/tmp/.X11-unix:rw
   ```

2. On host, allow Docker to connect:
   ```bash
   xhost +local:docker
   ```

3. Update `.env`:
   ```bash
   HEADLESS=false
   ```

**Windows/Mac**: Non-headless mode requires VNC or X11 server setup (very complex, not recommended).

#### Browser Selection

Choose browser in `.env`:

```bash
# Chromium (default, fastest, most stable)
BROWSER=chromium

# Firefox (Gecko engine)
BROWSER=firefox

# Webkit (Safari engine)
BROWSER=webkit
```

Or override in MCP tool calls:
```json
{
  "variables": {
    "BROWSER": "firefox",
    "HEADLESS": "true"
  }
}
```

#### Troubleshooting Browser Issues

**Error: "Browser not found" or "Failed to launch browser"**

Solution:
```bash
# Rebuild the image to ensure rfbrowser init ran correctly
./setup_container.sh
```

**Error: "Display not found"**

Solution: Ensure `HEADLESS=true` in `.env`

**Slow test execution**

Solution: Chromium is fastest in containers. Ensure you're using:
```bash
BROWSER=chromium
HEADLESS=true
```

**Want to see what the browser is doing?**

Use Playwright's trace/video features instead of non-headless mode:
```robotframework
New Context    recordVideo={'dir': '/results/videos'}
```

**Playwright Configuration**

The Dockerfile includes proper Playwright configuration for Docker:
- `PLAYWRIGHT_BROWSERS_PATH=/ms-playwright` - Browser installation location
- Browsers are pre-installed during image build via `rfbrowser init`
- All browsers (Chromium, Firefox, Webkit) are headless-ready
- Screenshots and traces work automatically for debugging

These settings are pre-configured and don't need modification.

## Testing Your Setup

### Manual Test

Run a simple test to verify everything works:

```bash
# Execute the MCP server's list_tests tool
docker exec -i RobotFramework-mcp-persistent python /app/server.py
```

### Run Tests Directly

You can also run Robot Framework directly:

```bash
# Run all tests
docker exec RobotFramework-mcp-persistent robot --outputdir /tmp/results /tests

# Run with tags
docker exec RobotFramework-mcp-persistent robot --outputdir /tmp/results --include smoke /tests

# Run specific test
docker exec RobotFramework-mcp-persistent robot --outputdir /tmp/results --test "My Test Name" /tests
```

## Available MCP Tools

Once configured, your AI assistant can use these tools:

1. **list_tests** - List all test cases in your suite
   ```
   Input: suite_path (optional, defaults to /tests)
   Output: List of test names
   ```

2. **run_suite** - Run an entire test suite
   ```
   Input:
     - suite_path (optional)
     - include_tags (optional)
     - exclude_tags (optional)
     - variables (optional dict)
   Output: Test results with stdout, stderr, and artifact paths
   ```

3. **run_test_by_name** - Run a specific test
   ```
   Input:
     - test_name (required)
     - suite_path (optional)
     - variables (optional dict)
   Output: Test results with stdout, stderr, and artifact paths
   ```

## Troubleshooting

### Container Won't Start

```bash
# Check Docker is running
docker ps

# Rebuild the image
./setup_container.sh  # or docker build -t robotframework-mcp:latest .

# Check for errors
docker logs RobotFramework-mcp-persistent
```

### Tests Not Found

- Verify `TESTS_DIR` in `.env` points to correct location
- Check the path exists: `ls -la /path/to/your/tests`
- Ensure tests are `.robot` files with proper Robot Framework syntax
- Restart container after changing paths

### Permission Errors

```bash
# Linux/macOS - Make results directory writable
chmod 777 /path/to/results

# Check Docker has access to your files (Docker Desktop settings)
```

### Network Issues

If tests can't reach your application:

1. Check application is running: `curl http://localhost:YOUR_PORT`
2. Verify `NETWORK_MODE=host` in `.env`
3. Try `docker network ls` to see available networks
4. On Windows/Mac, you may need to use `host.docker.internal` instead of `localhost`

### Can't Access Test Results

Results are in two locations:
- Inside container: `/tmp/results/`
- On host: Path specified in `RESULTS_DIR` (if you mounted `/results`)

To copy results:
```bash
docker cp RobotFramework-mcp-persistent:/tmp/results/report.html ./
```

## Updating the Server

To update the MCP server or Robot Framework version:

1. Stop and remove the container:
   ```bash
   docker stop RobotFramework-mcp-persistent
   docker rm RobotFramework-mcp-persistent
   ```

2. Rebuild the image:
   ```bash
   ./setup_container.sh
   ```

3. Restart the container:
   ```bash
   ./start-container.sh
   ```

## Advanced Configuration

### Managing Robot Framework Versions

#### Default Behavior: Latest Versions

By default, the Dockerfile installs the **latest available versions** of:
- Robot Framework
- Robot Framework Browser Library
- Robot Framework Requests Library
- MCP SDK

This means each time you build the image, you'll get the newest versions available at that time.

#### Matching Versions to Your Project

**IMPORTANT**: If your project uses specific versions of Robot Framework and libraries, you should pin those versions in the Dockerfile to ensure consistency.

##### Step 1: Check Your Project's Versions

In your project directory, check what versions you're currently using:

```bash
# If you have a requirements.txt
cat requirements.txt | grep robotframework

# Or check installed versions in your local environment
pip list | grep robotframework

# Or check your project's package.json, Pipfile, pyproject.toml, etc.
```

Example output:
```
robotframework==7.1.0
robotframework-browser==18.0.0
robotframework-requests==0.9.6
```

##### Step 2: Update the Dockerfile

Edit the `Dockerfile` and pin the versions to match your project:

```dockerfile
# Robot Framework + Browser + Requests + MCP SDK
RUN pip install --no-cache-dir \
    robotframework==7.1.0 \
    robotframework-browser==18.0.0 \
    robotframework-requests==0.9.6 \
    "mcp[cli]" \
    && rfbrowser init
```

**Find these lines around line 22-27 in the Dockerfile.**

##### Step 3: Rebuild the Image

After changing versions, rebuild the Docker image:

```bash
# Linux/macOS
./setup_container.sh

# Windows
docker build -t robotframework-mcp:latest .
```

##### Step 4: Verify Installed Versions

Check what versions were installed:

```bash
# After starting the container
docker exec RobotFramework-mcp-persistent pip list | grep robotframework
```

#### Version Compatibility Notes

**Robot Framework Browser Library**:
- Requires Robot Framework 5.0 or later
- Requires Python 3.8 or later
- Includes Playwright browsers (Chromium, Firefox, Webkit)
- Major version changes may introduce breaking changes

**Robot Framework Requests Library**:
- Compatible with Robot Framework 3.1+
- Relatively stable across versions

**Checking Compatibility**:
```bash
# Visit PyPI for compatibility information
# https://pypi.org/project/robotframework-browser/
# https://pypi.org/project/robotframework-requests/
```

#### Using Latest Stable Versions

To always use the latest versions without pinning:

```dockerfile
RUN pip install --no-cache-dir \
    robotframework \
    robotframework-browser \
    robotframework-requests \
    "mcp[cli]" \
    && rfbrowser init
```

This is the **default configuration** in the template.

#### Using Version Ranges

For more flexibility, use version ranges:

```dockerfile
RUN pip install --no-cache-dir \
    "robotframework>=7.0,<8.0" \
    "robotframework-browser>=19.0,<20.0" \
    "robotframework-requests>=0.9.0" \
    "mcp[cli]" \
    && rfbrowser init
```

#### Example Scenarios

**Scenario 1**: Your project uses Robot Framework 6.1.1
```dockerfile
RUN pip install --no-cache-dir \
    robotframework==6.1.1 \
    robotframework-browser==17.5.2 \
    robotframework-requests==0.9.7 \
    "mcp[cli]" \
    && rfbrowser init
```

**Scenario 2**: You want to stay on major version 7
```dockerfile
RUN pip install --no-cache-dir \
    "robotframework>=7.0,<8.0" \
    robotframework-browser \
    robotframework-requests \
    "mcp[cli]" \
    && rfbrowser init
```

**Scenario 3**: Bleeding edge - always latest
```dockerfile
RUN pip install --no-cache-dir \
    robotframework \
    robotframework-browser \
    robotframework-requests \
    "mcp[cli]" \
    && rfbrowser init
```

### Additional Robot Framework Libraries

Add to `Dockerfile` before the `rfbrowser init` line:

```dockerfile
RUN pip install --no-cache-dir \
    robotframework-seleniumlibrary \
    robotframework-databaselibrary \
    your-custom-library
```

### Custom Environment Variables

Add to `.env`:

```bash
# Custom variables
BASE_URL=http://localhost:8080
API_KEY=your-api-key-here
```

These will be available in the container environment.

## Getting Help

- Check the main [README.md](README.md) for detailed usage examples
- Visit [Robot Framework Documentation](https://robotframework.org/)
- Check [MCP Specification](https://spec.modelcontextprotocol.io/)

## Next Steps

1. Configure your AI assistant to use this MCP server
2. Ask your AI assistant to list your tests: "List all Robot Framework tests"
3. Run tests through your AI assistant: "Run the smoke tests"
4. View test results in the `RESULTS_DIR` you configured

That's it! You now have a working RobotFramework MCP Server for your project.
