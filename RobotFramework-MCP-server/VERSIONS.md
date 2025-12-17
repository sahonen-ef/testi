# Robot Framework Version Reference

This file provides guidance on Robot Framework and library versions for the MCP Server template.

## Default Configuration

**The template uses the latest stable versions by default.**

When you build the Docker image, it installs:
- Latest Robot Framework
- Latest Robot Framework Browser Library
- Latest Robot Framework Requests Library
- Latest MCP SDK

## How to Check Your Project's Versions

### Method 1: Using pip
```bash
pip list | grep robotframework
```

### Method 2: Check requirements.txt
```bash
cat requirements.txt | grep robotframework
```

### Method 3: In Python
```python
import robot
import Browser
import RequestsLibrary

print(f"Robot Framework: {robot.__version__}")
print(f"Browser Library: {Browser.__version__}")
print(f"Requests Library: {RequestsLibrary.__version__}")
```

### Method 4: Via Robot Framework
```bash
robot --version
```

## How to Pin Versions in Dockerfile

Edit the `Dockerfile` around line 22-27:

```dockerfile
RUN pip install --no-cache-dir \
    robotframework==X.Y.Z \
    robotframework-browser==X.Y.Z \
    robotframework-requests==X.Y.Z \
    "mcp[cli]" \
    && rfbrowser init
```

Replace `X.Y.Z` with your desired versions.

## Version Compatibility Matrix

### Robot Framework Core

| Version | Python Support | Released | Notes |
|---------|---------------|----------|-------|
| 7.x | 3.8+ | 2024 | Latest stable, recommended |
| 6.x | 3.6+ | 2022 | Mature, widely used |
| 5.x | 3.6+ | 2021 | Older but stable |

### Robot Framework Browser Library

| Version | Robot Framework | Python | Playwright | Notes |
|---------|----------------|--------|------------|-------|
| 19.x | 5.0+ | 3.8+ | Latest | Latest features |
| 18.x | 5.0+ | 3.8+ | 1.44+ | Stable |
| 17.x | 5.0+ | 3.8+ | 1.39+ | Previous stable |

**Key Requirements**:
- Requires Robot Framework 5.0 or later
- Requires Python 3.8 or later
- Node.js 18+ required for Playwright

### Robot Framework Requests Library

| Version | Robot Framework | Python | Requests | Notes |
|---------|----------------|--------|----------|-------|
| 0.9.x | 3.1+ | 3.6+ | 2.x | Current stable |
| 0.8.x | 3.1+ | 3.6+ | 2.x | Previous stable |

**Key Requirements**:
- Compatible with Robot Framework 3.1+
- Very stable library, rarely breaks

## Common Version Combinations

### Latest Everything (Default)
```dockerfile
RUN pip install --no-cache-dir \
    robotframework \
    robotframework-browser \
    robotframework-requests \
    "mcp[cli]" \
    && rfbrowser init
```

### Conservative (Pinned Major Versions)
```dockerfile
RUN pip install --no-cache-dir \
    "robotframework>=7.0,<8.0" \
    "robotframework-browser>=19.0,<20.0" \
    "robotframework-requests>=0.9,<1.0" \
    "mcp[cli]" \
    && rfbrowser init
```

### Specific Versions (Maximum Stability)
```dockerfile
RUN pip install --no-cache-dir \
    robotframework==7.1.1 \
    robotframework-browser==19.0.0 \
    robotframework-requests==0.9.7 \
    "mcp[cli]" \
    && rfbrowser init
```

### Older Project (Robot Framework 6.x)
```dockerfile
RUN pip install --no-cache-dir \
    robotframework==6.1.1 \
    robotframework-browser==17.5.2 \
    robotframework-requests==0.9.7 \
    "mcp[cli]" \
    && rfbrowser init
```

## Breaking Changes to Watch For

### Robot Framework 7.0
- Python 3.8+ required (dropped 3.7)
- Some keyword argument changes
- New features: WHILE loops, TRY/EXCEPT improvements

### Robot Framework 6.0
- Python 3.6+ required (dropped 2.7 and 3.5)
- Native IF/ELSE syntax
- Native inline IF
- Native CONTINUE and BREAK

### Browser Library Major Versions
- Major version bumps often align with Playwright updates
- May include breaking changes in keywords
- Check release notes before upgrading

## Troubleshooting Version Issues

### Error: "Module not found" or "Import Error"
**Cause**: Incompatible versions or missing dependencies

**Solution**: Check version compatibility matrix above

### Error: "Keyword not found"
**Cause**: Using keywords from newer library version

**Solution**: Either upgrade library or use older keyword syntax

### Error: "Browser initialization failed"
**Cause**: Playwright version mismatch

**Solution**: Ensure `rfbrowser init` runs after installation

### Tests pass locally but fail in container
**Cause**: Version mismatch between local and container

**Solution**:
1. Check local versions: `pip list | grep robotframework`
2. Pin those versions in Dockerfile
3. Rebuild container

## Verifying Installed Versions in Container

After building and starting the container:

```bash
# Check all installed packages
docker exec RobotFramework-mcp-persistent pip list

# Check Robot Framework version
docker exec RobotFramework-mcp-persistent robot --version

# Check specific libraries
docker exec RobotFramework-mcp-persistent pip list | grep robotframework
```

## Where to Find Version Information

- **Robot Framework**: https://github.com/robotframework/robotframework/releases
- **Browser Library**: https://github.com/MarketSquare/robotframework-browser/releases
- **Requests Library**: https://github.com/MarketSquare/robotframework-requests/releases
- **PyPI Package Index**: https://pypi.org/
  - https://pypi.org/project/robotframework/
  - https://pypi.org/project/robotframework-browser/
  - https://pypi.org/project/robotframework-requests/

## Recommended Approach

1. **For new projects**: Use latest versions (default configuration)
2. **For existing projects**: Pin to your current versions
3. **For CI/CD**: Always pin specific versions for reproducibility
4. **For development**: Use version ranges (e.g., `>=7.0,<8.0`)

## Getting Help

If you encounter version compatibility issues:

1. Check the [SETUP.md](SETUP.md) troubleshooting section
2. Review the library's GitHub issues
3. Check PyPI for compatibility requirements
4. Test version combinations in a local virtual environment first

## Quick Commands Reference

```bash
# Check what's in your Dockerfile
grep "robotframework" Dockerfile

# Check what's in the built image
docker run --rm robotframework-mcp:latest pip list | grep robotframework

# Check what's in the running container
docker exec RobotFramework-mcp-persistent pip list | grep robotframework

# Rebuild with new versions
docker build -t robotframework-mcp:latest . --no-cache
```

## Version History of This Template

- **Initial Release**: Used specific pinned versions (RF 7.3.2, Browser 19.12.0, Requests 0.9.7)
- **Current Release**: Uses latest stable versions by default (no pinning)

Users are encouraged to pin versions in production environments for stability.
