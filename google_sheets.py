import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from config import json_path, scope, spreadsheet_name, worksheet_name


def authenticate_google_sheets():
    """Autentica na API do Google Sheets e retorna um cliente."""
    creds = Credentials.from_service_account_file(json_path, scopes=scope)
    client = gspread.authorize(creds)
    return client


def get_sheet_data():
    """Obtém os dados do Google Sheets e retorna um DataFrame."""
    client = authenticate_google_sheets()  # Aqui garantimos que o cliente é criado corretamente
    spreadsheet = client.open(spreadsheet_name)
    sheet = spreadsheet.worksheet(worksheet_name)
    
    rows = sheet.get_all_values()
    headers = rows[6]  # Linha 7 contém os cabeçalhos
    data = rows[7:]
    
    df = pd.DataFrame(data, columns=headers)
    return df
