
from cenario import Cenario
from consultas import Consultor
from geometry.geometria import Ponto


cenario = Cenario(800, 600)
cenario.gerar_triangulos(
    quantidade=100,
    semente=42
)

consultor = Consultor(cenario)

pontos = [
    Ponto(100, 100),
    Ponto(400, 300),
    Ponto(600, 450),
    Ponto(0, 0),
    Ponto(800, 600)
]

modos = [
    ("Forca bruta", False, False),
    ("AABB", True, False),
    ("Grade", False, True),
    ("Grade + AABB", True, True)
]

for ponto in pontos:
    print(f"\nPonto: {ponto}")

    referencia = None

    for nome, envelope, subdivisao in modos:
        resultado = consultor.consultar(
            ponto,
            usar_envelope=envelope,
            usar_subdivisao=subdivisao
        )

        encontrados = set(
            resultado.triangulos_contendo
        )

        if referencia is None:
            referencia = encontrados

        assert encontrados == referencia, (
            f"Resultados diferentes no modo {nome}"
        )

        print(
            f"{nome}: "
            f"Subdivisao="
            f"{len(resultado.candidatos_subdivisao)}, "
            f"AABB="
            f"{len(resultado.candidatos_envelope)}, "
            f"Detalhados={resultado.testes_detalhados}, "
            f"Encontrados={len(encontrados)}, "
            f"Tempo={resultado.tempo_ns / 1000:.2f} us"
        )

print("\nTodos os modos retornaram os mesmos resultados!")
