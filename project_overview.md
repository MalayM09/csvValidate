# Google Sheet Entry Validator

## Overview
The **Google Sheet Entry Validator** is a high-performance Python tool designed to verify the completeness of policy data. It connects to a Google Sheet, searches for a specific entry based on a user-defined column (like `POL_ID` or `AFYP`), and checks if the required fields—`LIFE_ASSURED_NAME` and `EMAIL_ID`—are present and valid.

## Core Features
- **Dynamic Lookup**: Search entries using any column in the sheet.
- **Data Cleansing**: Automatically handles whitespace in headers and cell values.
- **Robust Validation**: Uses `pandas` to manage large datasets and handle missing values (`NA`) without errors.
- **Silent Mode**: Suppresses system and library warnings for a clean interface.
- **Schema Discovery**: Ability to see all columns and their inferred data types using the `--show_info` flag.

## Technical Requirements
- **Language**: Python 3.9+ 
- **Libraries**: `google-api-python-client`, `pandas`, `google-auth-oauthlib`.
- **Authentication**: Requires a `credentials.json` file from a Google Cloud Project with the Sheets API enabled.

## Data Structure Example
The validator expects a sheet containing (at minimum) these columns:
- `LIFE_ASSURED_NAME`
- `EMAIL_ID`
- `POL_ID` (or any other identifier like `AFYP`)

## Integration Points for UI Design

### 1. Inputs Needed
- **Sheet ID**: The unique identifier of the Google Sheet.
- **Lookup Column**: A dropdown or search field for the column to search in (e.g., `POL_ID`).
- **Target Value**: The specific value to look for (e.g., `32662.3`).

### 2. Logic Flow
1. **Fetch**: Connect to Google Sheets and pull the latest data.
2. **Standardize**: Strip whitespace from headers and values.
3. **Filter**: Locate the row(s) matching the Target Value in the Lookup Column.
4. **Validate**:
   - Check if `LIFE_ASSURED_NAME` is not empty.
   - Check if `EMAIL_ID` is not empty.
5. **Report**: Return a simple "Valid" or "Invalid" status with details.

### 3. Expected Outputs
- **Validation Status**: `SUCCESS` (Both present) or `FAILURE` (One/Both missing).
- **Details**:
  - `Name Status`: Present (Value) / Missing.
  - `Email Status`: Present (Value) / Missing.

## CLI Usage (Reference)
- **Standard Check**: `python validator.py --sheet_id [ID] --column_name "POL_ID" --column_value "123"`
- **Alternate Column**: `python validator.py --sheet_id [ID] --column_name "AFYP" --column_value "32662.3"`
- **Schema Info**: `python validator.py --sheet_id [ID] --show_info`
