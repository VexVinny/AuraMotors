import pyodbc

def abrir_conexao():
    try:
        dados_conexao = (
            "Driver={PostgreSQL Unicode(x64)};"
            "Server=localhost;"
            "Port=5432;"
            "Database=postgres;"
            "UID=postgres;"
            "PWD={q1p0Q!P)};"
        )
        return pyodbc.connect(dados_conexao)
    except Exception as e:
        print(f"Erro na conexão com o banco: {e}")
        return None