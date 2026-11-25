from abc import ABC, abstractmethod

from model.enums import StatusVenda
from model.excecoes import OperacaoInvalidaError


class EstadoVenda(ABC):
    """State: o que a venda pode fazer depende do estado em que ela está."""

    @property
    @abstractmethod
    def status(self):
        """Retorna o StatusVenda correspondente."""

    # Por padrão toda operação é proibida; cada estado libera só o que pode.
    def adicionar_produto(self, venda, produto, quantidade):
        raise OperacaoInvalidaError(
            f"Não é possível adicionar produtos a uma venda {self.status.value.lower()}."
        )

    def finalizar(self, venda, pagamento):
        raise OperacaoInvalidaError(
            f"Não é possível finalizar uma venda {self.status.value.lower()}."
        )

    def cancelar(self, venda):
        raise OperacaoInvalidaError(
            f"Não é possível cancelar uma venda {self.status.value.lower()}."
        )


class VendaPendente(EstadoVenda):
    @property
    def status(self):
        return StatusVenda.PENDENTE

    def adicionar_produto(self, venda, produto, quantidade):
        produto.baixar_estoque(quantidade)  # reserva o estoque
        venda._registrar_item(produto, quantidade)

    def finalizar(self, venda, pagamento):
        if not venda.itens:
            raise OperacaoInvalidaError("Não é possível finalizar uma venda vazia!")
        venda._registrar_pagamento(pagamento)
        venda._mudar_estado(VendaFinalizada())

    def cancelar(self, venda):
        for item in venda.itens:  # devolve o que foi reservado
            item.produto.repor(item.quantidade)
        venda._mudar_estado(VendaCancelada())


class VendaFinalizada(EstadoVenda):
    @property
    def status(self):
        return StatusVenda.FINALIZADA


class VendaCancelada(EstadoVenda):
    @property
    def status(self):
        return StatusVenda.CANCELADA
