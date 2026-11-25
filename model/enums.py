from enum import Enum

class FormaPagamento(Enum):
    PIX = "Pix"
    DINHEIRO = "Dinheiro"
    CREDITO = "Cartão de crédito"
    DEBITO = "Cartão de débito"


class StatusVenda(Enum):
    PENDENTE = "Pendente"
    FINALIZADA = "Finalizada"
    CANCELADA = "Cancelada"


class TipoProduto(Enum):
    JOGO = "Jogo"
    FIGURE = "Figure"
    ACESSORIO = "Acessório"
