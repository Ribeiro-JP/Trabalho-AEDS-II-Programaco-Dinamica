"""Testes unitários para Subsequência Comum Máxima (LCS - Cormen 15.4)."""

from __future__ import annotations

import pytest

from src.lcs import (
    format_table,
    lcs_length_two_rows,
    lcs_memo,
    lcs_naive,
    lcs_string,
    lcs_table,
)


class TestLCS:
    """Suíte de testes para os algoritmos de Subsequência Comum Máxima."""

    def test_cormen_reference_strings(self) -> None:
        """Exemplo oficial do Cormen:

        X = 'ABCBDAB'
        Y = 'BDCABA'
        Comprimento ótimo da LCS = 4.
        Soluções possíveis válidas: 'BCBA', 'BDAB', 'BCAB'.
        """
        x = "ABCBDAB"
        y = "BDCABA"

        assert lcs_naive(x, y) == 4
        assert lcs_memo(x, y) == 4
        assert lcs_length_two_rows(x, y) == 4

        c, b = lcs_table(x, y)
        assert c[len(x)][len(y)] == 4

        lcs_res = lcs_string(x, y)
        assert len(lcs_res) == 4
        assert lcs_res in {"BCBA", "BDAB", "BCAB"}

    def test_edge_cases(self) -> None:
        """Casos de borda: strings vazias, idênticas e totalmente disjuntas."""
        # Strings vazias
        assert lcs_naive("", "") == 0
        assert lcs_memo("", "") == 0
        assert lcs_string("", "") == ""
        assert lcs_length_two_rows("", "") == 0

        assert lcs_naive("ABC", "") == 0
        assert lcs_memo("", "XYZ") == 0

        # Strings idênticas
        assert lcs_naive("ALGORITMO", "ALGORITMO") == 9
        assert lcs_string("ALGORITMO", "ALGORITMO") == "ALGORITMO"
        assert lcs_length_two_rows("ALGORITMO", "ALGORITMO") == 9

        # Nenhum caractere em comum
        assert lcs_naive("ABC", "DEF") == 0
        assert lcs_memo("ABC", "DEF") == 0
        assert lcs_string("ABC", "DEF") == ""
        assert lcs_length_two_rows("ABC", "DEF") == 0

    def test_equivalence_all_versions(self) -> None:
        """Verifica consistência de resultados entre todas as 4 abordagens."""
        x = "DYNAMIC"
        y = "PROGRAMMING"

        val_naive = lcs_naive(x, y)
        val_memo = lcs_memo(x, y)
        val_two_rows = lcs_length_two_rows(x, y)
        c, _ = lcs_table(x, y)
        val_table = c[len(x)][len(y)]

        assert val_naive == val_memo == val_two_rows == val_table
        seq = lcs_string(x, y)
        assert len(seq) == val_naive

    def test_format_table_output(self) -> None:
        """Testa se a função format_table gera representação em texto contendo as letras das sequências."""
        x = "AB"
        y = "BD"
        c, _ = lcs_table(x, y)
        rendered = format_table(c, x, y)
        assert isinstance(rendered, str)
        assert len(rendered) > 0
