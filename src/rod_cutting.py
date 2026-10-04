"""Problema do Corte de Hastes (Rod Cutting) - Cormen Seção 15.1.

Dada uma haste de comprimento n e uma tabela de preços p[1..n], determinar
a receita máxima r_n obtida cortando a haste em pedaços inteiros e vendendo-os.

Recorrência fundamental:
    r_0 = 0
    r_n = max_{1 <= i <= n} (p[i] + r_{n-i}), para n >= 1
"""

from __future__ import annotations

from src.common import CallCounter

# Preços de referência do livro do Cormen (índice 0 é 0 para alinhar com o tamanho)
PRICES_CORMEN: list[int] = [0, 1, 5, 8, 9, 10, 17, 17, 20, 24, 30]


def cut_rod_naive(p: list[int], n: int, counter: CallCounter | None = None) -> int:
    """Resolve o corte de haste por recursão ingênua sem memoização.

    Complexidade:
        Tempo: Theta(2^n) devido à árvore de recursão com 2^(n-1) folhas.
        Espaço: O(n) da pilha de recursão.

    Args:
        p: Vetor de preços onde p[i] é o valor de uma haste de tamanho i.
        n: Comprimento total da haste inicial.
        counter: Instância opcional de CallCounter para registrar invocações.

    Returns:
        A receita máxima obtida para uma haste de tamanho n.
    """
    raise NotImplementedError("TODO(P3): Implementar cut_rod_naive")


def cut_rod_memo(p: list[int], n: int, counter: CallCounter | None = None) -> int:
    """Resolve o corte de haste com recursão e memoização (Top-Down).

    Guarda os valores ótimos r[0..n] em um vetor de resultados conhecidos.

    Complexidade:
        Tempo: Theta(n^2).
        Espaço: Theta(n) para a tabela de memoização e pilha de chamadas.

    Args:
        p: Vetor de preços onde p[i] é o valor de uma haste de tamanho i.
        n: Comprimento total da haste inicial.
        counter: Instância opcional de CallCounter para registrar invocações.

    Returns:
        A receita máxima obtida para uma haste de tamanho n.
    """
    raise NotImplementedError("TODO(P3): Implementar cut_rod_memo")


def cut_rod_bottom_up(p: list[int], n: int) -> int:
    """Resolve o corte de haste iterativamente de baixo para cima (Bottom-Up).

    Preenche a tabela r[0..n] ordenando subproblemas pelo comprimento j (1..n).

    Complexidade:
        Tempo: Theta(n^2).
        Espaço: Theta(n) para a tabela de resultados.

    Args:
        p: Vetor de preços onde p[i] é o valor de uma haste de tamanho i.
        n: Comprimento total da haste inicial.

    Returns:
        A receita máxima obtida para uma haste de tamanho n.
    """
    raise NotImplementedError("TODO(P3): Implementar cut_rod_bottom_up")


def cut_rod_extended(p: list[int], n: int) -> tuple[int, list[int]]:
    """Versão estendida do corte de haste (Extended-Bottom-Up-Cut-Rod do Cormen).

    Retorna tanto a receita máxima quanto o vetor 's' de tamanhos do primeiro
    pedaço ótimo cortado para cada subproblema j de 1 a n.

    Complexidade:
        Tempo: Theta(n^2).
        Espaço: Theta(n) para as tabelas r e s.

    Args:
        p: Vetor de preços onde p[i] é o valor de uma haste de tamanho i.
        n: Comprimento total da haste inicial.

    Returns:
        Uma tupla (receita_maxima, s), onde s[j] é o tamanho do primeiro corte ótimo
        para uma haste de comprimento j.
    """
    raise NotImplementedError("TODO(P3): Implementar cut_rod_extended")


def reconstruct_cuts(s: list[int], n: int) -> list[int]:
    """Reconstrói a lista de pedaços que compõem o corte ótimo a partir do vetor s.

    Args:
        s: Vetor de escolhas ótimas gerado por `cut_rod_extended`.
        n: Comprimento original da haste.

    Returns:
        Lista com os comprimentos de cada pedaço cortado na solução ótima.
    """
    raise NotImplementedError("TODO(P3): Implementar reconstruct_cuts")


def cut_rod_greedy_ratio(p: list[int], n: int) -> tuple[int, list[int]]:
    """Heurística gulosa para o corte de hastes baseada na razão densidade de valor (p[i] / i).

    Escolhe repetidamente o pedaço com a maior razão preço por centímetro que
    ainda caiba no comprimento restante. Usado para demonstrar que abordagens
    gulosas falham com frequência neste problema.

    Complexidade:
        Tempo: O(n log n) ou O(n^2).
        Espaço: O(n).

    Args:
        p: Vetor de preços onde p[i] é o valor de uma haste de tamanho i.
        n: Comprimento total da haste inicial.

    Returns:
        Tupla (receita_obtida, pedacos_escolhidos).
    """
    raise NotImplementedError("TODO(P3): Implementar cut_rod_greedy_ratio")
