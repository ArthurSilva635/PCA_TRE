from google_sheets import get_sheet_data
from database import save_to_db
from utils import format_column_names

def main():
    print("Obtendo dados do Google Sheets...")
    df = get_sheet_data()

    print("Formatando nomes das colunas...")
    df = format_column_names(df)

    print("Salvando dados no banco de dados...")
    save_to_db(df)

    print("Processo concluído!")

if __name__ == "__main__":
    main()
