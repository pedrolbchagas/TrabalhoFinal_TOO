from model.enums import FormaPagamento
from strategies.pagamento import Pagamento


class PagamentoPix(Pagamento):
    DESCONTO = 0.05  

    @property
    def forma(self):
        return FormaPagamento.PIX

    def calcular_valor(self, valor):
        return round(valor * (1 - self.DESCONTO), 2)
