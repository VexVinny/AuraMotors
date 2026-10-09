import pyodbc
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from conexao import abrir_conexao

def listar_clientes():
    conexao = abrir_conexao()
    if not conexao: return

    try:
        cursor = conexao.cursor()
        query = 'SELECT * FROM "Aura Motors".vw_04_clientes_e_vendas;'
        cursor.execute(query)
        
        colunas = [column[0] for column in cursor.description]
        resultados = cursor.fetchall()

        print("\n--- RELATÓRIO DE CLIENTES E COMPRAS ---")
        print(" | ".join(colunas))
        print("-" * 70)
        
        for linha in resultados:
            print(" | ".join(str(valor) if valor is not None else "Sem compras" for valor in linha))
    except Exception as erro:
        print(f"Erro ao listar clientes: {erro}")
    finally:
        cursor.close()
        conexao.close()
        
        
def adicionar_cliente(nome, email, cpf, telefone):
    conexao = abrir_conexao()
    if not conexao:
        return 
    
    try:
        cursor = conexao.cursor()
        query = "INSERT INTO clientes (nome, email, cpf, telefone) VALUES (?, ?, ?, ?)"
        cursor.execute(query, (nome, email, cpf, telefone))
        conexao.commit()
        print(f"\nCliente '{nome}' inserido com sucesso!")
    except Exception as erro:
        print(f"\nErro ao inserir cliente: {erro}")
        conexao.rollback()
    finally:
        cursor.close()
        conexao.close()
        
        
def remover_cliente(cpf):
    conexao = abrir_conexao()
    if not conexao:
        return
    
    try:
        cursor = conexao.cursor()
        cursor.execute('SELECT nome FROM "Aura Motors".cliente WHERE cpf = ?',(cpf,))
        cursor.fetchone()
        
        if not cliente:
            print(f"\nAviso: Nenhum cliente encontrado com cpf de numero {cpf}.")
            return
        
        nome_cliente = cliente[0]
        cursor.execute('DELETE FROM "Aura Motors".cliente WHERE cpf = ?',(cpf,))
        conexao.commit()
        print(f"\nSucesso: O cliente '{nome_cliente}' foi removido do sistema!")
        
    except pyodbc.IntegrityError:
        print(f"\nErro de integridade: Não é possível remover o cliente '{nome_cliente}' pois tem histórico de compra!")
        
    except Exception as error:
        print(f"\nErro inesperado ao remover o cliente: {error}")
        conexao.rollback()
        
    finally:
        cursor.close()
        conexao.close()
        
        
def listar_desempenho_colaboradores():
    conexao = abrir_conexao()
    if not conexao:
        return
    
    try:
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM "Aura Motors".mv_12_desempenho_colaboradores;')
        
        colunas = [column[0] for column in cursor.description]
        resultado = cursor.fetchall()
        
        print("\n--- DESEMPENHO DOS COLABORADORES ---")
        print(" | ".join(colunas))
        print("-" * 70)
        
        for linha in resultado:
            print(" | ".join(str(valor) for valor in linha))
    except Exception as error:
        print(f"\nErro ao listar colaboradores: {error}")
    finally:
        cursor.close()
        conexao.close()
        

def adicionar_colaborador(nome,cpf,cargo):
    conexao = abrir_conexao()
    if not conexao:
        return
    
    try:
        cursor = conexao.cursor()
        cursor.execute('INSERT INTO "Aura Motors".colaborador (nome, cpf, cargo) VALUES (?, ?, ?)', (nome, cpf, cargo))
        conexao.commit()
        
        print(f"\nSucesso: O colaborador '{nome}' com '{cargo}' foi adicionado ao sistema!")
        
    except Exception as error:
        print(f"\nErro ao registrar colaborador: {error}")
        conexao.rollback()
    finally:
        cursor.close()
        conexao.close()
        
        
def remover_colaborador(cpf):
    conexao = abrir_conexao()
    if not conexao:
        return
    
    try:
        cursor = conexao.cursor()
        cursor.execute('SELECT nome FROM "Aura Motors".colaborador WHERE cpf = ?',(cpf,))
        colaborador = cursor.fetchone()
        
        if not colaborador:
            print(f"\nAviso: Nenhum colaborador com cpf de número {cpf} encontrado.")
            return
        
        nome_colaborador = colaborador[0]
        cursor.execute('DELETE FROM "Aura Motors".colaborador WHERE cpf = ?',(cpf,))
        conexao.commit()
        print(f"\nSucesso: O colaborador '{nome_colaborador}' foi removido do sistema!")
        
    except pyodbc.IntegrityError:
        print(f"\nErro de integridade: Não é possível remover o colaborador '{nome_colaborador}' pois tem histórico de vendas!")
    except Exception as error:
        print(f"\nErro inesperado ao remover o colaborador: {error}")
        conexao.rollback()
    finally:
        cursor.close()
        conexao.close()

    
                
