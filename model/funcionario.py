from model.pessoa import Pessoa


class Funcionario(Pessoa):
    def __init__(self, nome, cpf, matricula, cargo, salario, telefone="", email=""):
        super().__init__(nome, telefone, email)
        self.__cpf = cpf
        self.__matricula = matricula
        self.cargo = cargo
        self.salario = salario

    @property
    def cpf(self):
        return self.__cpf

    @property
    def matricula(self):
        return self.__matricula

    @property
    def salario(self):
        return self.__salario

    @salario.setter
    def salario(self, valor):
        if valor < 0:
            raise ValueError("O salário não pode ser negativo.")
        self.__salario = valor

    def atualizar_cargo(self, novo_cargo):
        self.cargo = novo_cargo

    def exibir_dados(self):
        self._exibir_base()
        print(f"CPF: {self.cpf}")
        print(f"Matrícula: {self.matricula}")
        print(f"Cargo: {self.cargo}")
        print(f"Salário: R$ {self.salario:.2f}")
