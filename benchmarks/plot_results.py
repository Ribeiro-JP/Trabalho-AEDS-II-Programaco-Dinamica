"""Módulo para geração e plotagem dos gráficos de experimentos.

Convenções obrigatórias para os gráficos do projeto (ver docs/tarefas/P4_...):
1. Resolução: PNG a 200 DPI salvos no diretório docs/figures/ (e relatorio/figuras/).
2. Textos e rótulos: Totalmente em Português do Brasil (títulos, eixos x/y, legendas).
3. Escalas: Escala logarítmica (semilog ou log-log) em experimentos comparando exponencial x polinomial.
4. Paleta de Cores Padronizada (imutável em todo o projeto, slides e web):
   - Ingênuo (Naive):           Vermelho  #d62728
   - Memoização (Top-Down):     Azul      #1f77b4
   - Bottom-Up (Tabulação):     Verde     #2ca02c
   - Duas Linhas (Espaço Otim): Roxo      #9467bd
   - Guloso (Greedy):           Cinza     #7f7f7f

Responsável: Integrante P4 (ver docs/tarefas/P4_estudo_de_caso_e_benchmarks.md).
"""

from __future__ import annotations

import os

# Paleta oficial do projeto
PALETTE: dict[str, str] = {
    "naive": "#d62728",
    "memo": "#1f77b4",
    "bottom_up": "#2ca02c",
    "two_rows": "#9467bd",
    "greedy": "#7f7f7f",
}

FIGURES_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "docs", "figures")
)


def plot_e1_fibonacci() -> None:
    """Gera gráfico E1: Tempo e número de chamadas recursivas x n (Fibonacci)."""
    raise NotImplementedError("TODO(P4): Implementar plot_e1_fibonacci")


def plot_e2_rod_cutting() -> None:
    """Gera gráfico E2: Tempo x n para corte de hastes (ingênuo x memo x bottom-up)."""
    raise NotImplementedError("TODO(P4): Implementar plot_e2_rod_cutting")


def plot_e3_lcs_memory() -> None:
    """Gera gráfico E3: Pico de memória x tamanho das strings (LCS completa x 2 linhas)."""
    raise NotImplementedError("TODO(P4): Implementar plot_e3_lcs_memory")


def plot_e4_cpp_vs_python() -> None:
    """Gera gráfico E4: Tempo de execução Python x C++ para LCS."""
    raise NotImplementedError("TODO(P4): Implementar plot_e4_cpp_vs_python")


def plot_e6_greedy_failure() -> None:
    """Gera gráfico E6: Taxa de erro percentual da abordagem gulosa no corte de hastes."""
    raise NotImplementedError("TODO(P4): Implementar plot_e6_greedy_failure")


def plot_e7_matrix_chain() -> None:
    """Gera gráfico E7: Tempo da PD x Crescimento dos números de Catalan (Cadeia de Matrizes)."""
    raise NotImplementedError("TODO(P4): Implementar plot_e7_matrix_chain")


def main() -> None:
    """Executa a geração de todos os gráficos a partir dos dados em benchmarks/results/."""
    print("Módulo de plotagem de gráficos (P4).")
    print(f"Diretório de destino: {FIGURES_DIR}")
    print("TODO(P4): Ler dados consolidados em CSV/JSON e salvar figuras a 200 DPI.")


if __name__ == "__main__":
    main()
