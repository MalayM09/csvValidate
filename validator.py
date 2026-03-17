import warnings
import os
import pickle

# Suppress warnings about Python version and SSL (must be at the top)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", message=".*urllib3 v2 only supports OpenSSL 1.1.1+.*")

import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

def get_sheets_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    return service

def validate_entry(sheet_id, column_name=None, column_value=None, show_info=False):
    service = get_sheets_service()
    sheet = service.spreadsheets()
    
    # Fetch all data from the first sheet
    spreadsheet = sheet.get(spreadsheetId=sheet_id).execute()
    sheet_name = spreadsheet['sheets'][0]['properties']['title']
    
    # Using only the sheet name as the range will fetch all cells with values
    result = sheet.values().get(spreadsheetId=sheet_id, range=sheet_name).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
        return

    # Create DataFrame and infer objects (helps with types)
    df = pd.DataFrame(values[1:], columns=values[0]).convert_dtypes()
    
    # Strip whitespace from column names
    df.columns = df.columns.str.strip()
    
    if show_info:
        print(f"\nSheet Info: {sheet_name}")
        print(f"----------------------------------------")
        print(df.info())
        print("\nColumn Data Types:")
        print(df.dtypes)
        return

    # Check if the specified column exists
    target_col = column_name.strip()
    if target_col not in df.columns:
        print(f"Error: Column '{target_col}' not found in the sheet.")
        print(f"Available columns: {list(df.columns)}")
        return

    # Filter by the specified column and value
    row = df[df[target_col].astype(str).str.strip() == str(column_value).strip()]
    
    if row.empty:
        print(f"No entry found where '{target_col}' is '{column_value}'")
        return

    # Check validation requirements
    name = row['LIFE_ASSURED_NAME'].values[0] if 'LIFE_ASSURED_NAME' in row.columns else None
    email = row['EMAIL_ID'].values[0] if 'EMAIL_ID' in row.columns else None

    # Handle NA values safely
    is_name_present = not pd.isna(name) and str(name).strip() != ""
    is_email_present = not pd.isna(email) and str(email).strip() != ""

    print(f"\nValidation Result for {target_col}: {column_value}")
    print(f"----------------------------------------")
    print(f"LIFE_ASSURED_NAME: {'Present' if is_name_present else 'Missing'} ({name})")
    print(f"EMAIL_ID:          {'Present' if is_email_present else 'Missing'} ({email})")
    
    if is_name_present and is_email_present:
        print("\nResult: VALID")
    else:
        print("\nResult: INVALID")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Validate Google Sheet Entry')
    parser.add_argument('--sheet_id', required=True, help='Google Sheet ID')
    parser.add_argument('--column_name', default='POL_ID', help='The column name to search in (default: POL_ID)')
    parser.add_argument('--column_value', help='The value to search for in the specified column')
    parser.add_argument('--show_info', action='store_true', help='Show column names and data types')
    
    args = parser.parse_args()
    
    try:
        if not os.path.exists('credentials.json'):
            print("Error: credentials.json not found. Please place your Google Cloud credentials in the project directory.")
        else:
            if not args.show_info and args.column_value is None:
                parser.error("--column_value is required unless --show_info is used")
            validate_entry(args.sheet_id, args.column_name, args.column_value, args.show_info)
    except Exception as e:
        print(f"An error occurred: {e}")
