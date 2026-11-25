from abc import ABC, abstractmethod


class Pessoa(ABC):

    def __init__(self, nome, telefone, email):
        self.nome = nome
        self.telefone = telefone
        self.email = email

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, valor):
        if not valor or not str(valor).strip():
            raise ValueError("O nome não pode ser vazio.")
        self.__nome = str(valor).strip()

    @property
    def telefone(self):
        return self.__telefone

    @telefone.setter
    def telefone(self, valor):
        self.__telefone = valor

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, valor):
        if valor and "@" not in valor:
            raise ValueError("E-mail inválido.")
        self.__email = valor

    def atualizar_telefone(self, novo_telefone):
        self.telefone = novo_telefone

    @abstractmethod
    def exibir_dados(self):
        """Cada subclasse mostra seus próprios dados (polimorfismo)."""

    def _exibir_base(self):
        print(f"Nome: {self.nome}")
        print(f"Telefone: {self.telefone}")
        print(f"E-mail: {self.email}")
