# Load Tests

Run against a running backend service:

```bash
locust -f cerberus/backend/tests/load/locustfile.py --host http://127.0.0.1:8000
```

Focus areas:
- leaderboard read throughput
- flag submission concurrency
- notification dispatch pressure
