from OpenGL.GL import *
from OpenGL.GLU import *
import glfw

from geometry.geometria import Ponto
from algoritmos import ponto_no_triangulo


class Renderizador:
    def __init__(self, cenario):
        self.cenario = cenario
        self.janela = None
        self.ponto = Ponto(
            cenario.largura / 2,
            cenario.altura / 2
        )

    def iniciar(self):
        if not glfw.init():
            raise RuntimeError("Erro ao inicializar GLFW")

        self.janela = glfw.create_window(
            self.cenario.largura,
            self.cenario.altura,
            "Inclusao de Ponto em Poligonos",
            None,
            None
        )

        if not self.janela:
            glfw.terminate()
            raise RuntimeError("Erro ao criar janela")

        glfw.make_context_current(self.janela)

        # Coordenadas do cenário: (0,0) no canto inferior esquerdo
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

        while not glfw.window_should_close(self.janela):
            glfw.poll_events()
            self.desenhar()
            glfw.swap_buffers(self.janela)

        glfw.terminate()

    def movimentar_mouse(self, janela, x, y):
        largura_janela, altura_janela = glfw.get_window_size(janela)

        if largura_janela == 0 or altura_janela == 0:
            return

        # Converte coordenadas da janela para o cenário
        x_cenario = x * self.cenario.largura / largura_janela
        y_cenario = (
            self.cenario.altura
            - y * self.cenario.altura / altura_janela
        )

        self.ponto = Ponto(x_cenario, y_cenario)

        glfw.set_window_title(
            janela,
            f"Ponto: ({x_cenario:.1f}, {y_cenario:.1f})"
        )

    def desenhar(self):
        glViewport(
            0, 0,
            *glfw.get_framebuffer_size(self.janela)
        )

        glClearColor(0.10, 0.12, 0.16, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        for triangulo in self.cenario.triangulos:
            dentro = ponto_no_triangulo(
                self.ponto, triangulo
            )

            if dentro:
                glColor3f(0.1, 0.8, 0.3)
            else:
                glColor3f(0.3, 0.5, 0.8)

            glBegin(GL_TRIANGLES)
            glVertex2f(triangulo.a.x, triangulo.a.y)
            glVertex2f(triangulo.b.x, triangulo.b.y)
            glVertex2f(triangulo.c.x, triangulo.c.y)
            glEnd()

            # Contorno do triângulo
            glColor3f(0.85, 0.85, 0.85)
            glBegin(GL_LINE_LOOP)
            glVertex2f(triangulo.a.x, triangulo.a.y)
            glVertex2f(triangulo.b.x, triangulo.b.y)
            glVertex2f(triangulo.c.x, triangulo.c.y)
            glEnd()

        # Desenha o ponto vermelho
        glPointSize(9)
        glColor3f(1.0, 0.2, 0.2)

        glBegin(GL_POINTS)
        glVertex2f(self.ponto.x, self.ponto.y)
        glEnd()
