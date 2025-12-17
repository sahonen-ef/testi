#!/usr/bin/env python3
import json
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from holidays_finland_user_year import count_working_day_holidays

def handle_mcp_request(request):
    """Handle MCP protocol requests"""
    if request.get("method") == "tools/list":
        return {
            "tools": [{
                "name": "get_finnish_holidays",
                "description": "Get Finnish public holidays that fall on working days",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "year": {"type": "integer", "minimum": 1900, "maximum": 2100},
                        "lang": {"type": "string", "enum": ["en", "fi", "sv", "no", "et"]}
                    },
                    "required": ["year"]
                }
            }]
        }
    elif request.get("method") == "tools/call":
        tool_name = request["params"]["name"]
        if tool_name == "get_finnish_holidays":
            args = request["params"]["arguments"]
            year = args.get("year")
            lang = args.get("lang", "en")
            
            try:
                count, holidays = count_working_day_holidays(year, lang=lang)
                result = {
                    "year": year,
                    "count": count,
                    "holidays": [
                        {
                            "date": d.strftime('%Y-%m-%d'),
                            "weekday": d.strftime('%A'),
                            "name": name
                        } for d, name in holidays
                    ]
                }
                return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
            except Exception as e:
                return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
    
    return {"error": "Unknown method"}

def main():
    """Main MCP server loop"""
    print("MCP Server is running. Type 'exit' to quit.", file=sys.stderr)  # Redirect to stderr
    for line in sys.stdin:
        try:
            request = json.loads(line)
            response = handle_mcp_request(request)
            print(json.dumps(response), flush=True)
        except Exception as e:
            print(json.dumps({"error": str(e)}), flush=True)

if __name__ == "__main__":
    main()