"""Problema da Mochila 0/1 (0/1 Knapsack) - Módulo Opcional.

Dado um conjunto de itens com pesos e valores, e uma mochila com capacidade máxima W,
determinar o subconjunto de itens com valor total máximo cujo peso não ultrapasse W.

Usado no projeto para ilustrar onde a Programação Dinâmica atinge complexidade
pseudo-polinomial O(n * W), dependente da magnitude numérica da entrada e não apenas
do seu tamanho em bits.

Recorrência fundamental:
    V[0, w] = 0, para todo 0 <= w <= W
    V[i, w] = V[i-1, w], se w_i > w
    V[i, w] = max(V[i-1, w], V[i-1, w - w_i] + v_i), se w_i <= w
"""

from __future__ import annotations


def knapsack_01(
    weights: list[int], values: list[int], W: int
) -> tuple[int, list[int]]:
    """Resolve o problema da mochila 0/1 retornando o valor máximo e os itens escolhidos.

    Complexidade:
        Tempo: O(n * W) onde n = len(weights) e W é a capacidade (pseudo-polinomial).
        Espaço: O(n * W) para a matriz de programação dinâmica.

    Args:
        weights: Lista com os pesos de cada item (1-indexados conceitualmente).
        values: Lista com os valores de cada item.
        W: Capacidade máxima suportada pela mochila.

    Returns:
        Tupla (valor_maximo, indices_itens_selecionados).
    """
    raise NotImplementedError("TODO(P3): Implementar knapsack_01")


def knapsack_one_row(weights: list[int], values: list[int], W: int) -> int:
    """Calcula apenas o valor máximo da mochila usando um único vetor de tamanho W + 1.

    Itera as capacidades de trás para frente (W descendo até w_i) para reutilizar
    apenas os estados da linha anterior sem sobrescrever antecipadamente.

    Complexidade:
        Tempo: O(n * W).
        Espaço: O(W).

    Args:
        weights: Lista com os pesos de cada item.
        values: Lista com os valores de cada item.
        W: Capacidade máxima suportada pela mochila.

    Returns:
        O valor máximo total atingível.
    """
    raise NotImplementedError("TODO(P3): Implementar knapsack_one_row")
