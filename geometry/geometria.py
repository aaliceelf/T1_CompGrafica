from dataclasses import dataclass, field

TOLERANCIA = 1e-9


@dataclass(frozen=True)
class Ponto:
    x: float
    y: float


@dataclass(frozen=True)
class Envelope:
    xmin: float
    ymin: float
    xmax: float
    ymax: float

    def contem(self, ponto: Ponto, tolerancia: float = TOLERANCIA) -> bool:
        return (
            self.xmin - tolerancia <= ponto.x <= self.xmax + tolerancia
            and self.ymin - tolerancia <= ponto.y <= self.ymax + tolerancia
        )


@dataclass
class Triangulo:
    id: int
    a: Ponto
    b: Ponto
    c: Ponto

    envelope: Envelope = field(init=False)

    def __post_init__(self):
        self.envelope = Envelope(
            min(self.a.x, self.b.x, self.c.x),
            min(self.a.y, self.b.y, self.c.y),
            max(self.a.x, self.b.x, self.c.x),
            max(self.a.y, self.b.y, self.c.y)
        )

    def area_dupla(self):
        return (
            (self.b.x - self.a.x) * (self.c.y - self.a.y)
            - (self.b.y - self.a.y) * (self.c.x - self.a.x)
        )
