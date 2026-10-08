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

from .common import CallCounter


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

    def resolver(i: int, j: int) -> int:
        # Resolve o subproblema LCS(x[:i], y[:j]).
        if counter is not None:
            counter.increment()

        if i == 0 or j == 0:
            return 0

        if x[i - 1] == y[j - 1]:
            return resolver(i - 1, j - 1) + 1

        return max(resolver(i - 1, j), resolver(i, j - 1))

    return resolver(len(x), len(y))


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
    memory: dict[tuple[int, int], int] = {}

    def resolver(i: int, j: int) -> int:
        if i == 0 or j == 0:
            return 0

        if (i, j) in memory:
            return memory[(i, j)]

        if x[i - 1] == y[j - 1]:
            memory[(i, j)] = resolver(i - 1, j - 1) + 1
        else:
            memory[(i, j)] = max(resolver(i - 1, j), resolver(i, j - 1))

        return memory[(i, j)]

    return resolver(len(x), len(y))


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
    m, n = len(x), len(y)

    c = [[0] * (n + 1) for _ in range(m + 1)]
    b = [[""] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if x[i - 1] == y[j - 1]:
                c[i][j] = c[i - 1][j - 1] + 1
                b[i][j] = "diag"
            elif c[i - 1][j] >= c[i][j - 1]:
                c[i][j] = c[i - 1][j]
                b[i][j] = "up"
            else:
                c[i][j] = c[i][j - 1]
                b[i][j] = "left"

    return c, b


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
    _, b = lcs_table(x, y)

    i, j = len(x), len(y)
    caracteres = []

    while i > 0 and j > 0:
        if b[i][j] == "diag":
            caracteres.append(x[i - 1])
            i -= 1
            j -= 1
        elif b[i][j] == "up":
            i -= 1
        else:
            j -= 1

    # O traceback percorre do fim para o início, então inverte o resultado.
    return "".join(reversed(caracteres))


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
    # A LCS é simétrica: garante que y seja a menor cadeia (largura das linhas).
    if len(y) > len(x):
        x, y = y, x

    anterior = [0] * (len(y) + 1)

    for i in range(1, len(x) + 1):
        atual = [0] * (len(y) + 1)

        for j in range(1, len(y) + 1):
            if x[i - 1] == y[j - 1]:
                atual[j] = anterior[j - 1] + 1
            else:
                atual[j] = max(anterior[j], atual[j - 1])

        anterior = atual

    return anterior[len(y)]


def format_table(c: list[list[int]], x: str, y: str) -> str:
    """Formata a tabela de programação dinâmica c como uma grade de texto legível.

    Args:
        c: Matriz de dimensões (len(x)+1) x (len(y)+1) com os comprimentos calculados.
        x: Primeira sequência utilizada nos índices das linhas.
        y: Segunda sequência utilizada nos índices das colunas.

    Returns:
        String contendo a tabela tabulada com cabeçalhos de linhas e colunas.
    """
    largura = max(len(str(valor)) for linha in c for valor in linha)

    cabecalho_colunas = ["ε"] + list(y)
    rotulos_linhas = ["ε"] + list(x)

    linhas = ["  " + " ".join(rotulo.rjust(largura) for rotulo in cabecalho_colunas)]

    for rotulo, linha in zip(rotulos_linhas, c):
        valores = " ".join(str(valor).rjust(largura) for valor in linha)
        linhas.append(f"{rotulo} {valores}")

    return "\n".join(linhas)
