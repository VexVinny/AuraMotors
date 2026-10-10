import sys
from modulos.estoque import listar_veiculos, listar_marcas
from modulos.pessoas import listar_clientes, listar_colaboradores
from modulos.vendas import listar_vendas, listar_veiculos_nunca_vendidos

# ARQUIVO PRINCIPAL PRA TESTE DO BACKEND
def menu_principal():
    while True:
        print("\n" + "="*50)
        print("SISTEMA AURA MOTORS - MODO TERMINAL")
        print("="*50)
        print("1. Listar Veículos em Estoque")
        print("2. Listar Clientes Cadastrados")
        print("3. Listar Colaboradores")
        print("4. Listar Histórico de Vendas")
        print("5. Relatório: Veículos Nunca Vendidos (Consulta EXCEPT)")
        print("0. Sair")
        print("="*50)
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            print("\n--- VEÍCULOS EM ESTOQUE ---")
            veiculos = listar_veiculos()
            if not veiculos:
                print("Nenhum veículo encontrado.")
            else:
                for v in veiculos:
                    # Assumindo a ordem: ID, Modelo, Ano, Preço...
                    print(f"ID: {v[0]} | Modelo: {v[1]} | Ano: {v[2]} | Preço: R$ {v[3]:.2f} | Status: {v[4]}")
                
        elif opcao == '2':
            print("\n--- CLIENTES CADASTRADOS ---")
            clientes = listar_clientes()
            if not clientes:
                print("Nenhum cliente encontrado.")
            else:
                for c in clientes:
                    print(f"Nome: {c[0]} | CPF: {c[1]} | E-mail: {c[2]}")
                    
        elif opcao == '3':
            print("\n--- COLABORADORES ---")
            colaboradores = listar_colaboradores()
            if not colaboradores:
                print("Nenhum colaborador encontrado.")
            else:
                for colab in colaboradores:
                    print(f"Nome: {colab[0]} | CPF: {colab[1]} | Cargo: {colab[2]}")
                
        elif opcao == '4':
            print("\n--- HISTÓRICO DE VENDAS ---")
            vendas = listar_vendas()
            if not vendas:
                print("Nenhuma venda registrada.")
            else:
                for v in vendas:
                    # v[3] = nome do cliente, v[4] = nome do colaborador (conforme seu INNER JOIN)
                    print(f"Venda #{v[0]} | Data: {v[1]} | Valor: R$ {v[2]:.2f} | Cliente: {v[3]} | Vendedor: {v[4]}")
                
        elif opcao == '5':
            print("\n--- VEÍCULOS NUNCA VENDIDOS ---")
            veiculos = listar_veiculos_nunca_vendidos()
            if not veiculos:
                print("Todos os veículos do estoque já possuem ao menos uma venda vinculada.")
            else:
                for v in veiculos:
                    print(f"ID: {v[0]} | Modelo: {v[1]} | Preço: R$ {v[2]:.2f}")
                    
        elif opcao == '0':
            print("\nA encerrar o sistema Aura Motors. Até logo!")
            sys.exit()
            
        else:
            print("\n[!] Opção inválida. Tente novamente.")

if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\nSistema encerrado de forma forçada pelo utilizador.")
        sys.exit()