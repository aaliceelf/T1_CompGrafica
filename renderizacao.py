import glfw

from OpenGL.GL import *
from OpenGL.GLU import *

from consultas import Consultor
from geometry.geometria import Ponto


class Renderizador:
    def __init__(self, cenario):
        self.cenario = cenario
        self.janela = None

        self.ponto = Ponto(
            cenario.largura / 2,
            cenario.altura / 2
        )

        self.consultor = Consultor(cenario)

        # Modos:
        # 1 = Forca bruta
        # 2 = AABB
        # 3 = Grade
        # 4 = Grade + AABB
        self.modo = 4

        # Opcoes visuais
        self.mostrar_grade = True
        self.mostrar_envelopes = False
        self.mostrar_candidatos = True

        self.resultado = None
        self.atualizar_consulta()

    def configuracao(self):
        usar_envelope = self.modo in (2, 4)
        usar_grade = self.modo in (3, 4)

        return usar_envelope, usar_grade

    def atualizar_consulta(self):
        envelope, grade = self.configuracao()

        self.resultado = self.consultor.consultar(
            self.ponto,
            usar_envelope=envelope,
            usar_subdivisao=grade
        )

        if self.janela is not None:
            self.atualizar_titulo()
            self.exibir_desempenho()

    def atualizar_titulo(self):
        nomes = {
            1: "Forca bruta",
            2: "AABB",
            3: "Grade",
            4: "Grade + AABB"
        }

        glfw.set_window_title(
            self.janela,
            f"Modo {self.modo}: {nomes[self.modo]} | "
            f"Ponto ({self.ponto.x:.1f}, "
            f"{self.ponto.y:.1f}) | "
            f"G: Grade | E: Envelopes | "
            f"C: Candidatos | +/-: Resolucao"
        )

    def exibir_desempenho(self):
        r = self.resultado

        print(
            f"\rModo {self.modo} | "
            f"Total: {len(self.cenario.triangulos)} | "
            f"Grade: {len(r.candidatos_subdivisao)} | "
            f"AABB: {len(r.candidatos_envelope)} | "
            f"Detalhados: {r.testes_detalhados} | "
            f"Encontrados: {len(r.triangulos_contendo)} | "
            f"Consulta: {r.tempo_ns / 1000:.2f} us | "
            f"Construcao grade: "
            f"{self.consultor.tempo_construcao_ns / 1000:.1f} us | "
            f"Referencias: "
            f"{self.consultor.grade.total_referencias()}",
            end="\n",
            flush=True
        )

    def movimentar_mouse(self, janela, x, y):
        largura, altura = glfw.get_window_size(janela)

        if largura <= 0 or altura <= 0:
            return

        x_cenario = (
            x * self.cenario.largura / largura
        )

        y_cenario = (
            self.cenario.altura
            - y * self.cenario.altura / altura
        )

        x_cenario = max(
            0, min(self.cenario.largura, x_cenario)
        )

        y_cenario = max(
            0, min(self.cenario.altura, y_cenario)
        )

        self.ponto = Ponto(
            x_cenario,
            y_cenario
        )

        self.atualizar_consulta()

    def controlar_teclado(
        self, janela, tecla, scancode, acao, mods
    ):
        if acao != glfw.PRESS:
            return

        # Alterna entre os quatro modos
        if glfw.KEY_1 <= tecla <= glfw.KEY_4:
            self.modo = tecla - glfw.KEY_1 + 1
            self.atualizar_consulta()

        elif tecla == glfw.KEY_G:
            self.mostrar_grade = not self.mostrar_grade

        elif tecla == glfw.KEY_E:
            self.mostrar_envelopes = (
                not self.mostrar_envelopes
            )

        elif tecla == glfw.KEY_C:
            self.mostrar_candidatos = (
                not self.mostrar_candidatos
            )

        # Aumenta ou diminui as divisoes da grade
        elif tecla in (
            glfw.KEY_EQUAL,
            glfw.KEY_KP_ADD,
            glfw.KEY_MINUS,
            glfw.KEY_KP_SUBTRACT
        ):
            atual = self.consultor.grade.colunas

            if tecla in (
                glfw.KEY_EQUAL,
                glfw.KEY_KP_ADD
            ):
                novo = min(80, atual + 5)

            else:
                novo = max(5, atual - 5)

            self.consultor.definir_grade(
                novo, novo
            )

            self.atualizar_consulta()

        elif tecla == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(
                janela, True
            )

    @staticmethod
    def desenhar_retangulo(
        envelope, cor, largura=1
    ):
        xmin, ymin, xmax, ymax = envelope

        glColor3f(*cor)
        glLineWidth(largura)

        glBegin(GL_LINE_LOOP)
        glVertex2f(xmin, ymin)
        glVertex2f(xmax, ymin)
        glVertex2f(xmax, ymax)
        glVertex2f(xmin, ymax)
        glEnd()

        glLineWidth(1)

    def desenhar_triangulos(self):
        usar_envelope, usar_grade = self.configuracao()

        candidatos_grade = set(
            self.resultado.candidatos_subdivisao
        )

        candidatos_aabb = set(
            self.resultado.candidatos_envelope
        )

        encontrados = set(
            self.resultado.triangulos_contendo
        )

        for indice, triangulo in enumerate(
            self.cenario.triangulos
        ):
            if indice in encontrados:
                # Verde: contem o ponto
                cor = (0.1, 0.8, 0.3)

            elif (
                self.mostrar_candidatos
                and usar_envelope
                and indice in candidatos_aabb
            ):
                # Amarelo: aprovado no envelope
                cor = (0.95, 0.7, 0.15)

            elif (
                self.mostrar_candidatos
                and usar_grade
                and indice in candidatos_grade
            ):
                # Roxo: candidato da grade
                cor = (0.65, 0.35, 0.9)

            else:
                # Azul: demais triangulos
                cor = (0.3, 0.5, 0.8)

            glColor3f(*cor)

            glBegin(GL_TRIANGLES)
            for ponto in (
                triangulo.a,
                triangulo.b,
                triangulo.c
            ):
                glVertex2f(ponto.x, ponto.y)
            glEnd()

            # Contorno
            glColor3f(0.85, 0.85, 0.85)

            glBegin(GL_LINE_LOOP)
            for ponto in (
                triangulo.a,
                triangulo.b,
                triangulo.c
            ):
                glVertex2f(ponto.x, ponto.y)
            glEnd()

    def desenhar_envelopes(self):
        for triangulo in self.cenario.triangulos:
            e = triangulo.envelope

            self.desenhar_retangulo(
                (e.xmin, e.ymin, e.xmax, e.ymax),
                (1, 0.85, 0.15)
            )

    def desenhar_grade_uniforme(self):
        grade = self.consultor.grade

        glColor3f(0.35, 0.4, 0.5)

        glBegin(GL_LINES)

        # Linhas verticais
        for coluna in range(1, grade.colunas):
            x = coluna * grade.largura_celula

            glVertex2f(x, 0)
            glVertex2f(x, self.cenario.altura)

        # Linhas horizontais
        for linha in range(1, grade.linhas):
            y = linha * grade.altura_celula

            glVertex2f(0, y)
            glVertex2f(self.cenario.largura, y)

        glEnd()

        # Destaca a celula atual
        if self.configuracao()[1]:
            celula = grade.localizar_celula(
                self.ponto
            )

            if celula is not None:
                linha, coluna = celula

                xmin = coluna * grade.largura_celula
                ymin = linha * grade.altura_celula

                xmax = xmin + grade.largura_celula
                ymax = ymin + grade.altura_celula

                self.desenhar_retangulo(
                    (xmin, ymin, xmax, ymax),
                    (1, 0.85, 0.1),
                    largura=3
                )

    def desenhar(self):
        largura, altura = glfw.get_framebuffer_size(
            self.janela
        )

        if largura <= 0 or altura <= 0:
            return

        glViewport(0, 0, largura, altura)

        glClearColor(0.1, 0.12, 0.16, 1)
        glClear(GL_COLOR_BUFFER_BIT)

        self.desenhar_triangulos()

        if self.mostrar_envelopes:
            self.desenhar_envelopes()

        if self.mostrar_grade:
            self.desenhar_grade_uniforme()

        # Ponto vermelho
        glPointSize(9)
        glColor3f(1, 0.2, 0.2)

        glBegin(GL_POINTS)
        glVertex2f(self.ponto.x, self.ponto.y)
        glEnd()

    def iniciar(self):
        if not glfw.init():
            raise RuntimeError("GLFW nao iniciou")

        try:
            self.janela = glfw.create_window(
                self.cenario.largura,
                self.cenario.altura,
                "Inclusao de Ponto em Poligonos",
                None,
                None
            )

            if not self.janela:
                raise RuntimeError(
                    "Nao foi possivel criar a janela GLFW"
                )

            glfw.make_context_current(self.janela)
            glfw.swap_interval(1)

            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()

            gluOrtho2D(
                0, self.cenario.largura,
                0, self.cenario.altura
            )

            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()

            glfw.set_cursor_pos_callback(
                self.janela,
                self.movimentar_mouse
            )

            glfw.set_key_callback(
                self.janela,
                self.controlar_teclado
            )

            self.atualizar_titulo()
            self.exibir_desempenho()

            while not glfw.window_should_close(
                self.janela
            ):
                glfw.poll_events()
                self.desenhar()
                glfw.swap_buffers(self.janela)

        finally:
            glfw.terminate()
            print()
