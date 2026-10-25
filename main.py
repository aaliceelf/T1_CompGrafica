
import argparse

from cenario import Cenario
from renderizacao import Renderizador


def main():
    parser = argparse.ArgumentParser(
        description="Inclusao de ponto em triangulos"
    )

    parser.add_argument(
        "--n", type=int, default=100
    )

    parser.add_argument(
        "--semente", type=int, default=42
    )

    parser.add_argument(
        "--min", type=float, default=20
    )

    parser.add_argument(
        "--max", type=float, default=80
    )

    parser.add_argument(
        "--arquivo",
        help="CSV de triangulos: ax,ay,bx,by,cx,cy"
    )

    args = parser.parse_args()

    cenario = Cenario(
        largura=800,
        altura=600
    )

    if args.arquivo:
        cenario.carregar_csv(args.arquivo)

    else:
        cenario.gerar_triangulos(
            quantidade=args.n,
            semente=args.semente,
            tamanho_min=args.min,
            tamanho_max=args.max
        )

    print(
        "Triangulos:", cenario.quantidade_triangulos(),
        "| Semente:", cenario.semente
    )

    renderizador = Renderizador(cenario)
    renderizador.iniciar()


if __name__ == "__main__":
    main()
