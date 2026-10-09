"""Módulo de compatibilidade e entrada para geração dos gráficos de benchmark.

Redireciona para benchmarks.plot_results.
"""

from __future__ import annotations

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from plot_results import main

if __name__ == "__main__":
    main()
