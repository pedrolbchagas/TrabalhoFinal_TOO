from factories.produto_factory import ProdutoFactory
from model.cliente import Cliente
from model.enums import TipoProduto
from model.estoque import Estoque
from model.excecoes import LojaError
from model.fornecedor import Fornecedor
from model.funcionario import Funcionario
from model.venda import Venda
from strategies.pagamento_cartao import PagamentoCartao
from strategies.pagamento_pix import PagamentoPix


def titulo(texto):
    print(f"\n===== {texto} =====")



cliente1 = Cliente("João", "12345678900", "99999-9999", "joao@email.com")
funcionario1 = Funcionario("Maria", "98765432100", "001", "Vendedor", 2500)
fornecedor1 = Fornecedor("Game Distribuidora", "12345678000199",
                         "3333-4444", "game@email.com", "Rua Central")

titulo("Exibir dados de cada pessoa")
for pessoa in (cliente1, funcionario1, fornecedor1):
    pessoa.exibir_dados()
    print("-" * 20)


jogo1 = ProdutoFactory.criar_produto(
    TipoProduto.JOGO, "God of War", "001", 199.90, 10, plataforma="PlayStation")
figure1 = ProdutoFactory.criar_produto(
    TipoProduto.FIGURE, "Leon", "002", 375.50, 1,
    personagem="Leon Kennedy RE4", tipo_figure="3D")
chaveiro1 = ProdutoFactory.criar_produto(
    TipoProduto.ACESSORIO, "Chaveiro Triforce", "003", 29.90, 20,
    tipo_acessorio="Chaveiro")

titulo("Exibir detalhes de cada produto")
for produto in (jogo1, figure1, chaveiro1):
    produto.exibir_detalhes()
    print("-" * 20)


estoque = Estoque()
for produto in (jogo1, figure1, chaveiro1):
    estoque.cadastrar_produto(produto)

titulo("Teste: produto duplicado")
try:
    estoque.cadastrar_produto(jogo1)
except LojaError as erro:
    print("Erro esperado:", erro)


titulo("Venda 1: pagamento via Pix")
venda1 = Venda(1, cliente1, funcionario1)
venda1.adicionar_produto(jogo1, 2)
venda1.adicionar_produto(chaveiro1, 1)
print(f"Total: R$ {venda1.valor_total:.2f}")
print(f"Simulação Pix:            R$ {venda1.calcular_pagamento(PagamentoPix()):.2f}")
print(f"Simulação crédito 3x:     R$ {venda1.calcular_pagamento(PagamentoCartao(True, 3)):.2f}")
venda1.finalizar_venda(PagamentoPix())
venda1.exibir_resumo()

titulo("Teste: venda finalizada não aceita mais produtos")
try:
    venda1.adicionar_produto(jogo1, 1)
except LojaError as erro:
    print("Erro esperado:", erro)


titulo("Venda 2: estoque insuficiente")
venda2 = Venda(2, cliente1, funcionario1)
try:
    venda2.adicionar_produto(figure1, 5)
except LojaError as erro:
    print("Erro esperado:", erro)

titulo("Venda 3: cancelamento devolve o estoque")
venda3 = Venda(3, cliente1, funcionario1)
venda3.adicionar_produto(jogo1, 3)
print("Estoque do jogo durante a venda:", jogo1.quantidade)
venda3.cancelar_venda()
print("Estoque do jogo após cancelar: ", jogo1.quantidade)
print("Status:", venda3.status.value)

titulo("Teste: venda vazia")
venda4 = Venda(4, cliente1, funcionario1)
try:
    venda4.finalizar_venda(PagamentoPix())
except LojaError as erro:
    print("Erro esperado:", erro)


titulo("Teste: encapsulamento")
try:
    jogo1.preco = -10
except ValueError as erro:
    print("Erro esperado:", erro)


titulo("Estoque")
estoque.verificar_estoque()
estoque.repor_estoque("002", 10, fornecedor1)
estoque.exibir_produtos()
