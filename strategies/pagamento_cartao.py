from model.enums import FormaPagamento
from strategies.pagamento import Pagamento


class PagamentoCartao(Pagamento):
    JUROS_PARCELADO = 0.03 

    def __init__(self, credito=True, parcelas=1):
        if parcelas < 1:
            raise ValueError("O número de parcelas deve ser pelo menos 1.")
        if not credito and parcelas > 1:
            raise ValueError("Débito não pode ser parcelado.")
        self.__credito = credito
        self.__parcelas = parcelas

    @property
    def forma(self):
        return FormaPagamento.CREDITO if self.__credito else FormaPagamento.DEBITO

    @property
    def parcelas(self):
        return self.__parcelas

    def calcular_valor(self, valor):
        if self.__parcelas > 1:
            valor *= 1 + self.JUROS_PARCELADO
        return round(valor, 2)
