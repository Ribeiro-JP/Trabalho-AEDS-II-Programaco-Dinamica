"""Módulo de utilitários comuns de infraestrutura e medição de desempenho.

Contém as ferramentas necessárias para instrumentação de chamadas recursivas
e medição de tempo de CPU e consumo de memória (tracemalloc).
"""

from __future__ import annotations

import time
import tracemalloc
from dataclasses import dataclass
from typing import Any, Callable, TypeVar

T = TypeVar("T")


@dataclass
class CallCounter:
    """Contador de chamadas recursivas para instrumentação algorítmica.

    Attributes:
        calls: Quantidade acumulada de invocações da função.
    """

    calls: int = 0

    def increment(self, step: int = 1) -> None:
        """Incrementa o contador de chamadas em 'step' unidades."""
        self.calls += step

    def reset(self) -> None:
        """Reinicia a contagem de chamadas para zero."""
        self.calls = 0


def measure(fn: Callable[..., T], *args: Any, **kwargs: Any) -> tuple[T, float, int]:
    """Mede o tempo de execução e o pico de memória alocada por uma função.

    Utiliza `time.perf_counter` para medição de alta precisão de tempo de parede (segundos)
    e `tracemalloc` para rastrear o pico de memória alocada em bytes durante a execução.

    Args:
        fn: Função ou método a ser executado e mensurado.
        *args: Argumentos posicionais a serem repassados para `fn`.
        **kwargs: Argumentos nomeados a serem repassados para `fn`.

    Returns:
        Uma tupla contendo:
            - resultado: Retorno da invocação de `fn(*args, **kwargs)`.
            - tempo_em_segundos: Tempo decorrido em segundos (float).
            - pico_memoria_bytes: Pico de memória alocada em bytes (int).
    """
    tracemalloc.start()
    tracemalloc.reset_peak()
    start_time = time.perf_counter()

    try:
        resultado = fn(*args, **kwargs)
    finally:
        end_time = time.perf_counter()
        _, pico_memoria_bytes = tracemalloc.get_traced_memory()
        tracemalloc.stop()

    tempo_em_segundos = end_time - start_time
    return resultado, tempo_em_segundos, pico_memoria_bytes
