import random
from geometry.geometria import Ponto, Triangulo


class Cenario:
    def __init__(self, largura=800, altura=600):
        self.largura = largura
        self.altura = altura
        self.triangulos = []
        self.semente = None

    def gerar_triangulos(self, quantidade, semente=42,
                         tamanho_min=20, tamanho_max=80):

        self.triangulos.clear()
        self.semente = semente

        gerador = random.Random(semente)

        for i in range(quantidade):
            # Centro do triângulo
            cx = gerador.uniform(0, self.largura)
            cy = gerador.uniform(0, self.altura)

            # Tamanho dos deslocamentos dos vértices
            tamanho = gerador.uniform(tamanho_min, tamanho_max)

            # Gera três vértices aleatórios próximos ao centro
            vertices = []

            for _ in range(3):
                x = cx + gerador.uniform(-tamanho, tamanho)
                y = cy + gerador.uniform(-tamanho, tamanho)

                x = max(0, min(x, self.largura))
                y = max(0, min(y, self.altura))

                vertices.append(Ponto(x, y))

            triangulo = Triangulo(
                id=i,
                a=vertices[0],
                b=vertices[1],
                c=vertices[2]
            )

            self.triangulos.append(triangulo)

    def quantidade_triangulos(self):
        return len(self.triangulos)
