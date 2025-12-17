import subprocess
import json
import sys

# Start the MCP server
process = subprocess.Popen(
    ["python", "my_server.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

print("MCP Server is running. Type 'exit' to quit.", file=sys.stderr)  # Redirect to stderr

while True:
    # Get year input from the user
    year = input("Enter a year (or type 'exit' to quit): ")
    if year.lower() == "exit":
        break

    try:
        year = int(year)
        # Create the request
        request = {
            "method": "tools/call",
            "params": {
                "name": "get_finnish_holidays",
                "arguments": {
                    "year": year,
                    "lang": "en"
                }
            }
        }

        # Send the request to the server
        process.stdin.write(json.dumps(request) + "\n")
        process.stdin.flush()

        # Read and print the response
        response = process.stdout.readline()
        print("Response:", response)

    except ValueError:
        print("Invalid year. Please enter a valid integer.", file=sys.stderr)  # Redirect to stderr

# Close the server
process.terminate()