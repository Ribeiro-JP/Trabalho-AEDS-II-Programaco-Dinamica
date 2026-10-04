"""Subsequência Comum Máxima (Longest Common Subsequence - LCS) - Cormen Seção 15.4.

Dadas duas sequências X = <x_1, ..., x_m> e Y = <y_1, ..., y_n>, encontrar o comprimento
e os elementos de uma subsequência comum de comprimento máximo.

Recorrência fundamental:
    c[i, j] = 0, se i == 0 ou j == 0
    c[i, j] = c[i-1, j-1] + 1, se i, j > 0 e x_i == y_j
    c[i, j] = max(c[i-1, j], c[i, j-1]), se i, j > 0 e x_i != y_j

A tabela b[i, j] armazena as direções ('diag' / 'up' / 'left' ou setas '↖', '↑', '←')
para a reconstrução da solução ótima.
"""

from __future__ import annotations

from src.common import CallCounter


def lcs_naive(x: str, y: str, counter: CallCounter | None = None) -> int:
    """Calcula o comprimento da LCS usando recursão ingênua sem memoização.

    Complexidade:
        Tempo: O(2^(m+n)) no pior caso (quando nenhum caractere coincide).
        Espaço: O(m + n) na pilha de chamadas.

    Args:
        x: Primeira cadeia de caracteres.
        y: Segunda cadeia de caracteres.
        counter: Instância opcional de CallCounter para registrar invocações.

    Returns:
        O comprimento da maior subsequência comum.
    """
    raise NotImplementedError("TODO(P3): Implementar lcs_naive")


def lcs_memo(x: str, y: str) -> int:
    """Calcula o comprimento da LCS usando recursão com memoização (Top-Down).

    Complexidade:
        Tempo: Theta(m * n).
        Espaço: Theta(m * n) para o cache e O(m + n) de pilha.

    Args:
        x: Primeira cadeia de caracteres.
        y: Segunda cadeia de caracteres.

    Returns:
        O comprimento da maior subsequência comum.
    """
    raise NotImplementedError("TODO(P3): Implementar lcs_memo")


def lcs_table(x: str, y: str) -> tuple[list[list[int]], list[list[str]]]:
    """Preenche as tabelas de comprimentos c e de direções b (LCS-Length do Cormen).

    Complexidade:
        Tempo: Theta(m * n).
        Espaço: Theta(m * n) para as duas matrizes (m+1) x (n+1).

    Args:
        x: Primeira cadeia de caracteres (tamanho m).
        y: Segunda cadeia de caracteres (tamanho n).

    Returns:
        Tupla (c, b), onde:
            - c: Matriz (m+1) x (n+1) de comprimentos acumulados.
            - b: Matriz (m+1) x (n+1) de direções de traceback ('diag', 'up', 'left').
    """
    raise NotImplementedError("TODO(P3): Implementar lcs_table")


def lcs_string(x: str, y: str) -> str:
    """Retorna uma subsequência comum máxima em formato de texto.

    Reconstrói a sequência realizando o traceback na tabela de direções ou
    diretamente na tabela de comprimentos.

    Complexidade:
        Tempo: Theta(m * n) para construir a tabela + O(m + n) para o traceback.
        Espaço: Theta(m * n).

    Args:
        x: Primeira cadeia de caracteres.
        y: Segunda cadeia de caracteres.

    Returns:
        Uma string contendo os caracteres da LCS encontrada.
    """
    raise NotImplementedError("TODO(P3): Implementar lcs_string")


def lcs_length_two_rows(x: str, y: str) -> int:
    """Calcula o comprimento da LCS utilizando apenas duas linhas da tabela (otimização de espaço).

    Como o cálculo de c[i, j] depende exclusivamente da linha atual (i) e da
    linha anterior (i-1), descarta as linhas anteriores para economizar memória.

    Complexidade:
        Tempo: Theta(m * n).
        Espaço: Theta(min(m, n)) mantendo a menor string como largura de linha.

    Args:
        x: Primeira cadeia de caracteres.
        y: Segunda cadeia de caracteres.

    Returns:
        O comprimento da maior subsequência comum.
    """
    raise NotImplementedError("TODO(P3): Implementar lcs_length_two_rows")


def format_table(c: list[list[int]], x: str, y: str) -> str:
    """Formata a tabela de programação dinâmica c como uma grade de texto legível.

    Args:
        c: Matriz de dimensões (len(x)+1) x (len(y)+1) com os comprimentos calculados.
        x: Primeira sequência utilizada nos índices das linhas.
        y: Segunda sequência utilizada nos índices das colunas.

    Returns:
        String contendo a tabela tabulada com cabeçalhos de linhas e colunas.
    """
    raise NotImplementedError("TODO(P3): Implementar format_table")
