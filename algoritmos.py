from geometry.geometria import Ponto, Triangulo

def orientacao(a: Ponto, b: Ponto, p: Ponto) -> float:
    return (
        (b.x - a.x) * (p.y - a.y)
        - (b.y - a.y) * (p.x - a.x)
    )


def ponto_no_triangulo(
    ponto: Ponto,
    triangulo: Triangulo,
    tolerancia: float = 1e-9
) -> bool:

    a = triangulo.a
    b = triangulo.b
    c = triangulo.c

    # Tolerância proporcional à escala do triângulo
    escala = max(
        abs(a.x - b.x), abs(a.y - b.y),
        abs(b.x - c.x), abs(b.y - c.y),
        abs(c.x - a.x), abs(c.y - a.y)
    )

    if escala == 0:
        return False

    eps = tolerancia * escala * escala

    # Ignora triângulos degenerados
    if abs(orientacao(a, b, c)) <= eps:
        return False

    d1 = orientacao(a, b, ponto)
    d2 = orientacao(b, c, ponto)
    d3 = orientacao(c, a, ponto)

    tem_negativo = d1 < -eps or d2 < -eps or d3 < -eps
    tem_positivo = d1 > eps or d2 > eps or d3 > eps

    return not (tem_negativo and tem_positivo)
