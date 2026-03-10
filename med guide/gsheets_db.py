import gspread
import streamlit as st

# 1. Connect to Google Sheets using your JSON key
def get_google_sheet():
    try:
        # This looks for the credentials.json file in your folder
        gc = gspread.service_account(filename='credentials.json')
        # Open the specific spreadsheet by its name
        sh = gc.open("ElderCare_DB")
        return sh
    except Exception as e:
        st.error(f"Failed to connect to Google Sheets: {e}")
        return None

# 2. Function to fetch user login data
def get_users():
    sh = get_google_sheet()
    if sh:
        worksheet = sh.worksheet("Users")
        # Returns a list of dictionaries, e.g., [{'username': 'patient1', 'password': '123', 'role': 'Patient'}]
        return worksheet.get_all_records()
    return []

# 3. Function to fetch patient data
def get_patient_data(username):
    sh = get_google_sheet()
    if sh:
        worksheet = sh.worksheet("Patients")
        records = worksheet.get_all_records()
        # Find the specific patient
        for record in records:
            if record['username'] == username:
                return record
    return None

# 4. Function to update a missed pill counter
def update_missed_pills(username, new_count):
    sh = get_google_sheet()
    if sh:
        worksheet = sh.worksheet("Patients")
        # Find the cell containing the user and update the count next to it
        cell = worksheet.find(username)
        if cell:
            # Assuming 'missed_count' is in the column right next to the username
            worksheet.update_cell(cell.row, cell.col + 1, new_count)