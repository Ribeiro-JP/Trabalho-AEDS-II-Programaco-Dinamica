"""Testes unitários para os estudos de caso (Diff de texto e Alinhamento de DNA)."""

from __future__ import annotations

import pytest

from src.case_study.diff_tool import diff_lines
from src.case_study.dna_alignment import align, edit_distance


class TestCaseStudy:
    """Suíte de testes para os estudos de caso de Programação Dinâmica."""

    def test_diff_tool_basic(self) -> None:
        """Testa geração de diff unificado com adição, remoção e linhas comuns."""
        a = ["linha 1\n", "linha 2 antiga\n", "linha 3\n"]
        b = ["linha 1\n", "linha 2 nova\n", "linha 3\n", "linha 4 adicionada\n"]

        diff = diff_lines(a, b)
        # Deve preservar linhas 1 e 3 com prefixo de espaço
        # Deve marcar remoção com '-' e adição com '+'
        assert any(l.startswith("  linha 1") for l in diff)
        assert any(l.startswith("- linha 2 antiga") for l in diff)
        assert any(l.startswith("+ linha 2 nova") for l in diff)
        assert any(l.startswith("+ linha 4 adicionada") for l in diff)

    def test_diff_tool_identical(self) -> None:
        """Arquivos idênticos não devem conter linhas com '+' ou '-'."""
        lines = ["alfa\n", "beta\n", "gama\n"]
        diff = diff_lines(lines, lines)
        assert not any(l.startswith("+ ") or l.startswith("- ") for l in diff)
        assert len(diff) == 3

    def test_dna_edit_distance_classic(self) -> None:
        """Exemplo clássico da literatura (kitten -> sitting = 3 operações)."""
        assert edit_distance("kitten", "sitting") == 3
        assert edit_distance("", "DNA") == 3
        assert edit_distance("ACGT", "ACGT") == 0

    def test_dna_alignment_structure(self) -> None:
        """Verifica se o alinhamento com gaps produz strings de mesmo tamanho."""
        seq_a = "ACGTACGTTAGC"
        seq_b = "ACGTAGCTTAGC"

        dist = edit_distance(seq_a, seq_b)
        aligned_a, aligned_b, score = align(seq_a, seq_b)

        assert len(aligned_a) == len(aligned_b)
        assert aligned_a.replace("-", "") == seq_a
        assert aligned_b.replace("-", "") == seq_b
        assert dist >= 0
