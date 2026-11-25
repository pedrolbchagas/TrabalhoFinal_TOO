from model.pessoa import Pessoa


class Cliente(Pessoa):
    def __init__(self, nome, cpf, telefone, email):
        super().__init__(nome, telefone, email)
        self.__cpf = cpf

    @property
    def cpf(self):
        return self.__cpf

    def exibir_dados(self):
        self._exibir_base()
        print(f"CPF: {self.cpf}")
