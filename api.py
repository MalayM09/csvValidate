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
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
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
    },
    "hdfc": {
        "keys": ["Policy No", "Life Assured Name", "Email ID"],
        "records": [
            {
                "SRC": "MUM_LA", "Login Date": "30/05/2023", "Application No": "1200082883656", "Policy No": "26124036", "Proposal Date": "24/05/2023", "Proposal Receive Date": "25/05/2023", "First Receipt Date": "24/05/2023", "Original Commensement Date": "30/05/2023", "Conversion Date": "30/05/2023", "Premium Due Date": "30/05/2026", "Lapsed Date": "-", "Maturity Date": "30/05/2055", "Grace Period Ends": "29/06/2026", "Product Name": "HDFC Life Click2 Protect Life", "Policy Term": "32", "Premium Paying Term": "32", "Premium Amount": "24,710", "PREMIUM_AMT_WITH_TAX": "24710", "COMBI_PREMIUM_AMT": "0", "COMBI_PREMIUM_AMT_WITH_TAX": "29158", "EXTERNAL_OPTION": "-", "Sum Assured": "17000000", "Policy Status": "In Force", "Reason Desc": "-", "Withdrawn Reason": "-", "Premium Paying Mode": "01", "Renewal Collection Method": "Credit Card", "SI Flag": "AutoDebit on Card", "Policy Flag": "POLICY", "Client Name": "Venugopal Kusumanchi", "Life Assured Name": "Venugopal Kusumanchi", "Email ID": "venugopalkusumanchi@gmail.com"
            },
            {
                "SRC": "MUM_LA", "Login Date": "02/09/2021", "Application No": "1270068970096", "Policy No": "24035781", "Proposal Date": "31/07/2021", "Proposal Receive Date": "31/07/2021", "First Receipt Date": "31/07/2021", "Original Commensement Date": "09/09/2021", "Conversion Date": "09/09/2021", "Premium Due Date": "09/09/2026", "Lapsed Date": "-", "Maturity Date": "09/09/2070", "Grace Period Ends": "09/10/2026", "Product Name": "HDFC Life Click2 Protect Life", "Policy Term": "49", "Premium Paying Term": "34", "Premium Amount": "23,653", "PREMIUM_AMT_WITH_TAX": "23653", "COMBI_PREMIUM_AMT": "0", "COMBI_PREMIUM_AMT_WITH_TAX": "27850", "EXTERNAL_OPTION": "-", "Sum Assured": "24000000", "Policy Status": "In Force", "Reason Desc": "-", "Withdrawn Reason": "-", "Premium Paying Mode": "01", "Renewal Collection Method": "Cash / Cheques", "SI Flag": "Non AutoDebit", "Policy Flag": "POLICY", "Client Name": "Sumukh Samant", "Life Assured Name": "Sumukh Samant", "Email ID": "sumukh.samant@gmail.com"
            },
            {
                "SRC": "MUM_LA", "Login Date": "02/11/2022", "Application No": "1271000029712", "Policy No": "25378637", "Proposal Date": "26/10/2022", "Proposal Receive Date": "26/10/2022", "First Receipt Date": "25/10/2022", "Original Commensement Date": "08/11/2022", "Conversion Date": "08/11/2022", "Premium Due Date": "08/11/2026", "Lapsed Date": "-", "Maturity Date": "08/11/2069", "Grace Period Ends": "08/12/2026", "Product Name": "HDFC Life Click2 Protect Life", "Policy Term": "47", "Premium Paying Term": "15", "Premium Amount": "43,337", "PREMIUM_AMT_WITH_TAX": "43337", "COMBI_PREMIUM_AMT": "0", "COMBI_PREMIUM_AMT_WITH_TAX": "51138", "EXTERNAL_OPTION": "-", "Sum Assured": "20000000", "Policy Status": "In Force", "Reason Desc": "-", "Withdrawn Reason": "-", "Premium Paying Mode": "01", "Renewal Collection Method": "Direct Debit", "SI Flag": "AutoDebit on Bank", "Policy Flag": "POLICY", "Client Name": "Rohini Bahuguna", "Life Assured Name": "Rohini Bahuguna", "Email ID": "rbahuguna3@gmail.com"
            },
            {
                "SRC": "MUM_LA", "Login Date": "21/03/2023", "Application No": "1271000032414", "Policy No": "25832327", "Proposal Date": "04/03/2023", "Proposal Receive Date": "04/03/2023", "First Receipt Date": "04/03/2023", "Original Commensement Date": "09/03/2023", "Conversion Date": "21/03/2023", "Premium Due Date": "09/03/2027", "Lapsed Date": "-", "Maturity Date": "09/03/2052", "Grace Period Ends": "08/04/2027", "Product Name": "HDFC Life Click2 Protect Life", "Policy Term": "29", "Premium Paying Term": "10", "Premium Amount": "48,404", "PREMIUM_AMT_WITH_TAX": "48404", "COMBI_PREMIUM_AMT": "0", "COMBI_PREMIUM_AMT_WITH_TAX": "57117", "EXTERNAL_OPTION": "-", "Sum Assured": "35000000", "Policy Status": "In Force", "Reason Desc": "-", "Withdrawn Reason": "-", "Premium Paying Mode": "01", "Renewal Collection Method": "Cash / Cheques", "SI Flag": "Non AutoDebit", "Policy Flag": "POLICY", "Client Name": "Ayush Yadav", "Life Assured Name": "Ayush Yadav", "Email ID": "ayushyadav1003@gmail.com"
            },
            {
                "SRC": "MUM_LA", "Login Date": "13/05/2023", "Application No": "1271000032642", "Policy No": "25935827", "Proposal Date": "26/03/2023", "Proposal Receive Date": "26/03/2023", "First Receipt Date": "26/03/2023", "Original Commensement Date": "26/03/2023", "Conversion Date": "13/05/2023", "Premium Due Date": "26/03/2026", "Lapsed Date": "-", "Maturity Date": "26/03/2049", "Grace Period Ends": "25/04/2026", "Product Name": "HDFC Life Click2 Protect Life", "Policy Term": "26", "Premium Paying Term": "26", "Premium Amount": "24,898", "PREMIUM_AMT_WITH_TAX": "24898", "COMBI_PREMIUM_AMT": "0", "COMBI_PREMIUM_AMT_WITH_TAX": "29380", "EXTERNAL_OPTION": "-", "Sum Assured": "20000000", "Policy Status": "In Force", "Reason Desc": "-", "Withdrawn Reason": "-", "Premium Paying Mode": "01", "Renewal Collection Method": "Cash / Cheques", "SI Flag": "Non AutoDebit", "Policy Flag": "POLICY", "Client Name": "Lebin Sebastian Francisbaby", "Life Assured Name": "Lebin Sebastian Francisbaby", "Email ID": "libinenjoy@gmail.com"
            },
            {
                "SRC": "MUM_LA", "Login Date": "25/04/2023", "Application No": "1271000032864", "Policy No": "26013114", "Proposal Date": "10/04/2023", "Proposal Receive Date": "10/04/2023", "First Receipt Date": "10/04/2023", "Original Commensement Date": "27/04/2023", "Conversion Date": "27/04/2023", "Premium Due Date": "27/04/2026", "Lapsed Date": "-", "Maturity Date": "27/04/2063", "Grace Period Ends": "27/05/2026", "Product Name": "HDFC Life Click2 Protect Life", "Policy Term": "40", "Premium Paying Term": "40", "Premium Amount": "39,975", "PREMIUM_AMT_WITH_TAX": "39975", "COMBI_PREMIUM_AMT": "0", "COMBI_PREMIUM_AMT_WITH_TAX": "47171", "EXTERNAL_OPTION": "-", "Sum Assured": "25000000", "Policy Status": "In Force", "Reason Desc": "-", "Withdrawn Reason": "-", "Premium Paying Mode": "01", "Renewal Collection Method": "Cash / Cheques", "SI Flag": "Non AutoDebit", "Policy Flag": "POLICY", "Client Name": "Harshit Singhal", "Life Assured Name": "Harshit Singhal", "Email ID": "singhal.harshit.1411@gmail.com"
            },
            {
                "SRC": "MUM_LA", "Login Date": "05/05/2023", "Application No": "1271000033137", "Policy No": "26053719", "Proposal Date": "27/04/2023", "Proposal Receive Date": "27/04/2023", "First Receipt Date": "27/04/2023", "Original Commensement Date": "05/05/2023", "Conversion Date": "05/05/2023", "Premium Due Date": "05/05/2026", "Lapsed Date": "-", "Maturity Date": "05/05/2053", "Grace Period Ends": "04/06/2026", "Product Name": "HDFC Life Click2 Protect Life", "Policy Term": "30", "Premium Paying Term": "30", "Premium Amount": "30,348", "PREMIUM_AMT_WITH_TAX": "30348", "COMBI_PREMIUM_AMT": "0", "COMBI_PREMIUM_AMT_WITH_TAX": "35811", "EXTERNAL_OPTION": "-", "Sum Assured": "32000000", "Policy Status": "In Force", "Reason Desc": "-", "Withdrawn Reason": "-", "Premium Paying Mode": "01", "Renewal Collection Method": "Cash / Cheques", "SI Flag": "Non AutoDebit", "Policy Flag": "POLICY", "Client Name": "Saravanan I", "Life Assured Name": "Saravanan I", "Email ID": "saravanancse13@gmail.com"
            }
        ]
    },
    "bajaj": {
        "keys": ["Policy Number", "Name", "Email"],
        "records": [
            {
                "Policy Number": "625315564", "Name": "TAKKILGE DATTATRI", "BOOKING_FREQUENCY": "1", "Benefit Term": "40", "Premium Term": "15", "Full Term Premium": "14746.83", "Annulized": "14746.83", "Agent Code": "2000050532", "Package Code": "LIFE_SHEILD_NEW", "CHANGE_DESCRIPTION": "ISSUED", "Term Start Date": "15/05/2025", "PAYMENT_DUE_DATE": "15/05/2026", "Appln No": "6136735274", "Renewal Mode": "NACH", "Pay Mode": "UPI", "Email": "dattatri.7585@gmail.com"
            },
            {
                "Policy Number": "603619411", "Name": "RAJAN V", "BOOKING_FREQUENCY": "1", "Benefit Term": "35", "Premium Term": "10", "Full Term Premium": "36909", "Annulized": "36909", "Agent Code": "2000050532", "Package Code": "LIFE_SHEILD_NEW", "CHANGE_DESCRIPTION": "ISSUED", "Term Start Date": "21/08/2024", "PAYMENT_DUE_DATE": "21/08/2026", "Appln No": "6135019604", "Renewal Mode": "NACH", "Pay Mode": "DCOL", "Email": "vrajan1988@gmail.com"
            },
            {
                "Policy Number": "622472245", "Name": "GANESH CHINNI", "BOOKING_FREQUENCY": "12", "Benefit Term": "39", "Premium Term": "10", "Full Term Premium": "4877", "Annulized": "58524", "Agent Code": "2000050532", "Package Code": "LIFE_SHEILD_NEW", "CHANGE_DESCRIPTION": "ISSUED", "Term Start Date": "11/04/2025", "PAYMENT_DUE_DATE": "11/03/2026", "Appln No": "6136537610", "Renewal Mode": "UPI_M", "Pay Mode": "UPI", "Email": "chinnig6@gmail.com"
            },
            {
                "Policy Number": "612839938", "Name": "NARAYANARAOPET SOWMYA", "BOOKING_FREQUENCY": "12", "Benefit Term": "50", "Premium Term": "20", "Full Term Premium": "2320", "Annulized": "27840", "Agent Code": "2000050532", "Package Code": "LIFE_SHEILD_PLUS_NEW", "CHANGE_DESCRIPTION": "ISSUED", "Term Start Date": "23/12/2024", "PAYMENT_DUE_DATE": "23/03/2026", "Appln No": "6135850483", "Renewal Mode": "NACH", "Pay Mode": "UPI", "Email": "narayanraopet.sowmya@gmail.com"
            },
            {
                "Policy Number": "636456186", "Name": "SURJEET RAWAT", "BOOKING_FREQUENCY": "1", "Benefit Term": "24", "Premium Term": "24", "Full Term Premium": "11655", "Annulized": "11655", "Agent Code": "2000050532", "Package Code": "LIFE_SHEILD_NEW", "CHANGE_DESCRIPTION": "ISSUED", "Term Start Date": "18/08/2025", "PAYMENT_DUE_DATE": "18/08/2026", "Appln No": "6166176514", "Renewal Mode": "NACH", "Pay Mode": "UPI", "Email": "jeetrawat5@gmail.com"
            },
            {
                "Policy Number": "634209876", "Name": "ABHILASH SATHIAN", "BOOKING_FREQUENCY": "12", "Benefit Term": "30", "Premium Term": "30", "Full Term Premium": "2146", "Annulized": "25752", "Agent Code": "2000050532", "Package Code": "LIFE_SHEILD_NEW", "CHANGE_DESCRIPTION": "ISSUED", "Term Start Date": "26/07/2025", "PAYMENT_DUE_DATE": "26/03/2026", "Appln No": "6137263179", "Renewal Mode": "NACH", "Pay Mode": "UPI", "Email": "abhilash_2011@yahoo.com"
            }
        ]
    },
    "icici": {
        "keys": ["Policy Number", "Life Assured First Name", "Life Assured Last Name", "Customer Email Id"],
        "records": [
            {
                "Policy Number": "K8573239", "Application Number": "OB31030264", "Policy Name": "IPRU iProtect Smart Plus RP/LP", "Policy Status": "In Force", "Proposal Received Date": "29-01-2026", "Issuance Date": "15-02-2026", "First Issuance Date": "2026-02-15", "Risk Commencement Date": "15-02-2026", "Sum Assured": "2.00E+07", "Premium Installment": "40352", "Payment Frequency": "Yearly", "Policy Term": "23", "Premium Paying Term": "23", "Annual Premium": "40352", "Owner/Proposer Name": "A S SHANKARANARAYANAN", "Address": "HOUSE NO 7 RAM AVENUE OPPOSITE NEW AMRITSAR 143001", "City": "AMRITSAR", "State": "Punjab", "Phone1": "", "Phone2": "", "Mobile Phone Number": "9870318482", "Customer Email Id": "shankar3888@gmail.com", "Date of Birth": "1988-08-03", "Proposer date of birth": "1988-08-03", "Next Premium Due Date": "15-02-2027", "Premium Pay Status": "PP", "Maturity Date": "15-02-2049", "Maturity Date Month": "February", "Maturity Date Year": "10-08-1905", "Upsell Propensity": "", "Product to Upsell": "", "Upsell Product Name": "", "Total Fund Value": "", "Customer Consent": "N", "Nav Date": "", "Life Assured First Name": "A S", "Life Assured Last Name": "SHANKARANARAYANAN", "Address Status": "Resident Indian", "Pasa value": "40352", "PAN Status": "", "Identity Status": "", "Bounced Date": "", "Bounced Reason": "", "MWPA tagging": "N", "Total premium paid": "40352", "Payment Mode": "Cash / Cheque", "Suspense Amount": "0"
            },
            {
                "Policy Number": "B6260248", "Application Number": "OB18533796", "Policy Name": "ICICI Pru iProtect Smart", "Policy Status": "Contract Withdrawn", "Proposal Received Date": "05-02-2022", "Issuance Date": "", "First Issuance Date": "", "Risk Commencement Date": "5-2-2022", "Sum Assured": "2.00E+07", "Premium Installment": "38840", "Payment Frequency": "Yearly", "Policy Term": "28", "Premium Paying Term": "23", "Annual Premium": "38840", "Owner/Proposer Name": "AADARSH BALAKRISHNA", "Address": "D4 6 Guruganesh Nagar part 1 near Ashish garden kothrud 411038", "City": "Pune", "State": "Maharashtra", "Phone1": "", "Phone2": "", "Mobile Phone Number": "9849092208", "Customer Email Id": "andycrik@yahoo.com", "Date of Birth": "1984-02-10", "Proposer date of birth": "1984-02-10", "Next Premium Due Date": "", "Premium Pay Status": "PS", "Maturity Date": "05-02-2050", "Maturity Date Month": "February", "Maturity Date Year": "11-8-1905", "Upsell Propensity": "", "Product to Upsell": "", "Upsell Product Name": "", "Total Fund Value": "", "Customer Consent": "N", "Nav Date": "", "Life Assured First Name": "AADARSH", "Life Assured Last Name": "BALAKRISHNA", "Address Status": "Resident Indian", "Pasa value": "38840", "PAN Status": "", "Identity Status": "", "Bounced Date": "", "Bounced Reason": "", "MWPA tagging": "N", "Total premium paid": "", "Payment Mode": "Cash / Cheque", "Suspense Amount": ""
            },
            {
                "Policy Number": "K3770046", "Application Number": "OB26914022", "Policy Name": "ICICI Pru iProtect Smart", "Policy Status": "In Force", "Proposal Received Date": "27-12-2024", "Issuance Date": "04-01-2025", "First Issuance Date": "2025-01-04", "Risk Commencement Date": "4-1-2025", "Sum Assured": "1.00E+07", "Premium Installment": "11912", "Payment Frequency": "Yearly", "Policy Term": "34", "Premium Paying Term": "34", "Annual Premium": "11912", "Owner/Proposer Name": "AAKASH PARESH GODSE", "Address": "2501 25th Floor Oceania BWing 400037", "City": "Mumbai", "State": "Maharashtra", "Phone1": "", "Phone2": "", "Mobile Phone Number": "7020425612", "Customer Email Id": "godseaakash7875@gmail.com", "Date of Birth": "1998-08-30", "Proposer date of birth": "1998-08-30", "Next Premium Due Date": "04-01-2027", "Premium Pay Status": "PP", "Maturity Date": "04-01-2059", "Maturity Date Month": "January", "Maturity Date Year": "20-8-1905", "Upsell Propensity": "", "Product to Upsell": "", "Upsell Product Name": "", "Total Fund Value": "", "Customer Consent": "N", "Nav Date": "", "Life Assured First Name": "AAKASH PARESH", "Life Assured Last Name": "GODSE", "Address Status": "Resident Indian", "Pasa value": "11912", "PAN Status": "", "Identity Status": "", "Bounced Date": "", "Bounced Reason": "", "MWPA tagging": "N", "Total premium paid": "22879", "Payment Mode": "ECS/SI", "Suspense Amount": "0"
            },
            {
                "Policy Number": "K2496435", "Application Number": "OB26562159", "Policy Name": "ICICI Pru iProtect Smart", "Policy Status": "In Force", "Proposal Received Date": "22-11-2024", "Issuance Date": "21-12-2024", "First Issuance Date": "2024-12-21", "Risk Commencement Date": "1-12-2024", "Sum Assured": "2.00E+07", "Premium Installment": "33771", "Payment Frequency": "Yearly", "Policy Term": "54", "Premium Paying Term": "54", "Annual Premium": "33771", "Owner/Proposer Name": "AAYUSH JAIN", "Address": "In front of house number 55 Suncity colony 471001", "City": "Chhatarpur", "State": "Madhya Pradesh", "Phone1": "", "Phone2": "", "Mobile Phone Number": "8011202941", "Customer Email Id": "aayushjain.jain28@gmail.com", "Date of Birth": "1992-12-02", "Proposer date of birth": "1992-12-02", "Next Premium Due Date": "1-12-2026", "Premium Pay Status": "PP", "Maturity Date": "01-12-2078", "Maturity Date Month": "December", "Maturity Date Year": "8-9-1905", "Upsell Propensity": "", "Product to Upsell": "", "Upsell Product Name": "", "Total Fund Value": "", "Customer Consent": "N", "Nav Date": "", "Life Assured First Name": "AAYUSH", "Life Assured Last Name": "JAIN", "Address Status": "Resident Indian", "Pasa value": "33771", "PAN Status": "", "Identity Status": "", "Bounced Date": "", "Bounced Reason": "", "MWPA tagging": "N", "Total premium paid": "64165", "Payment Mode": "ECS/SI", "Suspense Amount": "0"
            },
            {
                "Policy Number": "D0757457", "Application Number": "OB19445358", "Policy Name": "ICICI Pru iProtect Smart", "Policy Status": "In Force", "Proposal Received Date": "23-7-2022", "Issuance Date": "27-8-2022", "First Issuance Date": "2022-08-27", "Risk Commencement Date": "27-8-2022", "Sum Assured": "6.00E+07", "Premium Installment": "60619", "Payment Frequency": "Yearly", "Policy Term": "34", "Premium Paying Term": "34", "Annual Premium": "60619", "Owner/Proposer Name": "ABHIK PATEL", "Address": "B81 MJR Platina Hosur Road 560068", "City": "Bangalore", "State": "Karnataka", "Phone1": "", "Phone2": "", "Mobile Phone Number": "8380823823", "Customer Email Id": "abhikpatel326@gmail.com", "Date of Birth": "1991-01-23", "Proposer date of birth": "1991-01-23", "Next Premium Due Date": "27-8-2026", "Premium Pay Status": "PP", "Maturity Date": "27-08-2056", "Maturity Date Month": "August", "Maturity Date Year": "17-8-1905", "Upsell Propensity": "", "Product to Upsell": "", "Upsell Product Name": "", "Total Fund Value": "", "Customer Consent": "N", "Nav Date": "", "Life Assured First Name": "ABHIK", "Life Assured Last Name": "PATEL", "Address Status": "Resident Indian", "Pasa value": "60619", "PAN Status": "", "Identity Status": "", "Bounced Date": "", "Bounced Reason": "", "MWPA tagging": "N", "Total premium paid": "242476", "Payment Mode": "Cash / Cheque", "Suspense Amount": "0"
            },
            {
                "Policy Number": "A7435831", "Application Number": "OB17984755", "Policy Name": "ICICI Pru iProtect Smart", "Policy Status": "In Force", "Proposal Received Date": "30-10-2021", "Issuance Date": "03-11-2021", "First Issuance Date": "2021-11-03", "Risk Commencement Date": "03-11-2021", "Sum Assured": "2.00E+07", "Premium Installment": "51504", "Payment Frequency": "Yearly", "Policy Term": "40", "Premium Paying Term": "10", "Annual Premium": "51504", "Owner/Proposer Name": "ABHILASH SANNE", "Address": "Flat 301 S R Sahasra 8th cross Kaggadaspura Main 560075", "City": "Bengaluru", "State": "Karnataka", "Phone1": "", "Phone2": "", "Mobile Phone Number": "9912085300", "Customer Email Id": "sanne.abhi@gmail.com", "Date of Birth": "1991-04-06", "Proposer date of birth": "1991-04-06", "Next Premium Due Date": "03-11-2026", "Premium Pay Status": "PP", "Maturity Date": "03-11-2061", "Maturity Date Month": "November", "Maturity Date Year": "22-08-1905", "Upsell Propensity": "", "Product to Upsell": "", "Upsell Product Name": "", "Total Fund Value": "", "Customer Consent": "N", "Nav Date": "", "Life Assured First Name": "ABHILASH", "Life Assured Last Name": "SANNE", "Address Status": "Resident Indian", "Pasa value": "51504", "PAN Status": "", "Identity Status": "", "Bounced Date": "", "Bounced Reason": "", "MWPA tagging": "N", "Total premium paid": "206016", "Payment Mode": "Cash / Cheque", "Suspense Amount": "0"
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
            # Strip, lowercase, and collapse multiple spaces
            s = " ".join(str(val).strip().lower().split())
            try:
                # Handle numeric values (e.g., 0 vs 0.0)
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
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
