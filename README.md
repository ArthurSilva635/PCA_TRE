# 🚀 Projeto PCA - Pipeline de Integração com Google Sheets e PostgreSQL

Este projeto automatiza a extração de dados do **Google Sheets**, faz o tratamento necessário e os armazena em um banco **PostgreSQL**.


### 1. Clonar o repositório

Abra o terminal e clone o repositório:

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

## 📌 **1. Pré-requisitos**

## Passos para configurar o ambiente
Antes de rodar o projeto, instale os pacotes necessários. Para isso, execute:

```bash
pip install -r requirements.txt
```

Se precisar gerar automaticamente um `requirements.txt`, utilize:

```bash
pip freeze > requirements.txt
```

Ou, para capturar apenas as bibliotecas realmente usadas no código:

```bash
pip install pipreqs
pipreqs . --force
```

---

## 📂 **2. Estrutura do Projeto**

```
/pcav10
│── /config.py         # Configurações gerais do projeto
│── /google_sheets.py  # Código para obter dados do Google Sheets
│── /database.py       # Código para salvar dados no PostgreSQL
│── /utils.py          # Funções auxiliares (como renomeação de colunas)
│── /main.py           # Arquivo principal que executa o pipeline
│── requirements.txt   # Lista de dependências do projeto
│── README.md          # Documentação do projeto
```

---

## 🔧 **3. Configuração do Google Sheets**

Antes de rodar o código, configure o arquivo `config.py` com suas credenciais:

```python
import gspread
from google.oauth2.service_account import Credentials

# Caminho para o JSON de credenciais
json_path = "pca-sheets-e3ca5d4ee085.json"

# Definição dos escopos necessários
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Autenticação com Google Sheets
creds = Credentials.from_service_account_file(json_path, scopes=scope)
client = gspread.authorize(creds)

# Nome da planilha e aba
spreadsheet_name = "CÓPIA PARA EQUIPE BI - PCA 2025 - Versão 1.0"
worksheet_name = "PCA 2025"
```

---

## 📊 **4. Extração de Dados do Google Sheets**

Arquivo: **`google_sheets.py`**

```python
import gspread
import pandas as pd
from config import client, spreadsheet_name, worksheet_name

def get_sheet_data():
    """ Obtém os dados da planilha do Google Sheets e retorna um DataFrame. """
    spreadsheet = client.open(spreadsheet_name)
    sheet = spreadsheet.worksheet(worksheet_name)

    rows = sheet.get_all_values()
    headers = rows[6]  # A linha 7 contém os cabeçalhos
    data = rows[7:]  # Dados a partir da linha 8

    df = pd.DataFrame(data, columns=headers)
    return df
```

---

## 🛠 **5. Tratamento e Renomeação de Colunas**

Arquivo: **`utils.py`**

```python
import re

def clean_column_names(df):
    """Converte os nomes das colunas para snake_case e remove espaços/hífens."""
    df.columns = [col.strip() if col.strip() else f"col_{i}" for i, col in enumerate(df.columns)]
    df.columns = [col.lower().replace(" ", "_").replace("-", "_") for col in df.columns]
    return df
```

---

## 🗄 **6. Salvando Dados no Banco de Dados PostgreSQL**

Arquivo: **`database.py`**

```python
from sqlalchemy import create_engine
from config import db_url

def save_to_db(df, table_name="PCA"):
    """Salva o DataFrame no banco de dados PostgreSQL."""
    engine = create_engine(db_url)
    df.to_sql(table_name, engine, if_exists="replace", index=False)
```

---

## 🚀 **7. Executando o Pipeline**

Arquivo: **`main.py`**

```python
from google_sheets import get_sheet_data
from utils import clean_column_names
from database import save_to_db

def main():
    print("Obtendo dados do Google Sheets...")
    df = get_sheet_data()

    print("Formatando nomes das colunas...")
    df = clean_column_names(df)

    print("Salvando dados no banco de dados...")
    save_to_db(df)

if __name__ == "__main__":
    main()
```

---

## ▶ **8. Rodando o Projeto**

Para executar o pipeline, use:

```bash
python main.py
```

