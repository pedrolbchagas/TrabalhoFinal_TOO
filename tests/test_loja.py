import unittest

from factories.produto_factory import ProdutoFactory
from model.cliente import Cliente
from model.enums import FormaPagamento, StatusVenda, TipoProduto
from model.estoque import Estoque
from model.excecoes import (EstoqueInsuficienteError, OperacaoInvalidaError,
                            ProdutoDuplicadoError, ProdutoNaoEncontradoError)
from model.funcionario import Funcionario
from model.pessoa import Pessoa
from model.produto import Acessorio, Figure, Jogo, Produto
from model.venda import Venda
from strategies.pagamento_cartao import PagamentoCartao
from strategies.pagamento_dinheiro import PagamentoDinheiro
from strategies.pagamento_pix import PagamentoPix


def novo_jogo(qtd=10):
    return ProdutoFactory.criar_produto(
        TipoProduto.JOGO, "God of War", "001", 100.0, qtd, plataforma="PlayStation")


def nova_venda():
    cliente = Cliente("João", "123", "9999", "joao@email.com")
    func = Funcionario("Maria", "456", "001", "Vendedor", 2500)
    return Venda(1, cliente, func)


class TestPOO(unittest.TestCase):
    def test_classes_abstratas_nao_instanciam(self):
        with self.assertRaises(TypeError):
            Produto("x", "1", 10, 1)
        with self.assertRaises(TypeError):
            Pessoa("x", "1", "a@b.com")

    def test_heranca_e_polimorfismo(self):
        self.assertIsInstance(novo_jogo(), Produto)
        self.assertIsInstance(Cliente("A", "1", "2", "a@b.com"), Pessoa)

    def test_encapsulamento_preco(self):
        jogo = novo_jogo()
        with self.assertRaises(ValueError):
            jogo.preco = -1
        with self.assertRaises(AttributeError):
            jogo.quantidade = 99  

    def test_email_invalido(self):
        with self.assertRaises(ValueError):
            Cliente("A", "1", "2", "sem-arroba")


class TestFactory(unittest.TestCase):
    def test_cria_cada_tipo(self):
        figure = ProdutoFactory.criar_produto(
            TipoProduto.FIGURE, "Leon", "2", 10, 1, personagem="Leon", tipo_figure="3D")
        acessorio = ProdutoFactory.criar_produto(
            TipoProduto.ACESSORIO, "Chaveiro", "3", 5, 1, tipo_acessorio="Chaveiro")
        self.assertIsInstance(novo_jogo(), Jogo)
        self.assertIsInstance(figure, Figure)
        self.assertIsInstance(acessorio, Acessorio)

    def test_dado_faltando(self):
        with self.assertRaises(ValueError):
            ProdutoFactory.criar_produto(TipoProduto.JOGO, "X", "1", 10, 1)

    def test_tipo_invalido(self):
        with self.assertRaises(ValueError):
            ProdutoFactory.criar_produto("jogo", "X", "1", 10, 1)


class TestStrategy(unittest.TestCase):
    def test_valores(self):
        self.assertEqual(PagamentoPix().calcular_valor(100), 95.0)
        self.assertEqual(PagamentoDinheiro().calcular_valor(100), 100.0)
        self.assertEqual(PagamentoCartao(True, 1).calcular_valor(100), 100.0)
        self.assertEqual(PagamentoCartao(True, 3).calcular_valor(100), 103.0)

    def test_formas(self):
        self.assertEqual(PagamentoPix().forma, FormaPagamento.PIX)
        self.assertEqual(PagamentoCartao(False).forma, FormaPagamento.DEBITO)

    def test_debito_nao_parcela(self):
        with self.assertRaises(ValueError):
            PagamentoCartao(credito=False, parcelas=2)


class TestEstoque(unittest.TestCase):
    def test_cadastro_duplicado(self):
        estoque = Estoque()
        estoque.cadastrar_produto(novo_jogo())
        with self.assertRaises(ProdutoDuplicadoError):
            estoque.cadastrar_produto(novo_jogo())

    def test_busca_inexistente(self):
        with self.assertRaises(ProdutoNaoEncontradoError):
            Estoque().buscar_produto("999")

    def test_reposicao_e_estoque_baixo(self):
        estoque = Estoque()
        jogo = novo_jogo(qtd=2)
        estoque.cadastrar_produto(jogo)
        self.assertIn(jogo, estoque.produtos_com_estoque_baixo())
        estoque.repor_estoque("001", 10)
        self.assertEqual(jogo.quantidade, 12)
        self.assertEqual(estoque.produtos_com_estoque_baixo(), [])

    def test_remover(self):
        estoque = Estoque()
        estoque.cadastrar_produto(novo_jogo())
        estoque.remover_produto("001")
        self.assertEqual(estoque.listar_produtos(), [])


class TestVendaState(unittest.TestCase):
    def test_fluxo_completo(self):
        jogo = novo_jogo()
        venda = nova_venda()
        self.assertEqual(venda.status, StatusVenda.PENDENTE)
        venda.adicionar_produto(jogo, 2)
        self.assertEqual(jogo.quantidade, 8)
        self.assertEqual(venda.valor_total, 200.0)
        venda.finalizar_venda(PagamentoPix())
        self.assertEqual(venda.status, StatusVenda.FINALIZADA)
        self.assertEqual(venda.valor_pago, 190.0)
        self.assertEqual(venda.forma_pagamento, FormaPagamento.PIX)

    def test_estoque_insuficiente(self):
        venda = nova_venda()
        with self.assertRaises(EstoqueInsuficienteError):
            venda.adicionar_produto(novo_jogo(qtd=1), 5)
        self.assertEqual(venda.itens, ())

    def test_quantidade_invalida(self):
        with self.assertRaises(ValueError):
            nova_venda().adicionar_produto(novo_jogo(), 0)

    def test_venda_vazia(self):
        with self.assertRaises(OperacaoInvalidaError):
            nova_venda().finalizar_venda(PagamentoPix())

    def test_cancelar_devolve_estoque(self):
        jogo = novo_jogo()
        venda = nova_venda()
        venda.adicionar_produto(jogo, 4)
        venda.cancelar_venda()
        self.assertEqual(jogo.quantidade, 10)
        self.assertEqual(venda.status, StatusVenda.CANCELADA)

    def test_estados_finais_bloqueiam_acoes(self):
        jogo = novo_jogo()
        venda = nova_venda()
        venda.adicionar_produto(jogo, 1)
        venda.finalizar_venda(PagamentoDinheiro())
        for acao in (lambda: venda.adicionar_produto(jogo, 1),
                     lambda: venda.finalizar_venda(PagamentoPix()),
                     venda.cancelar_venda):
            with self.assertRaises(OperacaoInvalidaError):
                acao()


if __name__ == "__main__":
    unittest.main()
