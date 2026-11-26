"""Keeps data/mcp-tools.json in step with the price server's own tool list (a tools/list answer, plain JSON or one SSE event)."""
import json
import sys
from pathlib import Path

raw = Path(sys.argv[1]).read_text(encoding="utf-8") if Path(sys.argv[1]).exists() else ""
start, end = raw.find("{"), raw.rfind("}")
try:
    tools = json.loads(raw[start:end + 1])["result"]["tools"]
except (ValueError, KeyError, TypeError):
    sys.exit(0)  # the server did not answer: keep the last list
out = Path(__file__).resolve().parent.parent / "data" / "mcp-tools.json"
out.write_text(json.dumps([{"name": t["name"], "description": t["description"]} for t in tools], indent=1), encoding="utf-8")
