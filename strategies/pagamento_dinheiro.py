from model.enums import FormaPagamento
from strategies.pagamento import Pagamento


class PagamentoDinheiro(Pagamento):
    @property
    def forma(self):
        return FormaPagamento.DINHEIRO

    def calcular_valor(self, valor):
        return round(valor, 2)
