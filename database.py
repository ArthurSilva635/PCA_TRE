from sqlalchemy import create_engine, text
from sqlalchemy.engine.url import URL
from sqlalchemy.engine import Engine
import pandas as pd
import psycopg2
from config import db_url, db_url2, DL1_DB, DL1_SCHEMA, DL1_USER, DL1_PASSWORD, DL1_IP, DL1_PORT, DL1_TABLE
from utils import clean_column_names


def connect_db():
    """Cria uma conexão com o banco de dados."""
    
   # Conecte-se ao banco postgres padrão
    engine = create_engine(db_url, isolation_level="AUTOCOMMIT")

    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1 FROM pg_database WHERE datname = 'bisaof'"))
        if not result.scalar():
            conn.execute(text("CREATE DATABASE bisaof"))
    
    # Construir explicitamente a URL do banco 'bisaof'
    bisaof_db_url = URL.create(
        drivername="postgresql",
        username="bisaof",  # Defina o usuário correto
        password="bisaof!trern",    # Defina a senha correta
        host="192.168.107.251",
        port=54321,
        database="bisaof"
    )

    # Criar engine para conectar ao banco 'bisaof'
    engine = create_engine(str(bisaof_db_url))
    
    with engine.connect() as conn:
        # Cria o schema se não existir
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS pca_schema"))
        conn.commit()
    
    return engine

def save_to_db(df):
    """Salva o DataFrame no banco de dados."""
    engine = connect_db()
    
    # Limpar nomes das colunas antes de salvar
    df = clean_column_names(df)

     # Salvar os dados na tabela do banco de dados, dentro do schema específico
    df.to_sql(DL1_TABLE, engine, schema="pca_schema", if_exists="replace", index=False)
    
    print(f"Dados inseridos na tabela {DL1_TABLE} no schema 'pca_schema'")


