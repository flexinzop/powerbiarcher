# Archer → Power BI (via REST API)

## Overview
Proof-of-concept in Python that **authenticates to RSA Archer**, **retrieves records via the Content API**, and **normalizes the JSON into a pandas DataFrame**—a convenient step before exporting to CSV or connecting your BI tool. The script logs into Archer to obtain a session token, then calls a Content API endpoint and flattens the response for analysis/ingestion.

## Features
- **Archer session login** using `api/core/security/login` to obtain a `SessionToken`.
- **Content API fetch** using HTTP Basic auth (`session-id` + token) against your application endpoint.
- **JSON → DataFrame** with `pandas.json_normalize([...], record_path=['value'])` for tabular output.
- **Config via JSON**: instance, username, domain, password read from `credentials.json`.

## Prerequisites
- **Python** 3.10+ (tested with 3.12).
- Python packages: `requests`, `pandas` (and `urllib3` present by default).
- Network access to your Archer instance (URLs currently use private IPs—adjust to your environment).
- An Archer account authorized to use the **Content API** for the target application.

## Installation
1. **Clone** the repository:
   ```bash
   git clone https://github.com/flexinzop/powerbiarcher
   cd powerbiarcher
   ```
2. (Optional) Create a **virtual environment** and install deps:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate

   pip install requests pandas
   ```
3. Create a **`credentials.json`** file and fill in your Archer credentials:
   ```json
   {
     "InstanceName": "<YourInstance>",
     "UserName": "<your.user>",
     "UserDomain": "",
     "Password": "<your-password>"
   }
   ```
   > ⚠️ By default the script points to a Windows local path. Adjust the **path** as in *Configuration* below.

## Usage
Execute:
```bash
python getToken.py
```
The script:
1) sends `InstanceName/UserName/UserDomain/Password` to `.../api/core/security/login`,  
2) extracts `SessionToken`,  
3) performs `GET` on the **Content API** endpoint,  
4) normalizes the response and **prints a DataFrame** to the console.

## Configuration
Open `getToken.py` and adjust:

- **Path to `credentials.json`** (the `open(...)` line):
  ```python
  with open(r"C:\path\to\your\credentials.json") as json_file:
      data = json.load(json_file)
  ```
- **Login endpoint (HTTPS recommended)**:
  ```python
  url = "https://<your-archer-host>/rsaarcher/api/core/security/login"
  ```
- **Content API endpoint** (replace with your application alias):
  ```python
  contentURL = "https://<your-archer-host>/rsaarcher/contentapi/<AppAlias>/<Resource>"
  # Example: "/contentapi/RestAPI_1/RestAPI"
  ```
- **Content API authentication** (Archer standard):
  ```python
  basic = HTTPBasicAuth('session-id', token)
  ```

## Export to CSV / Power BI
After you obtain the `DataFrame` (`df`), you can export to CSV and connect in Power BI Desktop:
```python
df.to_csv("archer_export.csv", index=False)
```
In **Power BI Desktop**: *Get Data → Text/CSV* and select `archer_export.csv`.

> Future/alternative: turn this script into a small API/Job that writes directly to a table (or uses a Power BI push dataset).

## Security Notes
- Do **not** commit `credentials.json`. Use environment variables or a secret manager in production.
- Prefer **HTTPS** for all endpoints.
- Restrict the user's permissions to only what’s required to read the target application.

## Troubleshooting
- **401/403**: check user permissions and whether the Content API app/endpoint is correct.
- **Timeout/SSL**: verify host, certificates, and firewall/VPN.
- **Schema**: `record_path=['value']` assumes the typical Content API format; adjust to your app’s payload.

---

**Author:** Samuel Andrade Pimenta
