import os
import json
import sys
import argparse
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_service():
    creds_json = os.environ.get('GOOGLE_SHEETS_CREDENTIALS_JSON')
    if not creds_json:
        print("Error: GOOGLE_SHEETS_CREDENTIALS_JSON environment variable not set.")
        sys.exit(1)
    
    try:
        info = json.loads(creds_json)
        creds = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
        return build('sheets', 'v4', credentials=creds)
    except Exception as e:
        print(f"Error initializing Google Sheets service: {e}")
        sys.exit(1)

def create_spreadsheet(title):
    service = get_service()
    spreadsheet = {'properties': {'title': title}}
    spreadsheet = service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId').execute()
    print(f"Created spreadsheet ID: {spreadsheet.get('spreadsheetId')}")

def read_spreadsheet(spreadsheet_id, range_name):
    service = get_service()
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])
    if not values:
        print("No data found.")
    else:
        print(json.dumps(values))

def append_values(spreadsheet_id, range_name, values_json):
    service = get_service()
    try:
        values = json.loads(values_json)
        if not isinstance(values, list):
            values = [values]
        
        body = {'values': [values] if not isinstance(values[0], list) else values}
        result = service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption='RAW', body=body).execute()
        print(f"{result.get('updates').get('updatedCells')} cells appended.")
    except Exception as e:
        print(f"Error appending values: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Google Sheets CLI integration')
    subparsers = parser.add_subparsers(dest='command')

    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new spreadsheet')
    create_parser.add_argument('--title', required=True, help='Title of the new spreadsheet')

    # Read command
    read_parser = subparsers.add_parser('read', help='Read a range of values')
    read_parser.add_argument('--spreadsheet-id', required=True, help='The spreadsheet ID')
    read_parser.add_argument('--range', required=True, help='The range to read (e.g. Sheet1!A1:B10)')

    # Append command
    append_parser = subparsers.add_parser('append', help='Append data to a sheet')
    append_parser.add_argument('--spreadsheet-id', required=True, help='The spreadsheet ID')
    append_parser.add_argument('--range', required=True, help='The range to append to')
    append_parser.add_argument('--values', required=True, help='JSON string of values to append (e.g. ["date", "desc", 42])')

    args = parser.parse_args()

    if args.command == 'create':
        create_spreadsheet(args.title)
    elif args.command == 'read':
        read_spreadsheet(args.spreadsheet_id, args.range)
    elif args.command == 'append':
        append_values(args.spreadsheet_id, args.range, args.values)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
