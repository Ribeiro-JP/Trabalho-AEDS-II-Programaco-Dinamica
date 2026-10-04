"""Testes unitários para o problema do Corte de Hastes (Rod Cutting - Cormen 15.1)."""

from __future__ import annotations

import pytest

from src.rod_cutting import (
    PRICES_CORMEN,
    cut_rod_bottom_up,
    cut_rod_extended,
    cut_rod_greedy_ratio,
    cut_rod_memo,
    cut_rod_naive,
    reconstruct_cuts,
)


class TestRodCutting:
    """Suíte de testes para os algoritmos de corte de haste."""

    def test_rod_cutting_base_cases(self) -> None:
        """Casos de borda: haste de comprimento 0 e comprimento 1."""
        assert cut_rod_naive(PRICES_CORMEN, 0) == 0
        assert cut_rod_memo(PRICES_CORMEN, 0) == 0
        assert cut_rod_bottom_up(PRICES_CORMEN, 0) == 0

        assert cut_rod_naive(PRICES_CORMEN, 1) == 1
        assert cut_rod_memo(PRICES_CORMEN, 1) == 1
        assert cut_rod_bottom_up(PRICES_CORMEN, 1) == 1

    def test_cormen_reference_values_1_to_10(self) -> None:
        """Verifica a tabela oficial do Cormen: r(1..10) = [1, 5, 8, 10, 13, 17, 18, 22, 25, 30]."""
        expected_revenues = [1, 5, 8, 10, 13, 17, 18, 22, 25, 30]
        for n in range(1, 11):
            expected = expected_revenues[n - 1]
            assert cut_rod_naive(PRICES_CORMEN, n) == expected
            assert cut_rod_memo(PRICES_CORMEN, n) == expected
            assert cut_rod_bottom_up(PRICES_CORMEN, n) == expected

            val_ext, _ = cut_rod_extended(PRICES_CORMEN, n)
            assert val_ext == expected

    def test_equivalence_small_lengths(self) -> None:
        """Garante equivalência entre naive, memo e bottom-up para comprimentos de 0 a 8."""
        for n in range(9):
            val_naive = cut_rod_naive(PRICES_CORMEN, n)
            assert cut_rod_memo(PRICES_CORMEN, n) == val_naive
            assert cut_rod_bottom_up(PRICES_CORMEN, n) == val_naive

    def test_cut_reconstruction(self) -> None:
        """Verifica se os pedaços reconstruídos somam exatamente n e totalizam a receita ótima."""
        for n in range(1, 11):
            revenue, s = cut_rod_extended(PRICES_CORMEN, n)
            cuts = reconstruct_cuts(s, n)
            assert sum(cuts) == n
            sum_prices = sum(PRICES_CORMEN[c] for c in cuts)
            assert sum_prices == revenue

    def test_greedy_vs_dynamic_programming_counterexample(self) -> None:
        """Contra-exemplo canônico onde a estratégia gulosa por densidade falha.

        Preços: [0, 1, 5, 8, 9] para tamanhos 0, 1, 2, 3, 4.
        Densidades:
            tam 1: 1 / 1 = 1.00
            tam 2: 5 / 2 = 2.50  (ótimo relativo)
            tam 3: 8 / 3 = 2.67  (maior densidade)
            tam 4: 9 / 4 = 2.25

        Para n = 4:
            - Guloso escolhe pedaço de tamanho 3 (razão 2.67, sobra 1) -> 8 + 1 = 9.
            - PD escolhe dois pedaços de tamanho 2 -> 5 + 5 = 10.
        """
        prices = [0, 1, 5, 8, 9]
        n = 4
        optimal_revenue = cut_rod_bottom_up(prices, n)
        greedy_revenue, pieces = cut_rod_greedy_ratio(prices, n)

        assert optimal_revenue == 10
        assert greedy_revenue == 9
        assert sum(pieces) == n
        assert greedy_revenue < optimal_revenue
