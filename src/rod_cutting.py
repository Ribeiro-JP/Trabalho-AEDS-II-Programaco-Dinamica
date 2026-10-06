"""Problema do Corte de Hastes (Rod Cutting) - Cormen Seção 15.1.

Dada uma haste de comprimento n e uma tabela de preços p[1..n], determinar
a receita máxima r_n obtida cortando a haste em pedaços inteiros e vendendo-os.

Recorrência fundamental:
    r_0 = 0
    r_n = max_{1 <= i <= n} (p[i] + r_{n-i}), para n >= 1
"""

from __future__ import annotations

from .common import CallCounter

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
    if counter is not None:
        counter.increment()

    if n == 0:
        return 0

    max_revenue = -float('inf')

    for i in range(1, n + 1):
        revenue = p[i] + cut_rod_naive(p, n - i, counter)
        if revenue > max_revenue:
            max_revenue = revenue

    return int(max_revenue)


def cut_rod_memo(p: list[int], n: int, counter: CallCounter | None = None, memory: dict | None = None) -> int:
    """Resolve o corte de haste com recursão e memoização (Top-Down).

    Guarda os valores ótimos r[0..n] em um vetor de resultados conhecidos.

    Complexidade:
        Tempo: Theta(n^2).
        Espaço: Theta(n) para a tabela de memoização e pilha de chamadas.

    Args:
        p: Vetor de preços onde p[i] é o valor de uma haste de tamanho i.
        n: Comprimento total da haste inicial.
        counter: Instância opcional de CallCounter para registrar invocações.

        memory: Guarda os valores para evitar recalcular.

    Returns:
        A receita máxima obtida para uma haste de tamanho n.
    """

    if memory is None:
        memory = {}

    if counter is not None:
        counter.increment()

    if n in memory:
        return memory[n]

    if n == 0:
        return 0

    max_revenue = -float('inf')
    
    for i in range(1, n + 1):
        
        revenue_atual = p[i] + cut_rod_memo(p, n - i, counter, memory)
        if revenue_atual > max_revenue:
            max_revenue = revenue_atual
            
    memory[n] = int(max_revenue)
    return memory[n]


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

    tabela = [0] * (n + 1)

    for j in range(1, n + 1):
        max_revenue = -float('inf')
        
        for i in range(1, j + 1):
            revenue_atual = p[i] + tabela[j - i]
            
            if revenue_atual > max_revenue:
                max_revenue = revenue_atual
                
        tabela[j] = int(max_revenue)
        
    return tabela[n]


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

    r = [0] * (n + 1)
    s = [0] * (n + 1)

    for j in range(1, n + 1):
        max_revenue = -float('inf')
        
        for i in range(1, j + 1):
            revenue_atual = p[i] + r[j - i]
            
            if revenue_atual > max_revenue:
                max_revenue = revenue_atual
                s[j] = i
                
        r[j] = int(max_revenue)
        
    return r[n], s


def reconstruct_cuts(s: list[int], n: int) -> list[int]:
    """Reconstrói a lista de pedaços que compõem o corte ótimo a partir do vetor s.

    Args:
        s: Vetor de escolhas ótimas gerado por `cut_rod_extended`.
        n: Comprimento original da haste.

    Returns:
        Lista com os comprimentos de cada pedaço cortado na solução ótima.
    """

    pedacos = []
    
    # Enquanto ainda houver haste restante para ser cortada
    while n > 0:
        # s[n] nos diz o tamanho do pedaço ótimo a ser retirado de uma haste de tamanho n
        first_piece = s[n]
        pedacos.append(first_piece)
        
        # Subtrai o pedaço cortado do comprimento atual da haste
        n -= first_piece
        
    return pedacos

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
    if n == 0:
        return 0, []

    razoes = []
    for i in range(1, len(p)):
        razao = p[i] / i
        razoes.append((razao, i))

    razoes.sort(reverse=True, key=lambda x: x[0])

    revenue = 0
    pedacos = []
    remaining_length = n

    for razao, tamanho in razoes:
        while remaining_length >= tamanho:
            revenue += p[tamanho]
            pedacos.append(tamanho)
            remaining_length -= tamanho

    return revenue, pedacos
