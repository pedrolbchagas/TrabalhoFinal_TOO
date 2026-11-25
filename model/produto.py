from abc import ABC, abstractmethod

from model.enums import TipoProduto
from model.excecoes import EstoqueInsuficienteError


class Produto(ABC):

    def __init__(self, nome, codigo, preco, quantidade):
        if not nome or not str(nome).strip():
            raise ValueError("O nome do produto não pode ser vazio.")
        if quantidade < 0:
            raise ValueError("A quantidade não pode ser negativa.")
        self.__nome = nome
        self.__codigo = codigo
        self.__quantidade = quantidade
        self.preco = preco  # passa pela validação do setter

    @property
    def nome(self):
        return self.__nome

    @property
    def codigo(self):
        return self.__codigo

    @property
    def quantidade(self):
        return self.__quantidade

    @property
    def preco(self):
        return self.__preco

    @preco.setter
    def preco(self, novo_preco):
        if novo_preco < 0:
            raise ValueError("O preço não pode ser negativo.")
        self.__preco = novo_preco

    def baixar_estoque(self, quantidade):
        if quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")
        if quantidade > self.__quantidade:
            raise EstoqueInsuficienteError(
                f"'{self.nome}': pedido {quantidade}, disponível {self.__quantidade}."
            )
        self.__quantidade -= quantidade

    def repor(self, quantidade):
        if quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")
        self.__quantidade += quantidade

    @property
    @abstractmethod
    def tipo(self):
        """"""

    @abstractmethod
    def _detalhes_especificos(self):
        """"""

    def exibir_detalhes(self):
        print(f"Tipo: {self.tipo.value}")
        print(f"Nome: {self.nome}")
        print(f"Código: {self.codigo}")
        print(f"Preço: R$ {self.preco:.2f}")
        print(f"Quantidade: {self.quantidade}")
        self._detalhes_especificos()


class Jogo(Produto):
    def __init__(self, nome, codigo, preco, quantidade, plataforma):
        super().__init__(nome, codigo, preco, quantidade)
        self.__plataforma = plataforma

    @property
    def plataforma(self):
        return self.__plataforma

    @property
    def tipo(self):
        return TipoProduto.JOGO

    def _detalhes_especificos(self):
        print(f"Plataforma: {self.plataforma}")


class Figure(Produto):
    def __init__(self, nome, codigo, preco, quantidade, personagem, tipo_figure):
        super().__init__(nome, codigo, preco, quantidade)
        self.__personagem = personagem
        self.__tipo_figure = tipo_figure  

    @property
    def personagem(self):
        return self.__personagem

    @property
    def tipo_figure(self):
        return self.__tipo_figure

    @property
    def tipo(self):
        return TipoProduto.FIGURE

    def _detalhes_especificos(self):
        print(f"Personagem: {self.personagem}")
        print(f"Tipo de figure: {self.tipo_figure}")


class Acessorio(Produto):
    def __init__(self, nome, codigo, preco, quantidade, tipo_acessorio):
        super().__init__(nome, codigo, preco, quantidade)
        self.__tipo_acessorio = tipo_acessorio  

    @property
    def tipo_acessorio(self):
        return self.__tipo_acessorio

    @property
    def tipo(self):
        return TipoProduto.ACESSORIO

    def _detalhes_especificos(self):
        print(f"Tipo de acessório: {self.tipo_acessorio}")
