# Robot Framework MCP Server (Template)

A plug-and-play MCP (Model Context Protocol) server that enables AI assistants to run Robot Framework tests in a containerized environment.

## What is This?

This template provides:
- A Docker container with Robot Framework, Browser Library (Playwright), and Requests Library pre-installed
- An MCP server that exposes Robot Framework test execution as tools for AI assistants
- Easy configuration for any Robot Framework project
- Persistent container approach for fast test execution

## Key Features

- **Browser Library (Playwright) as Default** - Modern, fast browser automation for UI testing
- Run Robot Framework tests via AI assistants (Claude, Copilot, etc.)
- Execute test suites with tags and variables
- List available tests in your project
- Access test results (XML, HTML reports, logs)
- Pre-installed browsers: Chromium (default), Firefox, Webkit
- Includes Requests Library for API testing
- Headless mode enabled (required for Docker containers)

## Quick Start

**New to this template? Start here:**

1. Read [SETUP.md](SETUP.md) for detailed configuration instructions
2. Copy `.env.example` to `.env` and configure your paths
3. **(Optional)** Pin Robot Framework versions in `Dockerfile` to match your project (see [VERSIONS.md](VERSIONS.md))
4. Run the setup and start scripts
5. Configure your AI tool to use the MCP server

```bash
# 1. Configure
cp .env.example .env
# Edit .env with your test paths

# 2. (Optional) Match versions - Edit Dockerfile if needed
# See VERSIONS.md for guidance

# 3. Build
./setup_container.sh

# 4. Start
./start-container.sh

# 5. Configure your AI tool (see SETUP.md)
```

## AI Assistant Setup Prompt

Copy and paste this prompt to your AI assistant (GitHub Copilot, Claude, Amazon Q), replacing the values with your project details:

```

```

**Change these values:**
- `Tests directory` - Path to your Robot Framework test files
- `Results directory` - Where to save test results
- `Application` - `localhost:PORT` or `Docker: container_name on network_name`
- `Platform` - `Windows PowerShell`, `Linux`, or `macOS`
- `AI tool` - `GitHub Copilot`, `Claude Desktop`, or `Amazon Q`

## What Gets Installed

- **Robot Framework** (latest) + **Browser Library** (Playwright-based, default for UI testing)
- **Requests Library** for API testing
- **Chromium, Firefox, Webkit** browsers (headless-ready)
- **MCP SDK** for AI tool integration
- **Node.js 20.x** + Playwright dependencies

**Note**: Latest versions installed by default. See [VERSIONS.md](VERSIONS.md) to pin specific versions.

## Volume Mounts

The container mounts two directories:

| Host Path | Container Path | Mode | Purpose |
|-----------|----------------|------|---------|
| Your tests directory | `/tests` | read-only | Robot Framework test files |
| Your results directory | `/results` | read-write | Test execution results |

Configure these paths in the `.env` file.

## Available MCP Tools

Once configured, AI assistants can use these tools:

### 1. list_tests
List all test cases in your test suite.

**Parameters:**
- `suite_path` (optional): Path to test suite (default: `/tests`)

**Returns:**
```json
{
  "count": 10,
  "tests": [
    "Suite1.Test1",
    "Suite1.Test2",
    "Suite2.Test1"
  ]
}
```

### 2. run_suite
Execute an entire Robot Framework test suite.

**Parameters:**
- `suite_path` (optional): Path to test suite (default: `/tests`)
- `include_tags` (optional): Run only tests with these tags
- `exclude_tags` (optional): Skip tests with these tags
- `variables` (optional): Dictionary of Robot Framework variables

**Returns:**
```json
{
  "returncode": 0,
  "command": "robot --outputdir /tmp/results -v BROWSER:chromium ...",
  "stdout": "...",
  "stderr": "...",
  "artifacts": {
    "output_xml": "/tmp/results/output.xml",
    "log_html": "/tmp/results/log.html",
    "report_html": "/tmp/results/report.html"
  }
}
```

### 3. run_test_by_name
Run a specific test by name or pattern.

**Parameters:**
- `test_name` (required): Name or pattern of the test to run
- `suite_path` (optional): Path to test suite (default: `/tests`)
- `variables` (optional): Dictionary of Robot Framework variables

**Returns:**
Same format as `run_suite`.

## Running Tests Manually

You can also execute tests directly without MCP:

```bash
# Run all tests
docker exec RobotFramework-mcp-persistent robot --outputdir /tmp/results /tests

# Run tests by tag
docker exec RobotFramework-mcp-persistent robot --outputdir /tmp/results --include smoke /tests

# Run specific test
docker exec RobotFramework-mcp-persistent robot --outputdir /tmp/results --test "Test Name" /tests

# Run with variables
docker exec RobotFramework-mcp-persistent robot --outputdir /tmp/results \
  -v BROWSER:chromium \
  -v BASE_URL:http://localhost:8000 \
  /tests
```

