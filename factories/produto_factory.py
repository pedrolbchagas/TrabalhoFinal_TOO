from model.enums import TipoProduto
from model.produto import Acessorio, Figure, Jogo


class ProdutoFactory:


    _TIPOS = {
        TipoProduto.JOGO: (Jogo, ("plataforma",)),
        TipoProduto.FIGURE: (Figure, ("personagem", "tipo_figure")),
        TipoProduto.ACESSORIO: (Acessorio, ("tipo_acessorio",)),
    }

    @staticmethod
    def criar_produto(tipo, nome, codigo, preco, quantidade, **dados):
        if tipo not in ProdutoFactory._TIPOS:
            raise ValueError("Tipo de produto inválido!")

        classe, campos = ProdutoFactory._TIPOS[tipo]
        faltando = [c for c in campos if c not in dados]
        if faltando:
            raise ValueError(f"Faltam dados para criar {tipo.value}: {', '.join(faltando)}")

        extras = [dados[c] for c in campos]
        return classe(nome, codigo, preco, quantidade, *extras)
