from dataclasses import dataclass

@dataclass
class Ponto:
    x: float
    y: float

@dataclass
class Triangulo:
    def __init__(self, p1: Ponto, p2:Ponto, p3:Ponto):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    