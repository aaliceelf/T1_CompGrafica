
import math

from geometry.geometria import TOLERANCIA


class GradeUniforme:
    def __init__(self, cenario, colunas=10, linhas=10):
        if (
            not isinstance(colunas, int)
            or not isinstance(linhas, int)
            or colunas < 1
            or linhas < 1
        ):
            raise ValueError(
                "Linhas e colunas devem ser inteiros positivos"
            )

        self.cenario = cenario
        self.colunas = colunas
        self.linhas = linhas

        self.largura_celula = cenario.largura / colunas
        self.altura_celula = cenario.altura / linhas

        self.celulas = [
            [[] for _ in range(colunas)]
            for _ in range(linhas)
        ]

        self.construir()

    def localizar_celula(self, ponto):
        if not (
            0 <= ponto.x <= self.cenario.largura
            and 0 <= ponto.y <= self.cenario.altura
        ):
            return None

        coluna = min(
            int(ponto.x / self.largura_celula),
            self.colunas - 1
        )

        linha = min(
            int(ponto.y / self.altura_celula),
            self.linhas - 1
        )

        return linha, coluna

    def construir(self):
        for linha in self.celulas:
            for celula in linha:
                celula.clear()

        for indice, triangulo in enumerate(
            self.cenario.triangulos
        ):
            envelope = triangulo.envelope

            cmin = max(
                0,
                int(math.floor(
                    (envelope.xmin - TOLERANCIA)
                    / self.largura_celula
                ))
            )

            cmax = min(
                self.colunas - 1,
                int(math.floor(
                    (envelope.xmax + TOLERANCIA)
                    / self.largura_celula
                ))
            )

            lmin = max(
                0,
                int(math.floor(
                    (envelope.ymin - TOLERANCIA)
                    / self.altura_celula
                ))
            )

            lmax = min(
                self.linhas - 1,
                int(math.floor(
                    (envelope.ymax + TOLERANCIA)
                    / self.altura_celula
                ))
            )

            for linha in range(lmin, lmax + 1):
                for coluna in range(cmin, cmax + 1):
                    self.celulas[linha][coluna].append(
                        indice
                    )

    def consultar(self, ponto):
        if self.localizar_celula(ponto) is None:
            return []

        cmin = max(
            0,
            int(math.floor(
                (ponto.x - TOLERANCIA)
                / self.largura_celula
            ))
        )

        cmax = min(
            self.colunas - 1,
            int(math.floor(
                (ponto.x + TOLERANCIA)
                / self.largura_celula
            ))
        )

        lmin = max(
            0,
            int(math.floor(
                (ponto.y - TOLERANCIA)
                / self.altura_celula
            ))
        )

        lmax = min(
            self.linhas - 1,
            int(math.floor(
                (ponto.y + TOLERANCIA)
                / self.altura_celula
            ))
        )

        candidatos = set()

        for linha in range(lmin, lmax + 1):
            for coluna in range(cmin, cmax + 1):
                candidatos.update(
                    self.celulas[linha][coluna]
                )

        return sorted(candidatos)

    def total_referencias(self):
        return sum(
            len(celula)
            for linha in self.celulas
            for celula in linha
        )
