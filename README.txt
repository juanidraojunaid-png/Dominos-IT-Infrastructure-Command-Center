# Domino's Infrastructure Command Center (Python)

## Run on Windows
1. Install Python 3.10 or newer.
2. Extract this folder.
3. Open Command Prompt in this folder.
4. Run:
   ```bat
   py -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   streamlit run app.py
   ```
5. Open the local address shown in the terminal (normally http://localhost:8501).

## Included
- Executive overview for 82 starter branch records
- Branch inventory search/filter and CSV export
- Host-1 / Host-2 detail view
- Event center
- CSV template upload
- Restart request queue (demo only)
- Deployment guide for live integration

## Important
This is a functional dashboard prototype, not a live monitoring system.
It does not connect to branch servers, collect actual CPU/RAM/disk/uptime, or restart servers.
Restart requests are only recorded in the demo session. Live deployment requires an authenticated
backend, database, secured connectivity, authorized monitoring agents, RBAC/MFA, approval workflow,
and audit logging. Do not enable remote restart without IT/security approval and testing.
