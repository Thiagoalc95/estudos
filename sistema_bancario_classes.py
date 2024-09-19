from abc import ABC, abstractmethod
from datetime import datetime

class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor
        self.data = datetime.now()
    
    def registrar(self, conta):
        conta.saldo += self.valor
        conta.historico.adicionar_transacao(self)

    def __str__(self):
        return f"Depósito de R$ {self.valor:.2f} em {self.data.strftime('%d/%m/%Y %H:%M:%S')}"

class Saque(Transacao):
    VALOR_MAXIMO_SAQUE = 500.0  # Limite máximo por saque

    def __init__(self, valor):
        self.valor = valor
        self.data = datetime.now()
    
    def registrar(self, conta):
        if self.valor > Saque.VALOR_MAXIMO_SAQUE:
            print(f"Erro: O valor máximo para saque é R$ {Saque.VALOR_MAXIMO_SAQUE:.2f}.")
            return
        
        if conta.saldo >= self.valor:
            conta.saldo -= self.valor
            conta.historico.adicionar_transacao(self)
        else:
            print("Saldo insuficiente!")

    def __str__(self):
        return f"Saque de R$ {self.valor:.2f} em {self.data.strftime('%d/%m/%Y %H:%M:%S')}"

class Historico:
    def __init__(self):
        self.transacoes = []
    
    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)
    
    def mostrar_historico(self):
        if not self.transacoes:
            print("Nenhuma transação registrada.")
        else:
            for transacao in self.transacoes:
                print(transacao)

class Conta:
    def __init__(self, numero, agencia, cliente):
        self.saldo = 0.0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()
    
    def depositar(self, valor):
        deposito = Deposito(valor)
        deposito.registrar(self)

class ContaCorrente(Conta):
    def __init__(self, numero, agencia, cliente, limite = 500, limite_saques = 3):
        super().__init__(numero, agencia, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        self.saques_realizados = 0  # Controla quantos saques foram feitos

    def sacar(self, valor):
        if self.saques_realizados >= self.limite_saques:
            print(f"Erro: Limite de {self.limite_saques} saques atingido.")
        else:
            saque = Saque(valor)
            if valor <= Saque.VALOR_MAXIMO_SAQUE:
                saque.registrar(self)
                if self.saldo >= valor:
                    self.saques_realizados += 1
            else:
                print(f"Erro: Valor máximo por saque é de R$ {Saque.VALOR_MAXIMO_SAQUE:.2f}.")

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento
