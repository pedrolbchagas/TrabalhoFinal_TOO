from model.pessoa import Pessoa


class Fornecedor(Pessoa):
    def __init__(self, nome, cnpj, telefone, email, endereco):
        super().__init__(nome, telefone, email)
        self.__cnpj = cnpj
        self.endereco = endereco

    @property
    def cnpj(self):
        return self.__cnpj

    def exibir_dados(self):
        self._exibir_base()
        print(f"CNPJ: {self.cnpj}")
        print(f"Endereço: {self.endereco}")
