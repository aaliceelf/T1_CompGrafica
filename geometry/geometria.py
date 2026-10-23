from dataclasses import dataclass, field

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

    def contem(self, ponto: Ponto, tolerancia=1e-9) -> bool:
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
            xmin=min(self.a.x, self.b.x, self.c.x),
            ymin=min(self.a.y, self.b.y, self.c.y),
            xmax=max(self.a.x, self.b.x, self.c.x),
            ymax=max(self.a.y, self.b.y, self.c.y)
        )
    