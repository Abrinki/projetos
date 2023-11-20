import pandas as pd
from datetime import datetime

# Verifica se o arquivo Excel existe, se não, cria um novo
try:
    df = pd.read_excel('estoque.xlsx')
except FileNotFoundError:
    df = pd.DataFrame(columns=['Produto', 'Quantidade', 'Valor', 'Data'])

def adicionar_produto():
    produto = input("Nome do produto: ")
    quantidade = int(input("Quantidade: "))
    valor = float(input("Valor por unidade: "))
    data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    novo_produto = pd.DataFrame([[produto, quantidade, valor, data]],
                                columns=['Produto', 'Quantidade', 'Valor', 'Data'])

    df_global = pd.concat([df, novo_produto], ignore_index=True)
    df_global.to_excel('estoque.xlsx', index=False)
    print(f"{produto} adicionado ao estoque com sucesso.")

def remover_produto():
    produto = input("Nome do produto a ser removido: ")
    quantidade = int(input("Quantidade a ser removida: "))
    data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Verifica se o produto está no estoque
    if produto in df['Produto'].values:
        index = df.index[df['Produto'] == produto].tolist()[0]

        # Verifica se há quantidade suficiente para a remoção
        if df.at[index, 'Quantidade'] >= quantidade:
            df.at[index, 'Quantidade'] -= quantidade
            df.at[index, 'Data'] = data
            df.to_excel('estoque.xlsx', index=False)
            print(f"{quantidade} unidades de {produto} removidas do estoque.")
        else:
            print(f"Quantidade insuficiente de {produto} no estoque.")
    else:
        print(f"{produto} não encontrado no estoque.")

def exibir_produtos():
    print(df)

while True:
    print("\n1. Adicionar Produto\n2. Remover Produto\n3. Exibir Produtos\n4. Sair")
    opcao = input("Escolha uma opção: ")

    if opcao == '1':
        adicionar_produto()
    elif opcao == '2':
        remover_produto()
    elif opcao == '3':
        exibir_produtos()
    elif opcao == '4':
        break
    else:
        print("Opção inválida. Tente novamente.")
