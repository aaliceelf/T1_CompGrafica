
from geometry.geometria import Ponto, Triangulo, TOLERANCIA


def orientacao(a: Ponto, b: Ponto, p: Ponto) -> float:
    return (
        (b.x - a.x) * (p.y - a.y)
        - (b.y - a.y) * (p.x - a.x)
    )


def ponto_no_triangulo(
    ponto: Ponto,
    triangulo: Triangulo,
    tolerancia: float = TOLERANCIA
) -> bool:

    a = triangulo.a
    b = triangulo.b
    c = triangulo.c

    area2 = orientacao(a, b, c)

    if area2 == 0:
        return False

    arestas = [
        (a, b),
        (b, c),
        (c, a)
    ]

    sinal = 1 if area2 > 0 else -1

    for u, v in arestas:
        comprimento = (
            (v.x - u.x)**2
            + (v.y - u.y)**2
        )**0.5

        if comprimento == 0:
            return False

        if (
            sinal * orientacao(u, v, ponto)
            < -tolerancia * comprimento
        ):
            return False

    return True