## Common Tag Operations

Robot Framework supports powerful tag-based filtering:

```bash
# Run smoke tests only
docker exec RobotFramework-mcp-persistent robot --outputdir /tmp/results -i smoke /tests

# Exclude slow tests
docker exec RobotFramework-mcp-persistent robot --outputdir /tmp/results -e slow /tests

# Run tests with BOTH tags (AND)
docker exec RobotFramework-mcp-persistent robot --outputdir /tmp/results -i smokeANDui /tests

# Run tests with EITHER tag (OR)
docker exec RobotFramework-mcp-persistent robot --outputdir /tmp/results -i smokeORregression /tests
```

## Test Results

### Inside Container
Results are always written to `/tmp/results/`:
- `output.xml` - Detailed execution data
- `log.html` - Execution log with details
- `report.html` - Summary report

### On Host Machine
If you mounted a volume to `/results`, results are also available at your configured `RESULTS_DIR`.

### Copy Results from Container
```bash
docker cp RobotFramework-mcp-persistent:/tmp/results/report.html ./
docker cp RobotFramework-mcp-persistent:/tmp/results/log.html ./
docker cp RobotFramework-mcp-persistent:/tmp/results/output.xml ./
```

## Configuration

### Environment Variables (in .env)

| Variable | Default | Description |
|----------|---------|-------------|
| `TESTS_DIR` | `./robot_tests` | Path to your Robot Framework tests |
| `RESULTS_DIR` | `./robot_results` | Path for test results |
| `CONTAINER_NAME` | `RobotFramework-mcp-persistent` | Docker container name |
| `IMAGE_NAME` | `robotframework-mcp:latest` | Docker image name |
| `NETWORK_MODE` | `host` | Docker network mode |
| `BROWSER` | `chromium` | Default browser for tests |
| `HEADLESS` | `true` | Run browser in headless mode |

See `.env.example` for complete list and documentation.

### Runtime Variables

