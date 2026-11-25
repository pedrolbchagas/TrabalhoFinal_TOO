from abc import ABC, abstractmethod


class Pagamento(ABC):


    @property
    @abstractmethod
    def forma(self):
        """"""

    @abstractmethod
    def calcular_valor(self, valor):
        """"""
