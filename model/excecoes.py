class LojaError(Exception):
    """Erro base do sistema da loja."""


class EstoqueInsuficienteError(LojaError):
    """Tentativa de retirar mais itens do que existem no estoque."""


class ProdutoDuplicadoError(LojaError):
    """Já existe um produto com o mesmo código no estoque."""


class ProdutoNaoEncontradoError(LojaError):
    """Produto inexistente no estoque."""


class OperacaoInvalidaError(LojaError):
    """Operação não permitida no estado atual da venda."""
