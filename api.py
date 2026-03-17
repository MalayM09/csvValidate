import os
import pickle
import warnings
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from typing import List, Optional

# Suppress warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", message=".*urllib3 v2 only supports OpenSSL 1.1.1+.*")

app = FastAPI()

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

def get_sheets_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                raise HTTPException(status_code=500, detail="credentials.json missing on server")
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('sheets', 'v4', credentials=creds)

class ValidationRequest(BaseModel):
    sheet_id: str
    column_name: str
    column_value: str

class ValidationResponse(BaseModel):
    valid: bool
    column_name: str
    column_value: str
    name: Optional[str]
    email: Optional[str]
    is_name_present: bool
    is_email_present: bool

@app.get("/api/sheet-info")
async def get_sheet_info(sheet_id: str):
    try:
        service = get_sheets_service()
        sheet = service.spreadsheets()
        spreadsheet = sheet.get(spreadsheetId=sheet_id).execute()
        sheet_name = spreadsheet['sheets'][0]['properties']['title']
        
        result = sheet.values().get(spreadsheetId=sheet_id, range=sheet_name).execute()
        values = result.get('values', [])
        
        if not values:
            return {"sheet_name": sheet_name, "columns": [], "row_count": 0}
            
        columns = [c.strip() for c in values[0]]
        return {
            "sheet_name": sheet_name,
            "columns": columns,
            "row_count": len(values) - 1
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/validate", response_model=ValidationResponse)
async def validate_entry(req: ValidationRequest):
    try:
        service = get_sheets_service()
        sheet = service.spreadsheets()
        
        spreadsheet = sheet.get(spreadsheetId=req.sheet_id).execute()
        sheet_name = spreadsheet['sheets'][0]['properties']['title']
        
        result = sheet.values().get(spreadsheetId=req.sheet_id, range=sheet_name).execute()
        values = result.get('values', [])

        if not values:
            raise HTTPException(status_code=404, detail="No data found in sheet")

        df = pd.DataFrame(values[1:], columns=values[0]).convert_dtypes()
        df.columns = df.columns.str.strip()
        
        target_col = req.column_name.strip()
        if target_col not in df.columns:
            raise HTTPException(status_code=400, detail=f"Column '{target_col}' not found")

        row = df[df[target_col].astype(str).str.strip() == str(req.column_value).strip()]
        
        if row.empty:
            raise HTTPException(status_code=404, detail=f"No entry found for {target_col}={req.column_value}")

        name = row['LIFE_ASSURED_NAME'].values[0] if 'LIFE_ASSURED_NAME' in row.columns else None
        email = row['EMAIL_ID'].values[0] if 'EMAIL_ID' in row.columns else None

        is_name_present = not pd.isna(name) and str(name).strip() != ""
        is_email_present = not pd.isna(email) and str(email).strip() != ""

        return {
            "valid": is_name_present and is_email_present,
            "column_name": target_col,
            "column_value": req.column_value,
            "name": str(name) if not pd.isna(name) else None,
            "email": str(email) if not pd.isna(email) else None,
            "is_name_present": is_name_present,
            "is_email_present": is_email_present
        }
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
