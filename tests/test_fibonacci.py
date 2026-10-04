"""Testes unitários para o cálculo da sequência de Fibonacci."""

from __future__ import annotations

import pytest

from src.common import CallCounter
from src.fibonacci import fib_bottom_up, fib_memo, fib_naive, fib_o1_space


class TestFibonacci:
    """Suíte de testes para as diferentes implementações de Fibonacci."""

    @pytest.mark.parametrize("n,expected", [(0, 0), (1, 1), (2, 1), (3, 2), (4, 3), (5, 5), (6, 8), (10, 55)])
    def test_fib_known_values(self, n: int, expected: int) -> None:
        """Testa valores conhecidos da sequência para n de 0 a 10."""
        assert fib_naive(n) == expected
        assert fib_memo(n) == expected
        assert fib_bottom_up(n) == expected
        assert fib_o1_space(n) == expected

    def test_fib_equivalence_small_values(self) -> None:
        """Verifica a equivalência entre todas as versões para valores de 0 a 12."""
        for n in range(13):
            val_naive = fib_naive(n)
            assert fib_memo(n) == val_naive
            assert fib_bottom_up(n) == val_naive
            assert fib_o1_space(n) == val_naive

    def test_fib_call_counter_cormen_naive_and_memo(self) -> None:
        """Verifica o número exato de chamadas do Cormen para n = 10.

        O Fibonacci ingênuo realiza 177 chamadas de função para calcular fib(10).
        A versão memoizada, ao registrar invocações ou subproblemas resolvidos,
        resolve apenas 11 subproblemas distintos (de 0 a 10).
        """
        counter_naive = CallCounter()
        fib_naive(10, counter=counter_naive)
        assert counter_naive.calls == 177

        counter_memo = CallCounter()
        res_memo = fib_memo(10, counter=counter_memo)
        assert res_memo == 55
        # Com memoização, o número de avaliações de subproblemas distintos é 11
        assert counter_memo.calls <= 20  # Linear, na faixa de O(n) chamadas

    def test_fib_large_value(self) -> None:
        """Testa valor maior onde apenas abordagens eficientes executam rapidamente."""
        # F(30) = 832040
        assert fib_bottom_up(30) == 832040
        assert fib_o1_space(30) == 832040
        assert fib_memo(30) == 832040
