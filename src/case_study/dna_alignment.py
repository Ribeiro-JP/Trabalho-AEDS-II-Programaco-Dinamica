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
    m, n = len(a), len(b)
    
    # Cria a matriz D com dimensões (m + 1) x (n + 1)
    D = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Casos base: D[i, 0] = i e D[0, j] = j
    for i in range(m + 1):
        D[i][0] = i
    for j in range(n + 1):
        D[0][j] = j
        
    # Preenchimento da matriz por programação dinâmica
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                D[i][j] = D[i - 1][j - 1]
            else:
                D[i][j] = 1 + min(
                    D[i - 1][j],      # Remoção de a[i-1]
                    D[i][j - 1],      # Inserção de b[j-1]
                    D[i - 1][j - 1]   # Substituição
                )
                
    return D[m][n]


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
    m, n = len(a), len(b)
    
    # 1. Computação da matriz de distâncias (idêntica ao edit_distance)
    D = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m + 1):
        D[i][0] = i
    for j in range(n + 1):
        D[0][j] = j
        
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                D[i][j] = D[i - 1][j - 1]
            else:
                D[i][j] = 1 + min(D[i - 1][j], D[i][j - 1], D[i - 1][j - 1])
                
    # Salva a distância final calculada
    distance = D[m][n]
    
    # 2. Traceback para reconstruir o alinhamento ótimo
    aligned_a = []
    aligned_b = []
    i, j = m, n
    
    while i > 0 or j > 0:
        # Se chegamos ao topo, o resto são inserções (gaps em A)
        if i == 0:
            aligned_a.append('-')
            aligned_b.append(b[j - 1])
            j -= 1
        # Se chegamos à esquerda, o resto são deleções (gaps em B)
        elif j == 0:
            aligned_a.append(a[i - 1])
            aligned_b.append('-')
            i -= 1
        # Se os caracteres casam, movemos na diagonal
        elif a[i - 1] == b[j - 1]:
            aligned_a.append(a[i - 1])
            aligned_b.append(b[j - 1])
            i -= 1
            j -= 1
        # Se diferem, descobrimos de qual vizinho veio o valor mínimo obtido
        else:
            current_val = D[i][j]
            # Verifica se veio da Substituição (diagonal)
            if current_val == D[i - 1][j - 1] + 1:
                aligned_a.append(a[i - 1])
                aligned_b.append(b[j - 1])
                i -= 1
                j -= 1
            # Verifica se veio da Remoção (para cima -> gap em B)
            elif current_val == D[i - 1][j] + 1:
                aligned_a.append(a[i - 1])
                aligned_b.append('-')
                i -= 1
            # Verifica se veio da Inserção (para a esquerda -> gap em A)
            else:
                aligned_a.append('-')
                aligned_b.append(b[j - 1])
                j -= 1
                
    # Como o traceback reconstrói as strings de trás para frente, invertemos os resultados
    aligned_a.reverse()
    aligned_b.reverse()
    
    return "".join(aligned_a), "".join(aligned_b), distance



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
