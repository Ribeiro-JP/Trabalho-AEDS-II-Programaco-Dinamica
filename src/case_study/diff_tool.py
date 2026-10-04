"""Estudo de caso 1: Ferramenta de comparação textual (mini diff).

Aplica a Subsequência Comum Máxima (LCS) tratando linhas de arquivos de texto como
elementos de sequência, gerando saídas no padrão unificado (' ', '+', '-').
"""

from __future__ import annotations

import argparse
import sys


def diff_lines(a_lines: list[str], b_lines: list[str]) -> list[str]:
    """Calcula a diferença linha a linha entre dois conjuntos de linhas usando LCS.

    Compara duas listas de linhas e produz uma lista de linhas marcadas com:
        - "  " (dois espaços) para linhas presentes em ambos os textos (LCS).
        - "- " para linhas presentes apenas no primeiro texto (removidas).
        - "+ " para linhas presentes apenas no segundo texto (adicionadas).

    Complexidade:
        Tempo: Theta(len(a_lines) * len(b_lines)).
        Espaço: Theta(len(a_lines) * len(b_lines)).

    Args:
        a_lines: Lista de linhas da versão original do texto.
        b_lines: Lista de linhas da versão modificada do texto.

    Returns:
        Lista de strings formatadas com os prefixos de adição, remoção ou preservação.
    """
    raise NotImplementedError("TODO(P4): Implementar diff_lines usando LCS")


def main() -> None:
    """Ponto de entrada de linha de comando para a ferramenta de diff."""
    parser = argparse.ArgumentParser(
        description="Mini diff baseado em LCS (Estudo de Caso de Programação Dinâmica)."
    )
    parser.add_argument("file_a", help="Caminho para o primeiro arquivo de texto")
    parser.add_argument("file_b", help="Caminho para o segundo arquivo de texto")
    args = parser.parse_args()

    try:
        with open(args.file_a, "r", encoding="utf-8") as f:
            lines_a = f.readlines()
        with open(args.file_b, "r", encoding="utf-8") as f:
            lines_b = f.readlines()
    except OSError as err:
        sys.exit(f"Erro ao ler arquivos: {err}")

    diff_output = diff_lines(lines_a, lines_b)
    for line in diff_output:
        print(line, end="" if line.endswith("\n") else "\n")


if __name__ == "__main__":
    main()
