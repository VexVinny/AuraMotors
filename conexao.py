import pyodbc

def abrir_conexao():
    dados_conexao = (
        "Driver={PostgreSQL Unicode(x64)};"
        "Server=localhost;"
        "Port=5432;"
        "Database=postgres;"
        "UID=postgres;"      
        "PWD=q1p0Q!P);"      
    )
    return pyodbc.connect(dados_conexao)
