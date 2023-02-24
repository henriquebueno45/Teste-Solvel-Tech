# Autor: Henrique Bueno de Morais - Teste Solvel Light
# Decidi fazer tudo no mesmo arquivo para enviar apenas um
import json

TAMANHO_MAXIMO = 10 # Tamanho máximo do carrinho
carrinho = {}
compra_finalizada = False


# O ARQUIVO DE RELAÇÃO DE CADASTRO DOS CLIENTES SERÁ SALVO NO MESMO DIRETÓRIO DO CÓDIGO-FONTE
def save():
    nome_cliente = input("Digite o nome do cliente: ")
    cpf = int(input("Digite o CPF do cliente: "))
    email = input("Digite o email do cliente: ")
    celular = int(input("Digite o celular do cliente: "))

    # Estrutura o dicionário com as informações do cliente
    new_data = {
        nome_cliente: {
            "email": email,
            "celular": celular,
            "cpf": cpf,
        }
    }
    # Tenta abrir o arquivo para leitura e coleta das informações ali contidas
    try:
        with open("cadastroClientes.json", "r") as cadastro:
            # Carrega as info. do arquivo
            data = json.loads(cadastro.read())
    # Caso não haja um arquivo de registro, cria um e já envia as novas informações de cliente para o arquivo
    except FileNotFoundError:  # Caso não encontre o arquivo, criará um
        with open("cadastroClientes.json", "w") as cadastro:
            json.dump(new_data, cadastro, indent=4)
    else:
        # Atualiza os dados antigos com as novas informações geradas
        data.update(new_data)
        with open("cadastroClientes.json", "w") as cadastro:
            # envia os dados atualizados para o arquivo
            json.dump(data, cadastro, indent=4)


def cadastro_novo_carrinho():
    new_product = input("Nome do produto: ")
    try:
        carrinho[new_product] = int(input("Valor: "))
    except ValueError:
        print("Digite um valor numérico")
        carrinho[new_product] = None
    if len(new_product) == 0 or carrinho[new_product] is None:
        print("Preencha os dados corretamente")
        cadastro_novo_carrinho()


# A cada iteração, é feita a divisão absoluta do valor restante pelo valor da nota, e
# depois é retirada do valor restante o equivalente a divisão absoluta vezes o peso da nota
def calcula_notas(valor):
    valores_notas = [100, 50, 20, 10, 5, 2, 1]
    current_value = valor
    for value in valores_notas:
        pivo = current_value // value
        current_value -= pivo * value
        if pivo != 0:
            print(f"{pivo} notas de R${value}")


# Soma o valor de todos os produtos adicionados e chama a função de contar as notas
def fechar_venda():
    valorTotal = 0.0
    print("\nProdutos do carrinho: \n")
    for key, value in carrinho.items():
        print(f"{key} - Valor: R${value}")
        valorTotal += value
    print(f"\nValor total: R${valorTotal} reais")
    calcula_notas(valorTotal)


# INÍCIO DE EXECUÇÃO
cadastro_novo_carrinho()

while len(carrinho) < TAMANHO_MAXIMO and not compra_finalizada:
    choice = int(input("Adicionar novo produto? [1]Sim ou [2]Não: "))
    if choice == 1:
        cadastro_novo_carrinho()
    else:
        compra_finalizada = True

fechar_venda()

choice = int(input("Já possui cadastro? [1]Sim ou [2]Não: "))
if choice == 1:
    name = input("Nome do cliente: ")
    try:
        with open("cadastroClientes.json", "r") as cadastro:
            datas = json.loads(cadastro.read())
            if name not in datas:
                choice = int(input("Não consta no cadastro. Gostaria de fazer o cadastro? [1]Sim ou [2]Não: "))
                if choice == 1:
                    save()
    except FileNotFoundError:
        choice = int(input("Não consta no cadastro. Gostaria de fazer o cadastro? [1]Sim ou [2]Não: "))
        if choice == 1:
            save()
else:
    save()

print("Compra finalizada!")
