import os
import warnings
import pandas as pd
import io
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict

# Suppress warnings
warnings.filterwarnings("ignore", category=FutureWarning)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Golden Records Data (Hardcoded as requested)
GOLDEN_RECORDS = [
    {
        "LIFE_ASSURED_NAME": "Neha Telang", "POL_ID": "118841428", "POL_ISSUED": "08-12-2022",
        "PLAN_NAME": "Axis Max Life Smart Secure Plus Plan_60 Pay_Online", "POL_TYPE": "TRAD",
        "CEASE_REASON_CD": "R", "CEASE_REASON_DESC": "Automatic Cease Reason", "POLICY_STATUS": "Premium paying",
        "BILL_MODE": "Annual", "BILL_TYPE": "Direct Bill", "PREVIOUS_DUE_DATE": "", "CPTD": "",
        "PTD": "08-12-2026", "C2P": "0", "MODEL_PRM": "44397.36", "AFYP": "44397.36",
        "TOTAL_SERV_TAX": "", "EMAIL_ID": "nehatelang@gmail.com"
    },
    {
        "LIFE_ASSURED_NAME": "TARLOCHAN SINGH", "POL_ID": "119771244", "POL_ISSUED": "03-01-2023",
        "PLAN_NAME": "Axis Max Life Smart Secure Plus Plan_60 Pay_Online", "POL_TYPE": "TRAD",
        "CEASE_REASON_CD": "R", "CEASE_REASON_DESC": "Automatic Cease Reason", "POLICY_STATUS": "Premium paying",
        "BILL_MODE": "Annual", "BILL_TYPE": "Direct Bill", "PREVIOUS_DUE_DATE": "", "CPTD": "",
        "PTD": "03-01-2027", "C2P": "0", "MODEL_PRM": "26369.24", "AFYP": "26369.24",
        "TOTAL_SERV_TAX": "", "EMAIL_ID": "TSINGH.GHADYOKE@GMAIL.COM"
    },
    {
        "LIFE_ASSURED_NAME": "Aditya Jain", "POL_ID": "140183146", "POL_ISSUED": "08-02-2023",
        "PLAN_NAME": "Axis Max Life Smart Secure Plus Plan_Regular_Online", "POL_TYPE": "TRAD",
        "CEASE_REASON_CD": "R", "CEASE_REASON_DESC": "Automatic Cease Reason", "POLICY_STATUS": "Premium paying",
        "BILL_MODE": "Annual", "BILL_TYPE": "Direct Bill", "PREVIOUS_DUE_DATE": "", "CPTD": "",
        "PTD": "08-02-2026", "C2P": "24009", "MODEL_PRM": "24009", "AFYP": "24009",
        "TOTAL_SERV_TAX": "", "EMAIL_ID": "aditya.jain.1396@gmail.com"
    },
    {
        "LIFE_ASSURED_NAME": "Samir Saurabh", "POL_ID": "140462425", "POL_ISSUED": "27-01-2023",
        "PLAN_NAME": "Axis Max Life Smart Secure Plus Plan_Regular_Online", "POL_TYPE": "TRAD",
        "CEASE_REASON_CD": "R", "CEASE_REASON_DESC": "Automatic Cease Reason", "POLICY_STATUS": "Premium paying",
        "BILL_MODE": "Annual", "BILL_TYPE": "Direct Bill", "PREVIOUS_DUE_DATE": "", "CPTD": "",
        "PTD": "27-01-2027", "C2P": "0", "MODEL_PRM": "18024.48", "AFYP": "18024.48",
        "TOTAL_SERV_TAX": "", "EMAIL_ID": "smrsrbh@gmail.com"
    },
    {
        "LIFE_ASSURED_NAME": "Prathamesh Mandar Lele", "POL_ID": "140695255", "POL_ISSUED": "17-02-2023",
        "PLAN_NAME": "Axis Max Life Smart Secure Plus Plan_Regular_Online", "POL_TYPE": "TRAD",
        "CEASE_REASON_CD": "R", "CEASE_REASON_DESC": "Automatic Cease Reason", "POLICY_STATUS": "Premium paying",
        "BILL_MODE": "Monthly", "BILL_TYPE": "ENACH", "PREVIOUS_DUE_DATE": "", "CPTD": "",
        "PTD": "17-03-2026", "C2P": "1154.35", "MODEL_PRM": "1154.35", "AFYP": "13852.2",
        "TOTAL_SERV_TAX": "", "EMAIL_ID": "prathameshlele7@gmail.com"
    },
    {
        "LIFE_ASSURED_NAME": "Namrata Gupta", "POL_ID": "140847153", "POL_ISSUED": "09-02-2023",
        "PLAN_NAME": "Axis Max Life Smart Secure Plus Plan_60 Pay_Online", "POL_TYPE": "TRAD",
        "CEASE_REASON_CD": "R", "CEASE_REASON_DESC": "Automatic Cease Reason", "POLICY_STATUS": "Premium paying",
        "BILL_MODE": "Annual", "BILL_TYPE": "Credit card", "PREVIOUS_DUE_DATE": "", "CPTD": "",
        "PTD": "09-02-2027", "C2P": "0", "MODEL_PRM": "29016.83", "AFYP": "29016.83",
        "TOTAL_SERV_TAX": "", "EMAIL_ID": "gupta.namrata8918@gmail.com"
    }
]

@app.post("/api/verify-golden")
async def verify_golden(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    
    try:
        content = await file.read()
        df = pd.read_csv(io.BytesIO(content)).convert_dtypes()
        df.columns = df.columns.str.strip()
        
        if df.empty:
            raise HTTPException(status_code=400, detail="CSV file is empty")
        
        # Helper to normalize values for comparison
        def normalize(val):
            if pd.isna(val) or str(val).strip() == "":
                return ""
            return str(val).strip().lower()

        results = []
        matched_count = 0
        
        for golden in GOLDEN_RECORDS:
            # Composite Key: Name, POL_ID, Email
            target_name = normalize(golden["LIFE_ASSURED_NAME"])
            target_id = normalize(golden["POL_ID"])
            target_email = normalize(golden["EMAIL_ID"])
            
            # Find in uploaded CSV
            match = df[
                (df["LIFE_ASSURED_NAME"].apply(normalize) == target_name) &
                (df["POL_ID"].astype(str).apply(normalize) == target_id) &
                (df["EMAIL_ID"].apply(normalize) == target_email)
            ]
            
            if not match.empty:
                csv_row = match.iloc[0].to_dict()
                comparison = {}
                is_perfect_match = True
                
                # Compare all fields in the Golden Record
                for key, expected_val in golden.items():
                    actual_val = csv_row.get(key, "")
                    if normalize(actual_val) != normalize(expected_val):
                        comparison[key] = {
                            "status": "mismatch",
                            "expected": expected_val,
                            "actual": str(actual_val) if not pd.isna(actual_val) else ""
                        }
                        is_perfect_match = False
                    else:
                        comparison[key] = {"status": "match"}
                
                results.append({
                    "primary_key": f"{golden['LIFE_ASSURED_NAME']} ({golden['POL_ID']})",
                    "found": True,
                    "is_valid": is_perfect_match,
                    "details": comparison
                })
                if is_perfect_match:
                    matched_count += 1
            else:
                results.append({
                    "primary_key": f"{golden['LIFE_ASSURED_NAME']} ({golden['POL_ID']})",
                    "found": False,
                    "is_valid": False,
                    "error": "Record not found in uploaded CSV"
                })

        return {
            "results": results, 
            "summary": f"{matched_count}/{len(GOLDEN_RECORDS)} Golden Records matched perfectly"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CSV: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
