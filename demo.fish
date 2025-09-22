#!/usr/bin/env fish

echo "=== Step 1: Creating virtual environment ==="
python3 -m venv .venv

echo ""
echo "=== Step 2: Activating virtual environment ==="
source .venv/bin/activate.fish

echo ""
echo "=== Step 3: Installing dependencies ==="
pip install -r requirements.txt

echo ""
echo "=== Step 4: Building index ==="
python3 -m app.index --root .

echo ""
echo "=== Step 5: Starting API ==="
env PYTHONPATH=. uvicorn app.api:app --reload > uvicorn.log 2>&1 &
set API_PID $last_pid

# Wait and verify if API is up
sleep 3
if not curl -s http://127.0.0.1:8000/docs > /dev/null
    echo "❌ ERROR: API failed to start. See uvicorn.log for details."
    cat uvicorn.log
    exit 1
end

echo ""
echo "=== Step 6: Running test query ==="
curl "http://127.0.0.1:8000/search?q=emv&k=5" | jq .

echo ""
echo "=== Step 7: Stopping API (PID: $API_PID) ==="
if test -n "$API_PID"
    kill $API_PID
end

echo ""
echo "✅ Done"