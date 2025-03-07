import re


def to_snake_case(string):
    """Converte strings para snake_case."""
    string = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", string)
    return string.lower()


def to_camel_case(string):
    """Converte strings para camelCase."""
    words = string.split("_")
    return words[0].lower() + "".join(word.capitalize() for word in words[1:])


def format_column_names(df):
    """Converte os nomes das colunas para snake_case."""
    df.columns = [to_snake_case(col) for col in df.columns]
    return df


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