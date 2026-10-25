
import csv
import random
import statistics

from cenario import Cenario
from consultas import Consultor
from geometry.geometria import Ponto


MODOS = [
    ("Forca bruta", False, False),
    ("AABB", True, False),
    ("Grade", False, True),
    ("Grade + AABB", True, True)
]

QUANTIDADES = [100, 500, 1000]
SEMENTES = [42, 99]

TAMANHOS = [
    (20, 40),
    (60, 120)
]

DIVISOES = [5, 10, 20]
REPETICOES = 20


def executar():
    resultados = []
    construcao = []

    for quantidade in QUANTIDADES:
        for semente in SEMENTES:
            for tamanho_min, tamanho_max in TAMANHOS:

                cenario = Cenario()

                cenario.gerar_triangulos(
                    quantidade=quantidade,
                    semente=semente,
                    tamanho_min=tamanho_min,
                    tamanho_max=tamanho_max
                )

                gerador = random.Random(12345)

                pontos = [
                    Ponto(
                        gerador.uniform(0, 800),
                        gerador.uniform(0, 600)
                    )
                    for _ in range(10)
                ]

                pontos.extend([
                    Ponto(0, 0),
                    Ponto(400, 300),
                    Ponto(800, 600)
                ])

                for divisao in DIVISOES:
                    tempos_construcao = []

                    # Mede a construcao varias vezes
                    for _ in range(REPETICOES):
                        consultor = Consultor(
                            cenario,
                            colunas=divisao,
                            linhas=divisao
                        )

                        tempos_construcao.append(
                            consultor.tempo_construcao_ns / 1000
                        )

                    construcao.append({
                        "quantidade": quantidade,
                        "semente": semente,
                        "tamanho_min": tamanho_min,
                        "tamanho_max": tamanho_max,
                        "divisao": divisao,
                        "referencias":
                            consultor.grade.total_referencias(),
                        "tempo_construcao_mediano_us":
                            round(
                                statistics.median(
                                    tempos_construcao
                                ),
                                4
                            )
                    })

                    for indice_ponto, ponto in enumerate(pontos):
                        referencia = None

                        for nome, envelope, grade in MODOS:
                            tempos = []
                            resultado = None

                            for _ in range(REPETICOES):
                                resultado = consultor.consultar(
                                    ponto,
                                    usar_envelope=envelope,
                                    usar_subdivisao=grade
                                )

                                tempos.append(
                                    resultado.tempo_ns / 1000
                                )

                            encontrados = set(
                                resultado.triangulos_contendo
                            )

                            if referencia is None:
                                referencia = encontrados

                            assert encontrados == referencia, (
                                "Resultados divergentes: "
                                f"N={quantidade}, "
                                f"semente={semente}, "
                                f"grade={divisao}, "
                                f"ponto={indice_ponto}, "
                                f"modo={nome}"
                            )

                            resultados.append({
                                "quantidade": quantidade,
                                "semente": semente,
                                "tamanho_min": tamanho_min,
                                "tamanho_max": tamanho_max,
                                "divisao": divisao,
                                "ponto": indice_ponto,
                                "x": round(ponto.x, 4),
                                "y": round(ponto.y, 4),
                                "modo": nome,
                                "candidatos_grade": len(
                                    resultado.candidatos_subdivisao
                                ),
                                "candidatos_aabb": len(
                                    resultado.candidatos_envelope
                                ),
                                "testes_detalhados":
                                    resultado.testes_detalhados,
                                "encontrados": len(encontrados),
                                "tempo_mediano_us": round(
                                    statistics.median(tempos),
                                    4
                                )
                            })

                    print(
                        f"Concluido: N={quantidade}, "
                        f"semente={semente}, "
                        f"tamanho={tamanho_min}-{tamanho_max}, "
                        f"grade={divisao}x{divisao}"
                    )

    arquivos = [
        ("resultados_experimentos.csv", resultados),
        ("resultados_construcao.csv", construcao)
    ]

    for nome, linhas in arquivos:
        with open(
            nome,
            "w",
            newline="",
            encoding="utf-8"
        ) as arquivo:
            escritor = csv.DictWriter(
                arquivo,
                fieldnames=linhas[0].keys()
            )

            escritor.writeheader()
            escritor.writerows(linhas)

    print("\nExperimentos concluidos!")
    print(f"Registros de consultas: {len(resultados)}")
    print(f"Registros de construcao: {len(construcao)}")


if __name__ == "__main__":
    executar()
