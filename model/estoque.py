from model.excecoes import ProdutoDuplicadoError, ProdutoNaoEncontradoError


class Estoque:
    LIMITE_ESTOQUE_BAIXO = 5

    def __init__(self):
        self.__produtos = {}  # codigo -> Produto

    def cadastrar_produto(self, novo_produto):
        if novo_produto.codigo in self.__produtos:
            raise ProdutoDuplicadoError(
                f"'{novo_produto.nome}' (código {novo_produto.codigo}) já está cadastrado."
            )
        self.__produtos[novo_produto.codigo] = novo_produto

    def buscar_produto(self, codigo):
        try:
            return self.__produtos[codigo]
        except KeyError:
            raise ProdutoNaoEncontradoError(f"Produto de código '{codigo}' não encontrado.")

    def repor_estoque(self, codigo, quantidade, fornecedor=None):
        produto = self.buscar_produto(codigo)
        produto.repor(quantidade)
        origem = f" (fornecedor: {fornecedor.nome})" if fornecedor else ""
        print(f"Reposição: +{quantidade} de '{produto.nome}'{origem}.")

    def remover_produto(self, codigo):
        produto = self.buscar_produto(codigo)
        del self.__produtos[codigo]
        print(f"Produto '{produto.nome}' removido.")

    def listar_produtos(self):

        return list(self.__produtos.values())

    def exibir_produtos(self):
        for produto in self.__produtos.values():
            print(f"{produto.codigo} | {produto.nome} - Quantidade: {produto.quantidade}")

    def produtos_com_estoque_baixo(self):
        return [p for p in self.__produtos.values() if p.quantidade <= self.LIMITE_ESTOQUE_BAIXO]

    def verificar_estoque(self):
        for produto in self.produtos_com_estoque_baixo():
            print(f"Estoque baixo: {produto.nome} ({produto.quantidade} un.)")
