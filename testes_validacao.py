
import random

from cenario import Cenario
from consultas import Consultor
from geometry.geometria import Ponto, Triangulo


MODOS = (
    (False, False),
    (True, False),
    (False, True),
    (True, True)
)


def verificar(consultor, ponto, esperado=None):
    resultados = []

    for usar_envelope, usar_grade in MODOS:
        resultado = consultor.consultar(
            ponto,
            usar_envelope=usar_envelope,
            usar_subdivisao=usar_grade
        )

        resultados.append(
            set(resultado.triangulos_contendo)
        )

    assert all(
        resultado == resultados[0]
        for resultado in resultados
    ), (ponto, resultados)

    if esperado is not None:
        assert resultados[0] == esperado, (
            ponto,
            resultados[0],
            esperado
        )


def main():
    cenario = Cenario()

    # Dois triangulos sobrepostos
    cenario.triangulos = [
        Triangulo(
            0,
            Ponto(100, 100),
            Ponto(300, 100),
            Ponto(100, 300)
        ),
        Triangulo(
            1,
            Ponto(100, 100),
            Ponto(300, 100),
            Ponto(100, 300)
        )
    ]

    consultor = Consultor(cenario)

    casos = [
        (Ponto(150, 150), {0, 1}),
        (Ponto(100, 100), {0, 1}),
        (Ponto(200, 100), {0, 1}),
        (Ponto(300, 300), set()),
        (Ponto(0, 0), set()),
        (Ponto(200, 200), {0, 1}),
        (Ponto(200, 200 + 1e-10), {0, 1})
    ]

    for ponto, esperado in casos:
        verificar(
            consultor,
            ponto,
            esperado
        )

    print("Casos especiais: OK")

    contador = 0

    for semente in (42, 99, 123):
        cenario = Cenario()

        cenario.gerar_triangulos(
            quantidade=500,
            semente=semente
        )

        for divisao in (5, 10, 20):
            consultor = Consultor(
                cenario,
                colunas=divisao,
                linhas=divisao
            )

            gerador = random.Random(2026)

            pontos = [
                Ponto(
                    gerador.uniform(0, 800),
                    gerador.uniform(0, 600)
                )
                for _ in range(100)
            ]

            # Pontos sobre linhas da grade
            for i in range(divisao + 1):
                pontos.extend([
                    Ponto(
                        i * 800 / divisao,
                        300
                    ),
                    Ponto(
                        400,
                        i * 600 / divisao
                    )
                ])

            # Vertices e pontos medios de arestas
            for t in cenario.triangulos[:20]:
                pontos.extend([
                    t.a,
                    t.b,
                    t.c
                ])

                for a, b in (
                    (t.a, t.b),
                    (t.b, t.c),
                    (t.c, t.a)
                ):
                    pontos.append(
                        Ponto(
                            (a.x + b.x) / 2,
                            (a.y + b.y) / 2
                        )
                    )

            for ponto in pontos:
                verificar(consultor, ponto)
                contador += 1

    print(
        "Consultas aleatorias e de borda "
        f"validadas: {contador}"
    )

    print("Quatro modos consistentes!")


if __name__ == "__main__":
    main()
