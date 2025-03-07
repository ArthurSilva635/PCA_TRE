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
