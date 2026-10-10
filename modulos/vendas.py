# modulo para tabelas (venda e item_venda)
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from conexao import abrir_conexao

def listar_vendas():
    """Busca e retorna todas as vendas registradas no banco."""
    conexao = abrir_conexao()
    if not conexao:
        return []

    try:
        cursor = conexao.cursor()
        query = 'SELECT * FROM "Aura Motors".venda;'
        cursor.execute(query)
        
        vendas = cursor.fetchall()
        
        cursor.close()
        conexao.close()
        return vendas

    except Exception as e:
        print(f"Erro ao buscar vendas: {e}")
        return []
    
def registrar_venda(valor_total, id_cliente, id_colaborador, itens):
    """
    Regista uma venda e os seus itens numa única transação.
    
    Parametro 'itens' deve ser uma lista de tuplos: 
    [(id_veiculo, preco_praticado), ...]
    """
    conexao = abrir_conexao()
    if not conexao:
        return False

    try:
        cursor = conexao.cursor()

        query_venda = '''
            INSERT INTO "Aura Motors".venda (valor_total, id_cliente, id_colaborador)
            VALUES (?, ?, ?)
            RETURNING id_venda;
        '''
        cursor.execute(query_venda, (valor_total, id_cliente, id_colaborador))
        
        id_venda = cursor.fetchone()[0]

        query_item = '''
            INSERT INTO "Aura Motors".item_venda (id_venda, id_veiculo, preco_praticado)
            VALUES (?, ?, ?);
        '''
        for id_veiculo, preco_praticado in itens:
            cursor.execute(query_item, (id_venda, id_veiculo, preco_praticado))

        conexao.commit()
        print(f"Sucesso: Venda número {id_venda} registada com êxito!")

        cursor.close()
        conexao.close()
        return True

    except Exception as e:
        print(f"Erro ao registar venda (alterações canceladas): {e}")
        conexao.rollback()
        conexao.close()
        return False
if __name__ == "__main__":
    print("--- Testando Listagem de Vendas ---")
    vendas = listar_vendas()
    print("Vendas encontradas:", vendas)