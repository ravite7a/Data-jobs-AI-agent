import os
import json
import base64

raw = os.environ.get("GOOGLE_CREDENTIALS", "").strip()

print(f"Length of GOOGLE_CREDENTIALS: {len(raw)}")
print(f"First 50 chars: {raw[:50]}")
print(f"Last 10 chars: {raw[-10:]}")

# Try base64 decode
try:
    decoded = base64.b64decode(raw).decode("utf-8")
    data = json.loads(decoded)
    print(f"SUCCESS: base64 decoded and parsed as JSON")
    print(f"project_id: {data.get('project_id')}")
    print(f"client_email: {data.get('client_email')}")
except Exception as e1:
    print(f"base64 decode failed: {e1}")
    # Try raw JSON
    try:
        data = json.loads(raw)
        print(f"SUCCESS: parsed as raw JSON")
        print(f"project_id: {data.get('project_id')}")
        print(f"client_email: {data.get('client_email')}")
    except Exception as e2:
        print(f"raw JSON parse also failed: {e2}")
