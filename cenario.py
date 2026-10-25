
import csv
import random

from geometry.geometria import Ponto, Triangulo


class Cenario:
    def __init__(self, largura=800, altura=600):
        if largura <= 0 or altura <= 0:
            raise ValueError(
                "Dimensoes do cenario precisam ser positivas"
            )

        self.largura = largura
        self.altura = altura
        self.triangulos = []
        self.semente = None

    def gerar_triangulos(
        self,
        quantidade,
        semente=42,
        tamanho_min=20,
        tamanho_max=80
    ):
        if quantidade < 0 or not (0 < tamanho_min <= tamanho_max):
            raise ValueError(
                "Quantidade ou tamanhos invalidos"
            )

        gerador = random.Random(semente)
        triangulos = []

        for i in range(quantidade):
            for tentativa in range(1000):
                cx = gerador.uniform(0, self.largura)
                cy = gerador.uniform(0, self.altura)

                tamanho = gerador.uniform(
                    tamanho_min, tamanho_max
                )

                vertices = []

                for _ in range(3):
                    x = cx + gerador.uniform(
                        -tamanho, tamanho
                    )

                    y = cy + gerador.uniform(
                        -tamanho, tamanho
                    )

                    x = min(self.largura, max(0, x))
                    y = min(self.altura, max(0, y))

                    vertices.append(Ponto(x, y))

                triangulo = Triangulo(
                    i,
                    *vertices
                )

                # Evita triangulos de area praticamente zero
                if abs(triangulo.area_dupla()) > 1e-8:
                    triangulos.append(triangulo)
                    break
            else:
                raise RuntimeError(
                    f"Nao foi possivel gerar triangulo valido {i}"
                )

        self.triangulos = triangulos
        self.semente = semente

    def quantidade_triangulos(self):
        return len(self.triangulos)

    def carregar_csv(self, caminho):
        triangulos = []

        with open(
            caminho,
            newline="",
            encoding="utf-8"
        ) as arquivo:

            leitor = csv.DictReader(arquivo)

            for i, linha in enumerate(leitor):
                valores = [
                    float(linha[ch])
                    for ch in (
                        "ax", "ay",
                        "bx", "by",
                        "cx", "cy"
                    )
                ]

                triangulo = Triangulo(
                    i,
                    Ponto(*valores[:2]),
                    Ponto(*valores[2:4]),
                    Ponto(*valores[4:])
                )

                if abs(triangulo.area_dupla()) <= 1e-8:
                    raise ValueError(
                        f"Triangulo degenerado na linha {i + 2}"
                    )

                triangulos.append(triangulo)

        self.triangulos = triangulos
        self.semente = None
