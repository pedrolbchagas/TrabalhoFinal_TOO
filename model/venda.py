from dataclasses import dataclass

from model.produto import Produto
from states.estado_venda import VendaPendente


@dataclass(frozen=True)
class ItemVenda:
    produto: Produto
    quantidade: int

    @property
    def subtotal(self):
        return self.produto.preco * self.quantidade


class Venda:
    def __init__(self, codigo, cliente, funcionario):
        self.__codigo = codigo
        self.__cliente = cliente
        self.__funcionario = funcionario
        self.__itens = []
        self.__forma_pagamento = None
        self.__valor_pago = None
        self.__estado = VendaPendente()


    @property
    def codigo(self):
        return self.__codigo

    @property
    def cliente(self):
        return self.__cliente

    @property
    def funcionario(self):
        return self.__funcionario

    @property
    def itens(self):
        return tuple(self.__itens)

    @property
    def status(self):
        return self.__estado.status

    @property
    def forma_pagamento(self):
        return self.__forma_pagamento

    @property
    def valor_pago(self):
        return self.__valor_pago

    @property
    def valor_total(self):
        return sum(item.subtotal for item in self.__itens)

    
    def adicionar_produto(self, produto, quantidade):
        self.__estado.adicionar_produto(self, produto, quantidade)

    def calcular_pagamento(self, estrategia):
        
        return estrategia.calcular_valor(self.valor_total)

    def finalizar_venda(self, estrategia):
        self.__estado.finalizar(self, estrategia)

    def cancelar_venda(self):
        self.__estado.cancelar(self)

    def exibir_resumo(self):
        print(f"Venda #{self.codigo} - {self.status.value}")
        print(f"Cliente: {self.cliente.nome}")
        print(f"Funcionário: {self.funcionario.nome}")
        for item in self.__itens:
            print(f"  {item.quantidade}x {item.produto.nome} = R$ {item.subtotal:.2f}")
        print(f"Total: R$ {self.valor_total:.2f}")
        if self.__valor_pago is not None:
            print(f"Pago via {self.__forma_pagamento.value}: R$ {self.__valor_pago:.2f}")


    def _registrar_item(self, produto, quantidade):
        self.__itens.append(ItemVenda(produto, quantidade))

    def _registrar_pagamento(self, estrategia):
        self.__forma_pagamento = estrategia.forma
        self.__valor_pago = estrategia.calcular_valor(self.valor_total)

    def _mudar_estado(self, novo_estado):
        self.__estado = novo_estado
