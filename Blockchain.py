'''      Leandro Sena Silva - 9293060 [ trabalho de blockchain e criptomoedas ]  '''



import hashlib
import json
from time import time

class Ledger:
    def __init__(self):
        self.bloco_registrado = []
        self.identidades_temp = []
        self.criar_bloco(ultimo_hash='0', ultima_prova=1)

    def criar_bloco(self, ultima_prova, ultimo_hash=None):
        bloco = {
            'numero.bloco': len(self.bloco_registrado) + 1,
            'timestamp': time(),
            'identidades.a.adicionar': self.identidades_temp,
            'prova.de.trabalho': ultima_prova,
            'hash.anterior': ultimo_hash or self.gerar_hash(self.bloco_registrado[-1]) if self.bloco_registrado else None
        }
        self.identidades_temp = []
        self.bloco_registrado.append(bloco)
        return bloco

    def adicionar_identidade(self, info_identidade):
        """         Adiciona uma nova identidade            """
        self.identidades_temp.append(info_identidade)

    def obter_ultimo_bloco(self):
        """     Retorna o último bloco registrado na cadeia de blocos      """
        return self.bloco_registrado[-1]

    @staticmethod
    def gerar_hash(bloco):
        """             Gera o hash de um bloco         """
        bloco_str = json.dumps(bloco, sort_keys=True).encode()
        return hashlib.sha256(bloco_str).hexdigest()

    def minerar_bloco(self, ultima_prova):
        """            Prova de Trabalho (Proof of Work)           """
        prova = 0
        while not self.eh_prova_valida(ultima_prova, prova):
            prova += 1
        return prova

    @staticmethod
    def eh_prova_valida(ultima_prova, prova):
        """     Verifica se a combinação da prova é válida          """
        tentativa = f'{ultima_prova}{prova}'.encode()
        tentativa_hash = hashlib.sha256(tentativa).hexdigest()
        return tentativa_hash[:4] == "0000"

    def obter_blocos(self):
        """         Retorna todos os blocos da blockchain          """
        return self.bloco_registrado


def cadastrar_identidade(ledger):
    """     Cadastra uma nova identidade na blockchain       """
    nome = input("Nome completo: ")
    cpf = input("CPF: ")
    email = input("E-mail: ")

    nova_identidade = {
        'nome': nome,
        'cpf': cpf,
        'email': email
    }

    ledger.adicionar_identidade(nova_identidade)
    ultimo_bloco = ledger.obter_ultimo_bloco()
    ultima_prova = ultimo_bloco['prova.de.trabalho']
    nova_prova = ledger.minerar_bloco(ultima_prova)
    ultimo_hash = ledger.gerar_hash(ultimo_bloco)
    ledger.criar_bloco(nova_prova, ultimo_hash)
    print("Identidade registrada com sucesso.")

def exibir_blockchain(ledger):
    """         Exibe toda a blockchain do sistema      """
    print("\nBlockchain:")
    for bloco in ledger.obter_blocos():
        print(json.dumps(bloco, indent=4))

def menu():
    """         Menu de navegação      """
    ledger = Ledger()

    while True:
        print("\nMenu de opções:")
        print("1. Registrar nova identidade")
        print("2. Exibir blockchain")
        print("3. Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            cadastrar_identidade(ledger)
        elif opcao == "2":
            exibir_blockchain(ledger)
        elif opcao == "3":
            print("Encerrando o sistema.")
            break
        else:
            print("Opção não reconhecida.")

if __name__ == "__main__":
    menu()
