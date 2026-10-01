from geometry.triangulo import Ponto, Triangulo


def main():
    pontoA = Ponto(0, 0)
    pontoB = Ponto(5, 0)
    pontoC = Ponto(0, 5)

    triangulo1 = Triangulo(pontoA, pontoB, pontoC)

    print(triangulo1)

if __name__ == '__main__':
    main()