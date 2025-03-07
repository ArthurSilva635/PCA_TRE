from sqlalchemy import create_engine
import pandas as pd
from config import db_url, PCA_DB


def connect_db():
    """Cria uma conexão com o banco de dados."""
    engine = create_engine(db_url)
    return engine

def clean_column_names(df):
    """Remove espaços extras, renomeia colunas duplicadas e substitui colunas sem nome."""

    df.columns = [col.strip() if col.strip() else f"col_{i}" for i, col in enumerate(df.columns)]

     # Substituir espaços e traços por underscore
    df.columns = [col.lower().replace(" ", "_").replace("-", "_") for col in df.columns]

    # Renomear colunas específicas
    df.rename(columns={"col_39": "impácto"}, inplace=True)

    # Criar um dicionário para contar ocorrências de nomes de colunas
    col_count = {}
    new_columns = []
    for col in df.columns:
        if col in col_count:
            col_count[col] += 1
            new_columns.append(f"{col}_{col_count[col]}")  # Adiciona um sufixo numérico
        else:
            col_count[col] = 1
            new_columns.append(col)

    df.columns = new_columns
    return df


def save_to_db(df):
    """Salva o DataFrame no banco de dados."""
    engine = connect_db()
    
    # Limpar nomes das colunas antes de salvar
    df = clean_column_names(df)

    df.to_sql(PCA_DB, engine, if_exists="replace", index=False)
    print(f"Dados inseridos na tabela {PCA_DB}")


