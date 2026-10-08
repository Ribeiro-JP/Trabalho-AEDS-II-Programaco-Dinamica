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
    m = len(a_lines)
    n = len(b_lines)
    
    # 1. Construção da matriz LCS utilizando programação dinâmica
    # dp[i][j] guardará o comprimento do LCS entre a_lines[0:i] e b_lines[0:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a_lines[i - 1] == b_lines[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
                
    # 2. Backtracking para reconstruir o diff
    # Como começamos do final, o resultado será gerado de trás para frente
    result = []
    i, j = m, n
    
    while i > 0 or j > 0:
        if i > 0 and j > 0 and a_lines[i - 1] == b_lines[j - 1]:
            # Linha idêntica em ambos os arquivos
            result.append(f"  {a_lines[i - 1]}")
            i -= 1
            j -= 1
        elif j > 0 and (i == 0 or dp[i][j - 1] >= dp[i - 1][j]):
            # Linha adicionada no texto B
            result.append(f"+ {b_lines[j - 1]}")
            j -= 1
        else:
            # Linha removida do texto A
            result.append(f"- {a_lines[i - 1]}")
            i -= 1
            
    # Como o backtracking foi feito de trás para frente, invertemos a lista
    result.reverse()
    return result



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
