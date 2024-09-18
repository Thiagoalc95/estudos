menu_principal = """

[1] Cadastrar Usuário
[2] Cadastrar Conta
[3] Listar Contas
[4] Acessar Conta
[q] Sair

=> """

menu_conta = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

usuarios = []
contas = []
numero_conta_sequencial = 1
AGENCIA = "0001"

# Função para cadastrar usuários
def cadastrar_usuario(nome, data_nascimento, cpf, endereco):
    global usuarios

    cpf = cpf.replace(".", "").replace("-", "")

    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            print("Erro: Já existe um usuário cadastrado com esse CPF.")
            return

    novo_usuario = {
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    }

    usuarios.append(novo_usuario)
    print("Usuário cadastrado com sucesso!")

# Função para buscar usuário pelo CPF
def buscar_usuario_por_cpf(cpf):
    cpf = cpf.replace(".", "").replace("-", "")
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return usuario
    return None

# Função para cadastrar contas bancárias
def cadastrar_conta(cpf):
    global contas, numero_conta_sequencial, AGENCIA

    usuario = buscar_usuario_por_cpf(cpf)
    if not usuario:
        print("Erro: Usuário não encontrado.")
        return

    nova_conta = {
        "agencia": AGENCIA,
        "numero_conta": numero_conta_sequencial,
        "usuario": usuario,
        "saldo": 0,
        "extrato": "",
        "numero_saques": 0
    }

    contas.append(nova_conta)
    numero_conta_sequencial += 1
    print(f"Conta criada com sucesso! Agência: {AGENCIA} Número da Conta: {nova_conta['numero_conta']}")

# Função para listar contas bancárias
def listar_contas():
    global contas
    if contas:
        print("\n===== Lista de Contas =====")
        for conta in contas:
            print(f"Agência: {conta['agencia']}, Número da Conta: {conta['numero_conta']}")
            print(f"Titular: {conta['usuario']['nome']} (CPF: {conta['usuario']['cpf']})")
            print("===============================")
    else:
        print("Nenhuma conta cadastrada.")

# Função para buscar conta por número de conta
def buscar_conta(numero_conta):
    for conta in contas:
        if conta["numero_conta"] == numero_conta:
            return conta
    return None

# Função para realizar depósito com positional-only arguments
def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")
    
    return saldo, extrato

# Função para realizar saque com keyword-only arguments
def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")
    
    return saldo, extrato

# Função para exibir extrato
def exibir_extrato(conta):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not conta["extrato"] else conta["extrato"])
    print(f"\nSaldo: R$ {conta['saldo']:.2f}")
    print("==========================================")

# Loop principal para o sistema
while True:
    opcao_principal = input(menu_principal)

    if opcao_principal == "1":
        nome = input("Informe o nome: ")
        data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
        cpf = input("Informe o CPF: ")
        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

        cadastrar_usuario(nome, data_nascimento, cpf, endereco)

    elif opcao_principal == "2":
        cpf = input("Informe o CPF do usuário para cadastrar uma conta: ")
        cadastrar_conta(cpf)

    elif opcao_principal == "3":
        listar_contas()

    elif opcao_principal == "4":
        numero_conta = int(input("Informe o número da conta para acessar: "))
        conta = buscar_conta(numero_conta)

        if conta:
            while True:
                opcao_conta = input(menu_conta)

                if opcao_conta == "d":
                    valor = float(input("Informe o valor do depósito: "))
                    saldo_atualizado, extrato_atualizado = depositar(
                        conta["saldo"],
                        valor,
                        conta["extrato"]
                    )
                    conta["saldo"] = saldo_atualizado
                    conta["extrato"] = extrato_atualizado

                elif opcao_conta == "s":
                    valor = float(input("Informe o valor do saque: "))
                    saldo_atualizado, extrato_atualizado = sacar(
                        saldo=conta["saldo"],
                        valor=valor,
                        extrato=conta["extrato"],
                        limite=500,
                        numero_saques=conta["numero_saques"],
                        limite_saques=3
                    )
                    conta["saldo"] = saldo_atualizado
                    conta["extrato"] = extrato_atualizado
                    conta["numero_saques"] += 1

                elif opcao_conta == "e":
                    exibir_extrato(conta)

                elif opcao_conta == "q":
                    break

                else:
                    print("Operação inválida, por favor selecione novamente a operação desejada.")
        else:
            print("Conta não encontrada com esse número.")

    elif opcao_principal == "q":
        break

    else:
        print("Opção inválida, por favor selecione novamente.")
