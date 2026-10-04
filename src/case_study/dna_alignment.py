"""Estudo de caso 2: Alinhamento de sequências biológicas e distância de edição.

Aplica o algoritmo de Needleman-Wunsch / Levenshtein para calcular a distância
de edição e o alinhamento global ótimo entre duas cadeias de nucleotídeos (DNA).
"""

from __future__ import annotations

import argparse
import sys


def edit_distance(a: str, b: str) -> int:
    """Calcula a distância mínima de edição (Levenshtein) entre duas sequências.

    Operações permitidas: inserção, remoção e substituição de caracteres (custo unitário).

    Recorrência:
        D[i, 0] = i
        D[0, j] = j
        D[i, j] = D[i-1, j-1] se a[i] == b[j]
        D[i, j] = 1 + min(D[i-1, j], D[i, j-1], D[i-1, j-1]) se a[i] != b[j]

    Complexidade:
        Tempo: Theta(len(a) * len(b)).
        Espaço: Theta(len(a) * len(b)).

    Args:
        a: Primeira sequência de caracteres (ex.: fita de DNA).
        b: Segunda sequência de caracteres.

    Returns:
        Número mínimo de operações para transformar 'a' em 'b'.
    """
    raise NotImplementedError("TODO(P4): Implementar edit_distance")


def align(a: str, b: str) -> tuple[str, str, int]:
    """Realiza o alinhamento global ótimo entre duas sequências de DNA.

    Utiliza a matriz de programação dinâmica para efetuar o traceback, inserindo
    gaps ('-') onde for necessária uma inserção ou deleção.

    Complexidade:
        Tempo: Theta(len(a) * len(b)) para computação + O(len(a) + len(b)) traceback.
        Espaço: Theta(len(a) * len(b)).

    Args:
        a: Primeira sequência de DNA (ex.: 'ACGTACGTTAGC').
        b: Segunda sequência de DNA (ex.: 'ACGTAGCTTAGC').

    Returns:
        Tupla (alinhamento_a, alinhamento_b, score_ou_distancia), onde as strings
        possuem o mesmo comprimento preenchidas com '-' nos gaps.
    """
    raise NotImplementedError("TODO(P4): Implementar align com traceback")


def _read_fasta_sequence(filepath: str) -> str:
    """Lê um arquivo FASTA simples e extrai a sequência de nucleotídeos."""
    lines: list[str] = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if not stripped.startswith(">"):
                lines.append(stripped.upper())
    return "".join(lines)


def main() -> None:
    """Ponto de entrada de linha de comando para o alinhador de DNA."""
    parser = argparse.ArgumentParser(
        description="Alinhador de DNA e distância de edição via Programação Dinâmica."
    )
    parser.add_argument("fasta_a", help="Caminho para o primeiro arquivo FASTA")
    parser.add_argument("fasta_b", help="Caminho para o segundo arquivo FASTA")
    args = parser.parse_args()

    try:
        seq_a = _read_fasta_sequence(args.fasta_a)
        seq_b = _read_fasta_sequence(args.fasta_b)
    except OSError as err:
        sys.exit(f"Erro ao ler arquivos FASTA: {err}")

    dist = edit_distance(seq_a, seq_b)
    aligned_a, aligned_b, score = align(seq_a, seq_b)

    print(f"Distância de Edição: {dist}")
    print(f"Score do Alinhamento: {score}")
    print("Alinhamento Ótimo:")
    print(f"Seq A: {aligned_a}")
    print(f"Seq B: {aligned_b}")


if __name__ == "__main__":
    main()
