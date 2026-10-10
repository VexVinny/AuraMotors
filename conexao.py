import pyodbc

def abrir_conexao():
    dados_conexao = (
        "Driver={PostgreSQL Unicode(x64)};"
        "Server=localhost;"
        "Port=5432;"
        "Database=postgres;"
        "UID=postgres;"      
        "1234;"
    )
    return pyodbc.connect(dados_conexao)
print("Programa executado!")