Override variables at runtime via MCP tools or in your test files. See [SETUP.md - Browser Configuration](SETUP.md#browser-configuration-and-headless-mode) for browser options and headless mode requirements.

## Network Configuration

The container uses `--network host` by default, allowing tests to access services on `localhost`.

- **On Linux**: `host` mode gives direct access to host network
- **On Windows/Mac**: `host` mode in Docker Desktop allows access to host services
- **Custom networks**: Set `NETWORK_MODE` in `.env` to use a specific Docker network

### Connecting to Applications in Docker

**Important**: If your application runs in Docker (docker-compose), you need to configure networking:

1. **Application with published ports**: Use `NETWORK_MODE=host` and access via `localhost:PORT`
2. **Application in custom network**: Set `NETWORK_MODE=your-network-name` and use service names in tests
3. **Docker Compose integration**: Add the MCP server as a service in your `docker-compose.yml` (see `docker-compose.example.yml`)

See [SETUP.md - Connecting to Your Application](SETUP.md#connecting-to-your-application-under-test) for detailed scenarios and examples.

## AI Tool Integration

### Claude Desktop

Add to `claude_desktop_config.json`:

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

### VS Code AI Toolkit

Add to AI Toolkit settings:

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

### GitHub Copilot / Amazon Q

See configuration examples in:
- `.vscode/agents/default.json`
- `.gitlab/agents/default.json`
- `amazonq/agents/default.json`

## Container Management

### View Status
```bash
docker ps --filter name=RobotFramework-mcp-persistent
```

### View Logs
```bash
docker logs RobotFramework-mcp-persistent
```

### Stop Container
```bash
docker stop RobotFramework-mcp-persistent
```

### Remove Container
```bash
docker rm RobotFramework-mcp-persistent
```

### Rebuild Everything
```bash
docker stop RobotFramework-mcp-persistent
docker rm RobotFramework-mcp-persistent
./setup_container.sh
./start-container.sh
```

## Troubleshooting

### Container Exits Immediately

The default entrypoint expects stdin (MCP stdio transport). The start script uses `tail -f /dev/null` to keep it running.

### Tests Can't Find Application

- Check your application is running
- Verify network mode: `NETWORK_MODE=host` in `.env`
- On Windows/Mac, try `host.docker.internal` instead of `localhost`

### Permission Errors

Linux/macOS:
```bash
chmod 777 /path/to/results
```

Windows: Check Docker Desktop has access to your drive in Settings > Resources > File Sharing

### Tests Not Found

- Verify `TESTS_DIR` path in `.env`
- Check tests are valid `.robot` files
- Restart container after changing configuration

### Browser Issues

The container includes:
- Chromium pre-installed via Playwright
- All browser dependencies
- Headless mode enabled by default

To use Firefox or Webkit, set `BROWSER` variable.

## Customization

### Match Versions to Your Project

**By default, the latest versions are installed.** To match your project's Robot Framework versions:

1. Check your project's versions:
   ```bash
   pip list | grep robotframework
   # or check requirements.txt
   ```

2. Edit `Dockerfile` (around line 22-27):
   ```dockerfile
   RUN pip install --no-cache-dir \
       robotframework==7.1.0 \
       robotframework-browser==18.0.0 \
       robotframework-requests==0.9.6 \
       "mcp[cli]"
   ```

3. Rebuild:
   ```bash
   ./setup_container.sh
   ```

See [SETUP.md - Managing Robot Framework Versions](SETUP.md#managing-robot-framework-versions) for detailed instructions and examples.

### Add More Libraries

Edit `Dockerfile` to add additional Robot Framework libraries:

```dockerfile
RUN pip install --no-cache-dir \
    robotframework \
    robotframework-browser \
    robotframework-requests \
    robotframework-seleniumlibrary \
    robotframework-databaselibrary \
    your-custom-library \
    "mcp[cli]" \
    && rfbrowser init
```

Then rebuild:
```bash
./setup_container.sh
```

### Custom Environment Variables

Add any variables to `.env` - they'll be available in the container environment.

## Architecture

```
┌─────────────────────────────────────┐
│       AI Assistant (Claude)         │
│  - Sends tool requests              │
│  - Receives test results            │
└────────────┬────────────────────────┘
             │ MCP Protocol (stdio)
             ▼
┌─────────────────────────────────────┐
│   Docker Container                  │
│  ┌───────────────────────────────┐  │
│  │   MCP Server (server.py)      │  │
│  │  - list_tests                 │  │
│  │  - run_suite                  │  │
│  │  - run_test_by_name           │  │
│  └──────────┬────────────────────┘  │
│             │                        │
│  ┌──────────▼────────────────────┐  │
│  │   Robot Framework             │  │
│  │  - Browser Library            │  │
│  │  - Requests Library           │  │
│  │  - Chromium browser           │  │
│  └───────────────────────────────┘  │
│                                      │
│  Volumes:                            │
│  - /tests (your tests, read-only)   │
│  - /results (output, read-write)    │
└─────────────────────────────────────┘
```

## Files in This Template

```
RobotFramework-MCP-server/
├── .env.example              # Configuration template (copy to .env)
├── Dockerfile                # Docker image definition
├── server.py                 # MCP server implementation (FastMCP)
├── setup_container.sh        # Build script (Linux/macOS)
├── start-container.sh        # Container start script (Linux/macOS)
├── docker-compose.example.yml # Example docker-compose integration
├── SETUP.md                  # Detailed setup instructions
├── VERSIONS.md               # Version management guide
├── PROJECT_STRUCTURE.md      # Directory structure examples
└── README.md                 # This file
```

## Documentation

- **[SETUP.md](SETUP.md)** - Complete setup guide with step-by-step instructions
- **[VERSIONS.md](VERSIONS.md)** - Robot Framework version management and compatibility guide
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Directory structure examples and best practices
- **[Robot Framework Docs](https://robotframework.org/)** - Official RF documentation
- **[Browser Library Docs](https://marketsquare.github.io/robotframework-browser/)** - Browser Library guide
- **[MCP Specification](https://spec.modelcontextprotocol.io/)** - Model Context Protocol spec
- **[FastMCP SDK](https://github.com/jlowin/fastmcp)** - Python MCP SDK

## Requirements

- Docker
- Robot Framework test files
- (Optional) AI assistant that supports MCP protocol

## Support

For issues specific to:
- **Robot Framework**: Check [Robot Framework documentation](https://robotframework.org/)
- **Browser Library**: Check [Browser Library documentation](https://marketsquare.github.io/robotframework-browser/)
- **MCP Protocol**: Check [MCP specification](https://spec.modelcontextprotocol.io/)
- **This template**: Check [SETUP.md](SETUP.md) troubleshooting section

## License

This template is provided as-is for use with Robot Framework projects.

## Next Steps

1. Read [SETUP.md](SETUP.md) for detailed configuration
2. Copy `.env.example` to `.env` and configure
3. Build and start the container
4. Configure your AI assistant
5. Start running tests through your AI assistant!
