"""Cálculo da sequência de Fibonacci utilizando diferentes abordagens.

Problema de aquecimento para ilustrar o paradigma de Programação Dinâmica:
- Abordagem ingênua (recursiva pura, tempo exponencial)
- Top-Down com Memoização (armazena valores já computados)
- Bottom-Up (tabela linear)
- Otimização de espaço O(1) (apenas duas variáveis anteriores)

Recorrência:
    F(0) = 0
    F(1) = 1
    F(n) = F(n-1) + F(n-2), para n >= 2
"""

from __future__ import annotations

from src.common import CallCounter


def fib_naive(n: int, counter: CallCounter | None = None) -> int:
    """Calcula o n-ésimo termo de Fibonacci recursivamente sem memoização.

    Complexidade:
        Tempo: Theta(2^n) devido à árvore de recursão com repetições redundantes.
        Espaço: O(n) na pilha de chamadas.

    Args:
        n: Índice do termo desejado na sequência de Fibonacci (n >= 0).
        counter: Instância opcional de CallCounter para registrar invocações.

    Returns:
        O valor do n-ésimo termo de Fibonacci.
    """
    raise NotImplementedError("TODO(P3): Implementar fib_naive")


def fib_memo(n: int, counter: CallCounter | None = None) -> int:
    """Calcula o n-ésimo termo de Fibonacci com recursão e memoização (Top-Down).

    Evita recalcular subproblemas já resolvidos consultando uma tabela de cache.

    Complexidade:
        Tempo: Theta(n) pois cada estado de 0 a n é computado apenas uma vez.
        Espaço: Theta(n) para o cache e pilha de recursão.

    Args:
        n: Índice do termo desejado na sequência de Fibonacci (n >= 0).
        counter: Instância opcional de CallCounter para registrar invocações.

    Returns:
        O valor do n-ésimo termo de Fibonacci.
    """
    raise NotImplementedError("TODO(P3): Implementar fib_memo")


def fib_bottom_up(n: int) -> int:
    """Calcula o n-ésimo termo de Fibonacci iterativamente (Bottom-Up).

    Preenche uma tabela de tamanho n + 1 a partir dos casos base F(0) e F(1).

    Complexidade:
        Tempo: Theta(n).
        Espaço: Theta(n) para o vetor de soluções dos subproblemas.

    Args:
        n: Índice do termo desejado na sequência de Fibonacci (n >= 0).

    Returns:
        O valor do n-ésimo termo de Fibonacci.
    """
    raise NotImplementedError("TODO(P3): Implementar fib_bottom_up")


def fib_o1_space(n: int) -> int:
    """Calcula o n-ésimo termo de Fibonacci com espaço constante O(1).

    Como cada termo F(n) depende unicamente de F(n-1) e F(n-2), armazena
    apenas os dois últimos valores calculados, eliminando a tabela completa.

    Complexidade:
        Tempo: Theta(n).
        Espaço: Theta(1).

    Args:
        n: Índice do termo desejado na sequência de Fibonacci (n >= 0).

    Returns:
        O valor do n-ésimo termo de Fibonacci.
    """
    raise NotImplementedError("TODO(P3): Implementar fib_o1_space")
