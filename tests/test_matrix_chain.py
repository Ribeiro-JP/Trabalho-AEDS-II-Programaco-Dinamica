"""Testes unitários para Multiplicação em Cadeia de Matrizes (Cormen 15.2)."""

from __future__ import annotations

import pytest

from src.matrix_chain import (
    count_parenthesizations,
    matrix_chain_memo,
    matrix_chain_naive,
    matrix_chain_order,
    optimal_parens,
)


class TestMatrixChain:
    """Suíte de testes para multiplicação em cadeia de matrizes."""

    def test_cormen_reference_example_6_matrices(self) -> None:
        """Exemplo oficial do Cormen com 6 matrizes:

        dims = [30, 35, 15, 5, 10, 20, 25]
        Custo mínimo: 15125 multiplicações escalares.
        Parentização ótima: ((A1(A2A3))((A4A5)A6)).
        """
        dims = [30, 35, 15, 5, 10, 20, 25]
        m, s = matrix_chain_order(dims)
        n = len(dims) - 1

        assert m[1][n] == 15125
        assert matrix_chain_memo(dims) == 15125

        parens = optimal_parens(s, 1, n)
        assert parens == "((A1(A2A3))((A4A5)A6))"

    def test_base_cases_single_and_two_matrices(self) -> None:
        """Casos de borda: apenas 1 matriz (sem multiplicação) e 2 matrizes."""
        # 1 matriz: A1 de 10 x 20
        dims_1 = [10, 20]
        m1, s1 = matrix_chain_order(dims_1)
        assert m1[1][1] == 0
        assert optimal_parens(s1, 1, 1) == "A1"
        assert matrix_chain_naive(dims_1) == 0

        # 2 matrizes: A1 (10 x 20) e A2 (20 x 30)
        dims_2 = [10, 20, 30]
        m2, s2 = matrix_chain_order(dims_2)
        assert m2[1][2] == 6000
        assert matrix_chain_naive(dims_2) == 6000
        assert matrix_chain_memo(dims_2) == 6000
        assert optimal_parens(s2, 1, 2) == "(A1A2)"

    def test_equivalence_small_chain(self) -> None:
        """Compara naive, memo e bottom-up em cadeia com 4 matrizes."""
        dims = [10, 100, 5, 50, 1]
        cost_naive = matrix_chain_naive(dims)
        cost_memo = matrix_chain_memo(dims)
        m, s = matrix_chain_order(dims)
        cost_bu = m[1][len(dims) - 1]

        assert cost_naive == cost_memo == cost_bu
        assert cost_bu > 0

    def test_catalan_parenthesization_count(self) -> None:
        """Verifica a sequência dos números de Catalan C(n-1) para n = 1 a 6 matrizes.

        n = 1: C(0) = 1
        n = 2: C(1) = 1
        n = 3: C(2) = 2
        n = 4: C(3) = 5
        n = 5: C(4) = 14
        n = 6: C(5) = 42
        """
        expected_counts = [1, 1, 2, 5, 14, 42]
        for n, expected in enumerate(expected_counts, start=1):
            assert count_parenthesizations(n) == expected
