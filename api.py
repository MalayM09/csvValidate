import os
import warnings
import pandas as pd
import io
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
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

# Golden Records Data organized by company
GOLDEN_DATA = {
    "max_life": {
        "keys": ["LIFE_ASSURED_NAME", "POL_ID", "EMAIL_ID"],
        "records": [
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
    },
    "tata": {
        "keys": ["policy_no", "Proposer_Name", "Email"],
        "records": [
            {
                "policy_no": "C296621620", "Sub_Status": "ISSUED (IN FORCE)", "Billing_Frequency": "Annual",
                "Next_Due_Date": "06/09/2026", "Proposer_Name": "SHAIK RAMEEJ RAJA", "Email": "rameej.iiit@gmail.com"
            },
            {
                "policy_no": "C197542675", "Sub_Status": "ISSUED (IN FORCE)", "Billing_Frequency": "Annual",
                "Next_Due_Date": "18/11/2026", "Proposer_Name": "ESWARA VENKATA KANAKA SWARNA T", "Email": "swarnatej.boddeda@gmail.com"
            },
            {
                "policy_no": "C580078387", "Sub_Status": "ISSUED (IN FORCE)", "Billing_Frequency": "Annual",
                "Next_Due_Date": "20/11/2026", "Proposer_Name": "YOGESWARA RAO GOLIVE", "Email": "yogesh419federer@gmail.com"
            },
            {
                "policy_no": "C121596888", "Sub_Status": "ISSUED (IN FORCE)", "Billing_Frequency": "Annual",
                "Next_Due_Date": "21/02/2027", "Proposer_Name": "Premkumar", "Email": "prem2600@gmail.com"
            },
            {
                "policy_no": "C244417624", "Sub_Status": "ISSUED (IN FORCE)", "Billing_Frequency": "Semi-Annual",
                "Next_Due_Date": "16/04/2026", "Proposer_Name": "SHRIDHAR CHAMARIA", "Email": "shridhar.chamaria@gmail.com"
            },
            {
                "policy_no": "C270243286", "Sub_Status": "ISSUED (IN FORCE)", "Billing_Frequency": "Monthly",
                "Next_Due_Date": "14/10/2025", "Proposer_Name": "Ashish Sachin Gondhale", "Email": "ashishgondhale123@gmail.com"
            }
        ]
    }
}

@app.post("/api/verify-golden")
async def verify_golden(
    file: UploadFile = File(...),
    company: str = Form(...)
):
    if company not in GOLDEN_DATA:
        raise HTTPException(status_code=400, detail=f"Company '{company}' not supported yet")
    
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    
    try:
        content = await file.read()
        # Robust CSV reading
        try:
            df = pd.read_csv(io.BytesIO(content), sep=None, engine='python').convert_dtypes()
        except:
            df = pd.read_csv(io.BytesIO(content)).convert_dtypes()
            
        df.columns = df.columns.str.strip()
        col_map = {c.lower(): c for c in df.columns}
        
        if df.empty:
            raise HTTPException(status_code=400, detail="CSV file is empty")
        
        company_config = GOLDEN_DATA[company]
        golden_records = company_config["records"]
        primary_keys = company_config["keys"]

        # Normalize function
        def normalize(val):
            if pd.isna(val) or str(val).strip() == "":
                return ""
            s = str(val).strip().lower()
            try:
                f = float(s)
                if f == int(f):
                    return str(int(f))
                return str(f)
            except (ValueError, TypeError):
                return s

        # Find actual column names in CSV
        csv_key_names = {}
        for k in primary_keys:
            mapped_col = col_map.get(k.lower())
            if not mapped_col:
                raise HTTPException(status_code=400, detail=f"Required column '{k}' missing in CSV")
            csv_key_names[k] = mapped_col

        results = []
        matched_count = 0
        
        for golden in golden_records:
            # Build filter for primary keys
            mask = pd.Series([True] * len(df))
            for k in primary_keys:
                target_val = normalize(golden[k])
                mask &= (df[csv_key_names[k]].astype(str).apply(normalize) == target_val)
            
            match = df[mask]
            
            if not match.empty:
                csv_row = match.iloc[0].to_dict()
                comparison = {}
                is_perfect_match = True
                
                # Compare all fields in the Golden Record
                for key, expected_val in golden.items():
                    csv_col = col_map.get(key.lower())
                    actual_val = csv_row.get(csv_col, "") if csv_col else ""
                    
                    if normalize(actual_val) != normalize(expected_val):
                        comparison[key] = {
                            "status": "mismatch",
                            "expected": expected_val,
                            "actual": str(actual_val) if not pd.isna(actual_val) else ""
                        }
                        is_perfect_match = False
                    else:
                        comparison[key] = {"status": "match"}
                
                display_id = golden.get("POL_ID") or golden.get("policy_no") or "Record"
                display_name = golden.get("LIFE_ASSURED_NAME") or golden.get("Proposer_Name") or ""
                
                results.append({
                    "primary_key": f"{display_name} ({display_id})",
                    "found": True,
                    "is_valid": is_perfect_match,
                    "details": comparison
                })
                if is_perfect_match:
                    matched_count += 1
            else:
                display_id = golden.get("POL_ID") or golden.get("policy_no") or "Record"
                display_name = golden.get("LIFE_ASSURED_NAME") or golden.get("Proposer_Name") or ""
                results.append({
                    "primary_key": f"{display_name} ({display_id})",
                    "found": False,
                    "is_valid": False,
                    "error": "Record not found in uploaded CSV"
                })

        return {
            "results": results, 
            "summary": f"{matched_count}/{len(golden_records)} Golden Records matched perfectly"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CSV: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
