from sqlalchemy import create_engine
import pandas as pd
from config import db_url, PCA_DB
from utils import clean_column_names

def connect_db():
    """Cria uma conexão com o banco de dados."""
    engine = create_engine(db_url)
    return engine

def save_to_db(df):
    """Salva o DataFrame no banco de dados."""
    engine = connect_db()
    
    # Limpar nomes das colunas antes de salvar
    df = clean_column_names(df)

    df.to_sql(PCA_DB, engine, if_exists="replace", index=False)
    print(f"Dados inseridos na tabela {PCA_DB}")


