#!/usr/bin/env bash
set -euo pipefail

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Load configuration from .env file if it exists
if [ -f "${SCRIPT_DIR}/.env" ]; then
    echo "📋 Loading configuration from .env file..."
    # Export variables from .env file, ignoring comments and empty lines
    set -a
    source "${SCRIPT_DIR}/.env"
    set +a
else
    echo "⚠️  No .env file found. Copy .env.example to .env and configure it first!"
    echo "   cp .env.example .env"
    echo ""
    echo "Using default values..."
fi

# Set defaults if not provided in .env
CONTAINER_NAME="${CONTAINER_NAME:-RobotFramework-mcp-persistent}"
IMAGE_NAME="${IMAGE_NAME:-robotframework-mcp:latest}"
TESTS_DIR="${TESTS_DIR:-${SCRIPT_DIR}/robot_tests}"
RESULTS_DIR="${RESULTS_DIR:-${SCRIPT_DIR}/robot_results}"
NETWORK_MODE="${NETWORK_MODE:-host}"

# Convert relative paths to absolute paths
if [[ ! "$TESTS_DIR" = /* ]]; then
    TESTS_DIR="$(cd "${SCRIPT_DIR}" && cd "$(dirname "${TESTS_DIR}")" && pwd)/$(basename "${TESTS_DIR}")"
fi

if [[ ! "$RESULTS_DIR" = /* ]]; then
    RESULTS_DIR="$(cd "${SCRIPT_DIR}" && mkdir -p "$(dirname "${RESULTS_DIR}")" && cd "$(dirname "${RESULTS_DIR}")" && pwd)/$(basename "${RESULTS_DIR}")"
fi

echo "🚀 Starting persistent MCP Robot Framework container..."

# Stop and remove the persistent container if it exists
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$" || true; then
    echo "🛑 Stopping and removing existing persistent container..."
    docker stop "$CONTAINER_NAME" 2>/dev/null || true
    docker rm -f "$CONTAINER_NAME" 2>/dev/null || true
fi

# Clean up any containers using the robotframework-mcp:latest image
echo "🧹 Cleaning up any containers using robotframework-mcp:latest image..."
docker ps -a --filter "ancestor=${IMAGE_NAME}" --format '{{.Names}}' | while read -r name; do
    if [ -n "$name" ]; then
        echo "   Removing: $name"
        docker stop "$name" 2>/dev/null || true
        docker rm -f "$name" 2>/dev/null || true
    fi
done || true

# Clean up any containers with RobotFramework-mcp in the name
echo "🧹 Cleaning up any containers with 'RobotFramework-mcp' in name..."
docker ps -a --format '{{.Names}}' | grep "RobotFramework-mcp" | while read -r name; do
    if [ -n "$name" ]; then
        echo "   Removing: $name"
        docker stop "$name" 2>/dev/null || true
        docker rm -f "$name" 2>/dev/null || true
    fi
done || true

# Ensure results directory exists
mkdir -p "${RESULTS_DIR}"

echo ""
echo "📦 Starting new persistent container..."
echo "   Tests from: $TESTS_DIR"
echo "   Results to: $RESULTS_DIR"
echo ""

# Start container in background with tail to keep it running
docker run -d \
    --name "$CONTAINER_NAME" \
    --network "$NETWORK_MODE" \
    --init \
    --entrypoint tail \
    -v "${TESTS_DIR}:/tests:ro" \
    -v "${RESULTS_DIR}:/results:rw" \
    "$IMAGE_NAME" \
    -f /dev/null

echo ""
echo "✅ Persistent container started: $CONTAINER_NAME"
echo ""
echo "🔍 Verifying container is running..."
docker ps --filter "name=$CONTAINER_NAME"
echo ""
# Simplified usage guidance (no Amazon Q specific instructions)
echo "📝 Use docker exec to run the MCP server:"
echo '   /usr/bin/docker exec -i RobotFramework-mcp-persistent python /app/server.py'
echo ""
echo "🛑 To stop: docker stop $CONTAINER_NAME"
echo "🗑️  To remove: docker rm $CONTAINER_NAME"