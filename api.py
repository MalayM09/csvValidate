import os
import pickle
import warnings
import pandas as pd
import io
import random
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from typing import List, Optional, Dict

# Suppress warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", message=".*urllib3 v2 only supports OpenSSL 1.1.1+.*")

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
TARGET_SHEET_ID = "1bMd0xDug32cCj9Ti3LB2b8DUsQA3fqreSjTfZQRZnHI"

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

class BatchItem(BaseModel):
    csv_row: Dict[str, str]
    sheet_row: Optional[Dict[str, str]] = None
    matches: Dict[str, bool] = {}
    is_valid: bool = False

@app.post("/api/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    
    try:
        content = await file.read()
        df = pd.read_csv(io.BytesIO(content)).convert_dtypes()
        df.columns = df.columns.str.strip()
        
        if df.empty:
            raise HTTPException(status_code=400, detail="CSV file is empty")
            
        # Sample 5-6 random entries
        sample_size = min(len(df), random.randint(5, 6))
        samples = df.sample(n=sample_size).to_dict(orient='records')
        
        # Clean the samples (convert NA to None for JSON)
        for row in samples:
            for k, v in row.items():
                if pd.isna(v):
                    row[k] = None
                else:
                    row[k] = str(v).strip()
                    
        return {"samples": samples, "total_rows": len(df)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CSV: {str(e)}")

@app.post("/api/validate-batch")
async def validate_batch(samples: List[Dict[str, str]]):
    try:
        service = get_sheets_service()
        sheet = service.spreadsheets()
        
        spreadsheet = sheet.get(spreadsheetId=TARGET_SHEET_ID).execute()
        sheet_name = spreadsheet['sheets'][0]['properties']['title']
        
        result = sheet.values().get(spreadsheetId=TARGET_SHEET_ID, range=sheet_name).execute()
        values = result.get('values', [])

        if not values:
            raise HTTPException(status_code=404, detail="No data found in Google Sheet")

        sheet_df = pd.DataFrame(values[1:], columns=values[0]).convert_dtypes()
        sheet_df.columns = sheet_df.columns.str.strip()
        
        batch_results = []
        
        for sample in samples:
            # We assume POL_ID is the unique identifier for comparison
            pol_id = sample.get('POL_ID')
            if not pol_id:
                batch_results.append({
                    "csv_row": sample,
                    "error": "Missing POL_ID in CSV row"
                })
                continue
                
            # Find matching row in Google Sheet
            matching_rows = sheet_df[sheet_df['POL_ID'].astype(str).str.strip() == str(pol_id).strip()]
            
            if matching_rows.empty:
                batch_results.append({
                    "csv_row": sample,
                    "sheet_row": None,
                    "is_valid": False,
                    "error": f"POL_ID {pol_id} not found in Google Sheet"
                })
                continue
            
            sheet_row = matching_rows.iloc[0].to_dict()
            # Clean sheet row
            for k, v in sheet_row.items():
                if pd.isna(v):
                    sheet_row[k] = None
                else:
                    sheet_row[k] = str(v).strip()
            
            # Compare critical fields
            matches = {}
            # We compare all fields that exist in BOTH
            for col in sample.keys():
                if col in sheet_row:
                    csv_val = str(sample[col]).strip() if sample[col] is not None else ""
                    sheet_val = str(sheet_row[col]).strip() if sheet_row[col] is not None else ""
                    matches[col] = (csv_val == sheet_val)
            
            # Check for name and email presence (original requirement)
            name_present = bool(sheet_row.get('LIFE_ASSURED_NAME'))
            email_present = bool(sheet_row.get('EMAIL_ID'))
            
            batch_results.append({
                "csv_row": sample,
                "sheet_row": sheet_row,
                "matches": matches,
                "is_valid": all(matches.values()) and name_present and email_present,
                "name_present": name_present,
                "email_present": email_present
            })
            
        return {"results": batch_results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
