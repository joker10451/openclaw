---
name: google-sheets
description: "Interact with Google Sheets API. Create, read, and update spreadsheets using service account credentials. Requires GOOGLE_SHEETS_CREDENTIALS_JSON env var."
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "requires":
          {
            "bins": ["python3"],
            "env": ["GOOGLE_SHEETS_CREDENTIALS_JSON"],
          },
        "install":
          [
            {
              "id": "pip-sheets",
              "kind": "pip",
              "packages": ["google-auth", "google-api-python-client"],
              "label": "Install Google API clients (pip)",
            },
          ],
      },
  }
---

# Google Sheets Skill

Use this skill to automate tasks in Google Sheets. You can create new sheets, append data, or read specific ranges.

## Configuration

Ensure you have a Service Account and the `GOOGLE_SHEETS_CREDENTIALS_JSON` environment variable contains the full JSON key.

## Usage Examples

### Append a row
```bash
python3 scripts/google_sheets_ops.py append --spreadsheet-id <ID> --range "Sheet1!A1" --values '["2023-10-27", "Sample data", 123.45]'
```

### Create a new spreadsheet
```bash
python3 scripts/google_sheets_ops.py create --title "My New Report"
```

### Read a range
```bash
python3 scripts/google_sheets_ops.py read --spreadsheet-id <ID> --range "Sheet1!A1:C10"
```
