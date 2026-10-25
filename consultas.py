
from dataclasses import dataclass, field
from time import perf_counter_ns

from algoritmos import ponto_no_triangulo
from grade import GradeUniforme


@dataclass
class ResultadoConsulta:
    candidatos_subdivisao: list = field(
        default_factory=list
    )

    candidatos_envelope: list = field(
        default_factory=list
    )

    triangulos_contendo: list = field(
        default_factory=list
    )

    testes_detalhados: int = 0
    tempo_ns: int = 0


class Consultor:
    def __init__(self, cenario, colunas=10, linhas=10):
        self.cenario = cenario

        self.tempo_construcao_ns = 0

        self.definir_grade(colunas, linhas)

    def definir_grade(self, colunas, linhas):
        inicio = perf_counter_ns()

        self.grade = GradeUniforme(
            self.cenario,
            colunas,
            linhas
        )

        self.tempo_construcao_ns = (
            perf_counter_ns() - inicio
        )

    def consultar(
        self,
        ponto,
        usar_envelope=True,
        usar_subdivisao=False
    ):
        inicio = perf_counter_ns()

        resultado = ResultadoConsulta()

        if usar_subdivisao:
            indices = self.grade.consultar(ponto)
        else:
            indices = list(
                range(len(self.cenario.triangulos))
            )

        resultado.candidatos_subdivisao = indices

        for indice in indices:
            triangulo = self.cenario.triangulos[indice]

            if usar_envelope:
                if not triangulo.envelope.contem(ponto):
                    continue

            resultado.candidatos_envelope.append(
                indice
            )

            resultado.testes_detalhados += 1

            if ponto_no_triangulo(ponto, triangulo):
                resultado.triangulos_contendo.append(
                    indice
                )

        resultado.tempo_ns = (
            perf_counter_ns() - inicio
        )

        return resultado
