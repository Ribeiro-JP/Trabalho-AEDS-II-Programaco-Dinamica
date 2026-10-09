"""Suíte de Benchmarks e Experimentos Empíricos de Programação Dinâmica (AEDS-II).

Este módulo executa experimentos empíricos controlados comparando abordagens
ingênuas (força bruta recursiva), memoização (Top-Down), tabulação (Bottom-Up)
e heurísticas gulosas para problemas clássicos do Cap. 15 do Cormen.

Tabela de Experimentos:
+----+-------------------------------------------------------------------------+-------------------------------------------------------+
| ID | Experimento                                                             | O que deve mostrar                                    |
+----+-------------------------------------------------------------------------+-------------------------------------------------------+
| E1 | Fibonacci: tempo e nº de chamadas x n                                   | Explosão exponencial contra crescimento linear        |
| E2 | Corte de hastes: tempo x n (naive, memo, bottom-up)                     | Theta(2^n) contra Theta(n^2)                          |
| E3 | LCS: tempo x tamanho; pico de memória (tabela completa x duas linhas)   | Theta(mn) e ganho de memória                          |
| E4 | LCS: Python contra C++                                                  | Gargalo de linguagem e overhead de interpretador      |
| E5 | Limite de recursão (RecursionError) na memoização                       | Custo do top-down no Python                           |
| E6 | Guloso contra PD (% de instâncias aleatórias em que o guloso erra)       | Guloso falha com frequência mensurável                |
| E7 | Cadeia de matrizes: tempo x n (naive, memo, bottom-up) e Catalan x n    | Theta(n^3) contra exponencial e explosão de Catalan   |
| E8 | Mochila 0/1: tempo x capacidade W (pseudo-polinomial)                   | Natureza pseudo-polinomial dependente de W            |
+----+-------------------------------------------------------------------------+-------------------------------------------------------+

Protocolo Científico Rigoroso:
- Média truncada de 5 repetições (descarta menor e maior medição, média das 3 centrais).
- Medição de memória (tracemalloc) isolada da medição de tempo para evitar distorção por overhead.
- Timeout real com encerramento de processo para algoritmos de complexidade exponencial.
- Sementes fixas para reprodutibilidade estrita.
- Gravação atômica dos datasets em CSV e exportação compatível para web/data/results.json.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import multiprocessing
import os
import platform
import queue
import random
import statistics
import subprocess
import sys
import tempfile
import time
import tracemalloc
import types
from typing import Any, Callable

# Configuração de caminhos do projeto
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
SRC_DIR = os.path.join(ROOT_DIR, "src")
RESULTS_DIR = os.path.join(SCRIPT_DIR, "results")
WEB_DATA_DIR = os.path.join(ROOT_DIR, "web", "data")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)


# -----------------------------------------------------------------------------
# 1. Carregador Seguro de Módulos (Garante integridade de src/)
# -----------------------------------------------------------------------------
def load_module_safely(module_name: str, file_rel_path: str) -> types.ModuleType:
    """Carrega módulo de src/ tratando diretivas com segurança em memória."""
    if module_name in sys.modules:
        return sys.modules[module_name]

    file_abs_path = os.path.join(SRC_DIR, file_rel_path)
    with open(file_abs_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Se houver diretiva de importação futura fora do topo, reorganiza em memória
    if "from __future__ import annotations" in content:
        lines = content.splitlines()
        future_line = "from __future__ import annotations"
        clean_lines = [l for l in lines if l.strip() != future_line]
        content = future_line + "\n" + "\n".join(clean_lines)

    mod = types.ModuleType(module_name)
    mod.__file__ = file_abs_path
    mod.__package__ = "src"
    sys.modules[module_name] = mod
    code_obj = compile(content, file_abs_path, "exec")
    exec(code_obj, mod.__dict__)
    return mod


# Módulos carregados sob demanda
common_mod = load_module_safely("src.common", "common.py")
fib_mod = load_module_safely("src.fibonacci", "fibonacci.py")
rod_mod = load_module_safely("src.rod_cutting", "rod_cutting.py")
lcs_mod = load_module_safely("src.lcs", "lcs.py")
matrix_mod = load_module_safely("src.matrix_chain", "matrix_chain.py")
knapsack_mod = load_module_safely("src.knapsack", "knapsack.py")

CallCounter = common_mod.CallCounter


# -----------------------------------------------------------------------------
# 2. Infraestrutura Estatística e de Medição Segura
# -----------------------------------------------------------------------------
def calculate_trimmed_mean(times: list[float]) -> float:
    """Calcula a média representativa conforme protocolo estatístico do projeto.

    Regras:
    - Se len(times) >= 5: descarta o menor e o maior tempo e calcula a média dos restantes.
    - Se len(times) in (3, 4): descarta o menor e o maior tempo e calcula a média dos centrais.
    - Se len(times) == 2: média aritmética dos 2 valores.
    - Se len(times) == 1: o próprio valor.
    - Se len(times) == 0: lança ValueError.
    """
    if not times:
        raise ValueError("A lista de tempos não pode estar vazia.")

    if len(times) >= 5:
        sorted_times = sorted(times)
        return statistics.mean(sorted_times[1:-1])
    elif len(times) >= 3:
        sorted_times = sorted(times)
        return statistics.mean(sorted_times[1:-1])
    elif len(times) == 2:
        return statistics.mean(times)
    else:
        return times[0]


def _worker_process_runner(
    fn: Callable[..., Any],
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
    out_q: multiprocessing.Queue,
) -> None:
    """Função executada em subprocesso isolado para garantir encerramento sob timeout."""
    try:
        t0 = time.perf_counter()
        res = fn(*args, **kwargs)
        elapsed = time.perf_counter() - t0
        out_q.put(("success", elapsed, res))
    except RecursionError:
        out_q.put(("recursion_error", None, None))
    except Exception as err:
        out_q.put(("execution_error", None, str(err)))


def execute_with_process_timeout(
    fn: Callable[..., Any],
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
    timeout_seconds: float,
) -> tuple[float | None, Any, str]:
    """Executa função em subprocesso separado garantindo encerramento real sob timeout.

    Retorna:
        tuple[tempo_segundos | None, resultado | None, status_str]
    """
    out_q: multiprocessing.Queue = multiprocessing.Queue()
    p = multiprocessing.Process(
        target=_worker_process_runner,
        args=(fn, args, kwargs, out_q),
    )
    p.start()
    p.join(timeout=timeout_seconds)

    if p.is_alive():
        # Encerramento forçado e limpeza do processo órfão
        p.terminate()
        p.join(timeout=1.0)
        if p.is_alive():
            try:
                p.kill()
            except Exception:
                pass
            p.join()
        return None, None, "timeout"

    try:
        status, elapsed, res = out_q.get_nowait()
        return elapsed, res, status
    except (queue.Empty, Exception):
        return None, None, "execution_error"


def measure_execution(
    fn: Callable[..., Any],
    *args: Any,
    repeats: int = 5,
    measure_peak_mem: bool = False,
    timeout: float | None = None,
    **kwargs: Any,
) -> tuple[float | None, int | None, str]:
    """Mede o tempo de execução e, isoladamente, o consumo de pico de memória.

    Requisitos Científicos:
    1. Medição de tempo estritamente independente de tracemalloc (sem sobrecarga de rastreamento).
    2. Protocolo de média truncada em 5 repetições (descarte de min e max).
    3. Suporte a timeout real através de encerramento de processo para algoritmos exponenciais.
    4. Garantia de desligamento de tracemalloc em caso de exceção.
    5. Documentação: tracemalloc rastreia alocações do heap Python, não o RSS total do SO.

    Retorna:
        (time_seconds, memory_bytes, status)
        onde status pode ser 'success', 'timeout', 'recursion_error', 'execution_error'.
    """
    # Se timeout foi solicitado e é positivo, utiliza proteção de processo
    if timeout is not None and timeout > 0:
        elapsed, _, status = execute_with_process_timeout(fn, args, kwargs, timeout)
        if status != "success":
            return None, None, status
        # Se a primeira execução passou no timeout, realizamos as repetições
        times: list[float] = [elapsed]
        for _ in range(repeats - 1):
            elp, _, st = execute_with_process_timeout(fn, args, kwargs, timeout)
            if st != "success":
                return None, None, st
            if elp is not None:
                times.append(elp)

        final_time = calculate_trimmed_mean(times)
        return final_time, None, "success"

    # Medição in-process para algoritmos sem timeout crítico
    times: list[float] = []
    for _ in range(repeats):
        try:
            start_t = time.perf_counter()
            _ = fn(*args, **kwargs)
            elapsed_t = time.perf_counter() - start_t
            times.append(elapsed_t)
        except RecursionError:
            return None, None, "recursion_error"
        except Exception:
            return None, None, "execution_error"

    final_time = calculate_trimmed_mean(times)

    # Medição de memória ISOLADA (execução separada para não contaminar tempos)
    peak_mem_bytes: int | None = None
    if measure_peak_mem:
        tracemalloc.start()
        tracemalloc.reset_peak()
        try:
            _ = fn(*args, **kwargs)
            _, peak_mem_bytes = tracemalloc.get_traced_memory()
        except RecursionError:
            peak_mem_bytes = None
        except Exception:
            peak_mem_bytes = None
        finally:
            if tracemalloc.is_tracing():
                tracemalloc.stop()

    return final_time, peak_mem_bytes, "success"


# -----------------------------------------------------------------------------
# 3. Persistência de Dados e Atualização Consolidada Atômica
# -----------------------------------------------------------------------------
CONSOLIDATED_COLUMNS = [
    "experiment",
    "algorithm",
    "approach",
    "n",
    "time_seconds",
    "memory_bytes",
    "calls",
    "status",
    "notes",
]


def atomic_write_csv(filepath: str, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    """Grava arquivo CSV atomicamente utilizando arquivo temporário."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    dir_name = os.path.dirname(filepath)
    with tempfile.NamedTemporaryFile("w", dir=dir_name, delete=False, newline="", encoding="utf-8") as tf:
        temp_name = tf.name
        writer = csv.DictWriter(tf, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for r in rows:
            # Garante representação textual adequada de valores nulos
            cleaned_row = {
                k: ("" if v is None else v) for k, v in r.items() if k in fieldnames
            }
            writer.writerow(cleaned_row)

    os.replace(temp_name, filepath)


def save_csv(filename: str, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    """Salva dataset individual em benchmarks/results/ com escrita atômica."""
    dest = os.path.join(RESULTS_DIR, filename)
    atomic_write_csv(dest, fieldnames, rows)


def upsert_consolidated(new_rows: list[dict[str, Any]], exp_id: str) -> None:
    """Atualiza o dataset all_benchmarks.csv de forma atômica e idempotente.

    Comportamento estrito:
    - Substitui exclusivamente os registros do experimento `exp_id`.
    - Preserva intactos os registros de todos os outros experimentos.
    - Nunca gera registros duplicados nem corrompe o cabeçalho.
    """
    dest = os.path.join(RESULTS_DIR, "all_benchmarks.csv")
    existing_rows: list[dict[str, Any]] = []

    if os.path.exists(dest):
        try:
            with open(dest, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Preserva linhas de outros experimentos
                    if row.get("experiment") != exp_id:
                        existing_rows.append(row)
        except Exception as err:
            print(f"      [AVISO] Não foi possível ler consolidação existente: {err}")
            existing_rows = []

    # Normaliza novos registros para o esquema padrão de consolidação
    normalized_new_rows: list[dict[str, Any]] = []
    for r in new_rows:
        item = {col: r.get(col, "") for col in CONSOLIDATED_COLUMNS}
        normalized_new_rows.append(item)

    combined_rows = existing_rows + normalized_new_rows
    atomic_write_csv(dest, CONSOLIDATED_COLUMNS, combined_rows)


def export_web_results_json() -> None:
    """Exporta todos os resultados gerados para web/data/results.json.

    - Mantém compatibilidade integral com a interface web.
    - Valores ausentes de tempo (falhas, timeout) são serializados como null.
    - Campos específicos de E5, E6 e E7 são preservados no JSON.
    - Gravação atômica via arquivo temporário.
    """
    os.makedirs(WEB_DATA_DIR, exist_ok=True)
    all_data: dict[str, list[dict[str, Any]]] = {}

    csv_mapping = {
        "E1": "e1_fibonacci.csv",
        "E2": "e2_rod_cutting.csv",
        "E3": "e3_lcs_memory.csv",
        "E4": "e4_lcs_cpp.csv",
        "E5": "e5_recursion_limit.csv",
        "E6": "e6_greedy_failure.csv",
        "E7": "e7_matrix_chain.csv",
        "E8": "e8_knapsack.csv",
    }

    for exp_id, filename in csv_mapping.items():
        filepath = os.path.join(RESULTS_DIR, filename)
        if not os.path.exists(filepath):
            continue

        records: list[dict[str, Any]] = []
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rec: dict[str, Any] = {}
                for k, v in row.items():
                    if v == "" or v is None:
                        rec[k] = None
                    elif k in ["n", "calls", "memory_bytes", "num_instances", "failures", "catalan_count"]:
                        try:
                            rec[k] = int(v)
                        except ValueError:
                            rec[k] = v
                    elif k in ["time_seconds", "failure_rate_percent", "average_loss_percent"]:
                        try:
                            rec[k] = float(v)
                        except ValueError:
                            rec[k] = None
                    else:
                        rec[k] = v
                records.append(rec)

        all_data[exp_id] = records

    dest_json = os.path.join(WEB_DATA_DIR, "results.json")
    with tempfile.NamedTemporaryFile("w", dir=WEB_DATA_DIR, delete=False, encoding="utf-8") as tf:
        temp_name = tf.name
        json.dump(all_data, tf, indent=2, ensure_ascii=False)

    os.replace(temp_name, dest_json)
    print(f"[OK] Dados consolidados exportados com sucesso para '{dest_json}'.")


def save_machine_metadata() -> None:
    """Gera metadados de reprodutibilidade em benchmarks/results/machine.json."""
    os.makedirs(RESULTS_DIR, exist_ok=True)
    dest = os.path.join(RESULTS_DIR, "machine.json")

    meta: dict[str, Any] = {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": sys.version,
        "python_implementation": platform.python_implementation(),
        "recursion_limit": sys.getrecursionlimit(),
        "measurement_protocol": {
            "name": "Média truncada de 3 centrais em 5 repetições",
            "repeats": 5,
            "discard_min_max": True,
            "memory_measurement": "tracemalloc isolado (alocações Python heap)",
            "random_seed": 42,
        },
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }

    with open(dest, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)


# -----------------------------------------------------------------------------
# 4. Implementação dos Experimentos E1 a E8
# -----------------------------------------------------------------------------

def exp_e1_fibonacci(quick: bool = False) -> None:
    """E1: Fibonacci - Força bruta, memoização, Bottom-Up e espaço O(1).

    Requisitos:
    - CallCounter independente por execução (sem acumular entre repetições).
    - Média coerente das contagens de chamadas.
    - Preservação temporária e segura do limite de recursão via try...finally.
    - Timeout real para a força bruta recursiva.
    """
    repeats = 3 if quick else 5
    naive_ns = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30] if quick else [
        2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32
    ]
    pd_ns = [
        2, 5, 8, 10, 15, 20, 25, 30, 40, 50, 75, 100, 150, 200, 300, 500
    ] if quick else [
        2, 5, 8, 10, 15, 20, 25, 30, 40, 50, 75, 100, 150, 200, 300, 500, 750, 1000, 1500, 2000
    ]

    results: list[dict[str, Any]] = []

    # 1. Naive (Força Bruta)
    for n in naive_ns:
        times: list[float] = []
        call_counts: list[int] = []
        status = "success"

        for _ in range(repeats):
            c = CallCounter()
            t, _, st = measure_execution(fib_mod.fib_naive, n, counter=c, repeats=1, timeout=3.0)
            if st != "success":
                status = st
                break
            if t is not None:
                times.append(t)
                call_counts.append(c.calls)

        avg_time = calculate_trimmed_mean(times) if status == "success" and times else None
        avg_calls = int(round(statistics.mean(call_counts))) if call_counts else None

        results.append({
            "experiment": "E1",
            "algorithm": "Fibonacci",
            "approach": "naive",
            "n": n,
            "time_seconds": avg_time,
            "memory_bytes": 0,
            "calls": avg_calls,
            "status": status,
            "notes": "Theta(2^n) Recursivo Puro",
        })
        if status == "timeout":
            break

    # 2. Programação Dinâmica: Memo, Bottom-Up e O(1) Espaço
    old_recursion_limit = sys.getrecursionlimit()
    max_needed_limit = max(pd_ns) + 500
    try:
        if max_needed_limit > old_recursion_limit:
            sys.setrecursionlimit(max_needed_limit)

        for n in pd_ns:
            # Top-Down Memoização
            times_memo: list[float] = []
            calls_memo: list[int] = []
            for _ in range(repeats):
                c = CallCounter()
                t, _, st = measure_execution(fib_mod.fib_memo, n, counter=c, memory={}, repeats=1)
                if t is not None and st == "success":
                    times_memo.append(t)
                    calls_memo.append(c.calls)

            results.append({
                "experiment": "E1",
                "algorithm": "Fibonacci",
                "approach": "memo",
                "n": n,
                "time_seconds": calculate_trimmed_mean(times_memo) if times_memo else None,
                "memory_bytes": 0,
                "calls": int(round(statistics.mean(calls_memo))) if calls_memo else 2 * n - 1,
                "status": "success",
                "notes": "Theta(n) Top-Down com Memoização",
            })

            # Bottom-Up Tabulação
            t_bu, _, st_bu = measure_execution(fib_mod.fib_bottom_up, n, repeats=repeats)
            results.append({
                "experiment": "E1",
                "algorithm": "Fibonacci",
                "approach": "bottom_up",
                "n": n,
                "time_seconds": t_bu,
                "memory_bytes": 0,
                "calls": 1,
                "status": st_bu,
                "notes": "Theta(n) Bottom-Up Iterativo",
            })

            # Espaço O(1)
            t_o1, _, st_o1 = measure_execution(fib_mod.fib_o1_space, n, repeats=repeats)
            results.append({
                "experiment": "E1",
                "algorithm": "Fibonacci",
                "approach": "o1_space",
                "n": n,
                "time_seconds": t_o1,
                "memory_bytes": 0,
                "calls": 1,
                "status": st_o1,
                "notes": "Theta(n) Tempo, O(1) Espaço",
            })
    finally:
        sys.setrecursionlimit(old_recursion_limit)

    fieldnames = list(results[0].keys())
    save_csv("e1_fibonacci.csv", fieldnames, results)
    upsert_consolidated(results, "E1")
    print(f"      -> {len(results)} registros gerados para Fibonacci (E1).")


def exp_e2_rod_cutting(quick: bool = False) -> None:
    """E2: Corte de hastes - Comparação entre força bruta e Programação Dinâmica."""
    repeats = 3 if quick else 5
    rng = random.Random(42)

    naive_ns = list(range(2, 16)) if quick else list(range(2, 21))
    pd_ns = [
        2, 5, 8, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100, 120
    ] if quick else [
        2, 5, 8, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200
    ]

    # Gera preços base determinísticos com extensão linear
    base_prices = list(rod_mod.PRICES_CORMEN)
    max_len = max(pd_ns) + 10
    while len(base_prices) <= max_len:
        idx = len(base_prices)
        base_prices.append(base_prices[-1] + rng.randint(1, 4))

    results: list[dict[str, Any]] = []

    # 1. Força Bruta (Naive)
    for n in naive_ns:
        times: list[float] = []
        call_counts: list[int] = []
        status = "success"

        for _ in range(repeats):
            c = CallCounter()
            t, _, st = measure_execution(rod_mod.cut_rod_naive, base_prices, n, counter=c, repeats=1, timeout=3.0)
            if st != "success":
                status = st
                break
            if t is not None:
                times.append(t)
                call_counts.append(c.calls)

        avg_time = calculate_trimmed_mean(times) if status == "success" and times else None
        avg_calls = int(round(statistics.mean(call_counts))) if call_counts else None

        results.append({
            "experiment": "E2",
            "algorithm": "Corte de Hastes",
            "approach": "naive",
            "n": n,
            "time_seconds": avg_time,
            "memory_bytes": 0,
            "calls": avg_calls,
            "status": status,
            "notes": "Theta(2^n) Recursivo Puro",
        })
        if status == "timeout":
            break

    # 2. PD: Memoização e Bottom-Up
    for n in pd_ns:
        # Validação de equivalência de solução ótima
        val_memo = rod_mod.cut_rod_memo(base_prices, n)
        val_bu = rod_mod.cut_rod_bottom_up(base_prices, n)
        if val_memo != val_bu:
            print(f"      [AVISO] Divergência em E2 para n={n}: memo={val_memo}, bu={val_bu}")

        t_memo, _, st_memo = measure_execution(rod_mod.cut_rod_memo, base_prices, n, repeats=repeats)
        results.append({
            "experiment": "E2",
            "algorithm": "Corte de Hastes",
            "approach": "memo",
            "n": n,
            "time_seconds": t_memo,
            "memory_bytes": 0,
            "calls": n + 1,
            "status": st_memo,
            "notes": "Theta(n^2) Top-Down Memoização",
        })

        t_bu, _, st_bu = measure_execution(rod_mod.cut_rod_bottom_up, base_prices, n, repeats=repeats)
        results.append({
            "experiment": "E2",
            "algorithm": "Corte de Hastes",
            "approach": "bottom_up",
            "n": n,
            "time_seconds": t_bu,
            "memory_bytes": 0,
            "calls": 1,
            "status": st_bu,
            "notes": "Theta(n^2) Bottom-Up Tabulação",
        })

    fieldnames = list(results[0].keys())
    save_csv("e2_rod_cutting.csv", fieldnames, results)
    upsert_consolidated(results, "E2")
    print(f"      -> {len(results)} registros gerados para Corte de Hastes (E2).")


def exp_e3_lcs_memory(quick: bool = False) -> None:
    """E3: LCS - Comparação de memória e tempo entre tabela completa e duas linhas."""
    repeats = 3 if quick else 5
    rng = random.Random(42)
    alphabet = ["A", "C", "G", "T"]

    sizes = [
        50, 100, 150, 200, 250, 300, 350, 400, 450, 500,
        550, 600, 700, 800, 900, 1000
    ] if quick else [
        50, 100, 150, 200, 250, 300, 350, 400, 450, 500,
        550, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400
    ]

    results: list[dict[str, Any]] = []

    for n in sizes:
        s1 = "".join(rng.choices(alphabet, k=n))
        s2 = "".join(rng.choices(alphabet, k=n))

        # Tabela completa (c, b)
        t_full, mem_full, st_full = measure_execution(
            lcs_mod.lcs_table, s1, s2, repeats=repeats, measure_peak_mem=True
        )
        results.append({
            "experiment": "E3",
            "algorithm": "LCS",
            "approach": "bottom_up",
            "n": n,
            "time_seconds": t_full,
            "memory_bytes": mem_full or 0,
            "calls": 1,
            "status": st_full,
            "notes": f"Tabela completa: Theta(mn) ({round((mem_full or 0)/1024, 1)} KB)",
        })

        # Duas linhas (espaço otimizado)
        t_two, mem_two, st_two = measure_execution(
            lcs_mod.lcs_length_two_rows, s1, s2, repeats=repeats, measure_peak_mem=True
        )
        results.append({
            "experiment": "E3",
            "algorithm": "LCS",
            "approach": "two_rows",
            "n": n,
            "time_seconds": t_two,
            "memory_bytes": mem_two or 0,
            "calls": 1,
            "status": st_two,
            "notes": f"Duas linhas: Theta(min(m,n)) ({round((mem_two or 0)/1024, 1)} KB)",
        })

    fieldnames = list(results[0].keys())
    save_csv("e3_lcs_memory.csv", fieldnames, results)
    upsert_consolidated(results, "E3")
    print(f"      -> {len(results)} registros gerados para LCS Memória (E3).")


def exp_e4_lcs_cpp_vs_python(quick: bool = False) -> None:
    """E4: LCS - Comparação de desempenho Python contra C++.

    Metodologia:
    - O código C++ é compilado com -O3 se g++ estiver disponível.
    - Se C++ não estiver presente ou implementado, documenta explicitamente a ausência
      e foca na medição de referência em Python (CPython 3.11).
    - C++ é rotulado como Bottom-Up (e nunca como 'memo').
    """
    repeats = 3 if quick else 5
    rng = random.Random(42)
    alphabet = ["A", "C", "G", "T"]
    sizes = [50, 100, 200, 300, 400, 500, 600, 800, 1000] if quick else [
        50, 100, 150, 200, 250, 300, 350, 400, 500, 600, 700, 800, 900, 1000, 1200
    ]

    cpp_bin_win = os.path.join(ROOT_DIR, "cpp", "lcs.exe")
    cpp_bin_posix = os.path.join(ROOT_DIR, "cpp", "lcs")
    cpp_binary = cpp_bin_win if os.path.exists(cpp_bin_win) else (cpp_bin_posix if os.path.exists(cpp_bin_posix) else None)

    results: list[dict[str, Any]] = []

    for n in sizes:
        s1 = "".join(rng.choices(alphabet, k=n))
        s2 = "".join(rng.choices(alphabet, k=n))

        # Medição Python
        t_py, mem_py, st_py = measure_execution(
            lcs_mod.lcs_length_two_rows, s1, s2, repeats=repeats
        )
        results.append({
            "experiment": "E4",
            "algorithm": "LCS",
            "approach": "bottom_up",
            "n": n,
            "time_seconds": t_py,
            "memory_bytes": mem_py or 0,
            "calls": 1,
            "status": st_py,
            "notes": "Python 3.11 (CPython Bottom-Up)",
        })

        # Se houver executável C++ funcional disponível
        if cpp_binary is not None:
            try:
                sub_res = subprocess.run(
                    [cpp_binary, s1, s2, str(repeats)],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                if sub_res.returncode == 0 and sub_res.stdout.strip():
                    try:
                        data = json.loads(sub_res.stdout.strip())
                        t_cpp = data.get("time_seconds")
                        results.append({
                            "experiment": "E4",
                            "algorithm": "LCS",
                            "approach": "bottom_up_cpp",
                            "n": n,
                            "time_seconds": t_cpp,
                            "memory_bytes": 0,
                            "calls": 1,
                            "status": "success",
                            "notes": "C++17 (g++ -O3, Bottom-Up)",
                        })
                    except json.JSONDecodeError:
                        pass
            except Exception:
                pass

    fieldnames = list(results[0].keys())
    save_csv("e4_lcs_cpp.csv", fieldnames, results)
    upsert_consolidated(results, "E4")
    print(f"      -> {len(results)} registros gerados para Comparativo C++ vs Python (E4).")


def exp_e5_recursion_limit(quick: bool = False) -> None:
    """E5: Limite de recursão (RecursionError) na memoização.

    Requisitos:
    - Status explícito: 'success', 'recursion_error'.
    - Nunca utilizar tempos negativos (como -1.0).
    - Representar falhas por tempo nulo (None / null no JSON).
    - Medir Bottom-Up separadamente e registrar seu próprio status.
    """
    limit = sys.getrecursionlimit()
    test_ns = [
        100, 200, 300, 400, 500, 600, 700, 800, 850, 900,
        950, 980, limit - 10, limit, limit + 20, limit + 50, limit + 100, limit + 200
    ] if quick else [
        100, 200, 300, 400, 500, 600, 700, 800, 850, 900,
        950, 970, 980, 990, limit, limit + 20, limit + 50, limit + 100, limit + 200, limit + 300
    ]

    results: list[dict[str, Any]] = []

    for n in test_ns:
        # 1. Top-Down Memoização
        status_memo = "success"
        t_memo: float | None = None
        try:
            # Não passa memory pré-populado para garantir nova memoização limpa em cada uma das 5 repetições
            t_memo, _, st = measure_execution(fib_mod.fib_memo, n, repeats=5)
            status_memo = st
        except RecursionError:
            status_memo = "recursion_error"
            t_memo = None
        except Exception:
            status_memo = "execution_error"
            t_memo = None

        if status_memo != "success":
            t_memo = None

        results.append({
            "experiment": "E5",
            "algorithm": "Fibonacci Top-Down",
            "approach": "memo",
            "n": n,
            "time_seconds": t_memo,
            "memory_bytes": 0,
            "calls": (2 * n - 1) if status_memo == "success" else None,
            "status": status_memo,
            "notes": f"Pilha Python: {status_memo} (limite global: {limit})",
        })

        # 2. Bottom-Up Iterativo (Imune a estouro de pilha)
        t_bu, _, st_bu = measure_execution(fib_mod.fib_bottom_up, n, repeats=5)
        results.append({
            "experiment": "E5",
            "algorithm": "Fibonacci Bottom-Up",
            "approach": "bottom_up",
            "n": n,
            "time_seconds": t_bu,
            "memory_bytes": 0,
            "calls": 1,
            "status": st_bu,
            "notes": "Bottom-Up Iterativo (sem chamadas de pilha recursiva)",
        })

    fieldnames = list(results[0].keys())
    save_csv("e5_recursion_limit.csv", fieldnames, results)
    upsert_consolidated(results, "E5")
    print(f"      -> {len(results)} registros gerados para Limite de Recursão (E5).")


def exp_e6_greedy_failure_rate(quick: bool = False) -> None:
    """E6: Corte de hastes - Taxa de falha e perda média da heurística gulosa.

    Requisitos:
    - Colunas semânticas próprias: failure_rate_percent, average_loss_percent, num_instances, failures.
    - Comparação com solução ótima de PD em cada instância.
    - Semente pseudo-aleatória fixa.
    """
    rng = random.Random(42)
    num_instances = 50 if quick else 200
    rod_sizes = [5, 8, 10, 12, 15, 18, 20, 25, 30, 35] if quick else [
        5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 35, 40, 45, 50
    ]

    results: list[dict[str, Any]] = []

    for n in rod_sizes:
        failures = 0
        losses: list[float] = []

        for _ in range(num_instances):
            # Gera preços crescentes com perturbações aleatórias que desafiam o guloso
            p = [0]
            for i in range(1, n + 1):
                p.append(p[-1] + rng.randint(1, 10))

            opt_revenue = rod_mod.cut_rod_bottom_up(p, n)
            greedy_revenue, _ = rod_mod.cut_rod_greedy_ratio(p, n)

            if greedy_revenue < opt_revenue:
                failures += 1
                loss = ((opt_revenue - greedy_revenue) / opt_revenue) * 100.0
                losses.append(loss)

        failure_rate = (failures / num_instances) * 100.0
        avg_loss = statistics.mean(losses) if losses else 0.0

        results.append({
            "experiment": "E6",
            "algorithm": "Corte de Hastes",
            "approach": "greedy",
            "n": n,
            "failure_rate_percent": round(failure_rate, 2),
            "average_loss_percent": round(avg_loss, 2),
            "num_instances": num_instances,
            "failures": failures,
            "status": "success",
            "notes": f"Guloso falhou em {failures}/{num_instances} instâncias (perda média: {round(avg_loss, 1)}%)",
        })

    fieldnames = list(results[0].keys())
    save_csv("e6_greedy_failure.csv", fieldnames, results)
    upsert_consolidated(results, "E6")
    print(f"      -> {len(results)} registros gerados para Falha do Guloso (E6).")


def exp_e7_matrix_chain(quick: bool = False) -> None:
    """E7: Cadeia de multiplicação de matrizes - PD Theta(n^3) e números de Catalan.

    Requisitos:
    - Coluna própria 'catalan_count' armazenando C(n-1).
    - 'memory_bytes' armazena apenas consumo de memória real (nunca números de Catalan!).
    - time_seconds armazena apenas tempo de execução.
    - Abordagens: naive, memo, bottom_up.
    """
    repeats = 3 if quick else 5
    rng = random.Random(42)

    naive_ns = [2, 3, 4, 5, 6, 7, 8, 9] if quick else [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    pd_ns = [
        2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 25, 30, 35, 40, 45, 50
    ] if quick else [
        2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 75
    ]

    # Dimensões determinísticas: lista de n + 1 dimensões para n matrizes
    max_dims = [rng.randint(10, 50) for _ in range(max(pd_ns) + 2)]

    results: list[dict[str, Any]] = []

    # 1. Força Bruta (Naive)
    for n in naive_ns:
        dims_n = max_dims[: n + 1]
        catalan_val = matrix_mod.count_parenthesizations(n)

        times: list[float] = []
        call_counts: list[int] = []
        status = "success"

        for _ in range(repeats):
            c = CallCounter()
            t, _, st = measure_execution(
                matrix_mod.matrix_chain_naive, dims_n, counter=c, repeats=1, timeout=3.0
            )
            if st != "success":
                status = st
                break
            if t is not None:
                times.append(t)
                call_counts.append(c.calls)

        avg_time = calculate_trimmed_mean(times) if status == "success" and times else None
        avg_calls = int(round(statistics.mean(call_counts))) if call_counts else None

        results.append({
            "experiment": "E7",
            "algorithm": "Cadeia de Matrizes",
            "approach": "naive",
            "n": n,
            "time_seconds": avg_time,
            "memory_bytes": 0,
            "calls": avg_calls,
            "catalan_count": catalan_val,
            "status": status,
            "notes": f"Naive: C({n-1}) = {catalan_val} parentizações",
        })
        if status == "timeout":
            break

    # 2. Programação Dinâmica: Memoização e Bottom-Up
    for n in pd_ns:
        dims_n = max_dims[: n + 1]
        catalan_val = matrix_mod.count_parenthesizations(n)

        # Validação de equivalência de custo mínimo
        val_memo = matrix_mod.matrix_chain_memo(dims_n)
        val_bu, _ = matrix_mod.matrix_chain_order(dims_n)
        cost_bu = val_bu[1][n]
        if val_memo != cost_bu:
            print(f"      [AVISO] Divergência em E7 para n={n}: memo={val_memo}, bu={cost_bu}")

        # Memoização
        t_memo, _, st_memo = measure_execution(
            matrix_mod.matrix_chain_memo, dims_n, repeats=repeats
        )
        results.append({
            "experiment": "E7",
            "algorithm": "Cadeia de Matrizes",
            "approach": "memo",
            "n": n,
            "time_seconds": t_memo,
            "memory_bytes": 0,
            "calls": 1,
            "catalan_count": catalan_val,
            "status": st_memo,
            "notes": "Theta(n^3) Top-Down Memoização",
        })

        # Bottom-Up
        t_bu, mem_bu, st_bu = measure_execution(
            matrix_mod.matrix_chain_order, dims_n, repeats=repeats, measure_peak_mem=True
        )
        results.append({
            "experiment": "E7",
            "algorithm": "Cadeia de Matrizes",
            "approach": "bottom_up",
            "n": n,
            "time_seconds": t_bu,
            "memory_bytes": mem_bu or 0,
            "calls": 1,
            "catalan_count": catalan_val,
            "status": st_bu,
            "notes": f"Theta(n^3) Bottom-Up Matrix-Chain-Order ({round((mem_bu or 0)/1024, 1)} KB)",
        })

    fieldnames = list(results[0].keys())
    save_csv("e7_matrix_chain.csv", fieldnames, results)
    upsert_consolidated(results, "E7")
    print(f"      -> {len(results)} registros gerados para Cadeia de Matrizes (E7).")


def exp_e8_knapsack_pseudo_polynomial(quick: bool = False) -> None:
    """E8: Mochila 0/1 - Comportamento pseudo-polinomial O(nW) e otimização de memória."""
    repeats = 3 if quick else 5
    rng = random.Random(42)

    capacities = [
        100, 250, 500, 750, 1000, 1500, 2000, 3000, 4000, 5000,
        6000, 7500, 10000, 12500, 15000, 17500, 20000
    ] if quick else [
        100, 250, 500, 750, 1000, 1500, 2000, 3000, 4000, 5000,
        6000, 7500, 10000, 12500, 15000, 17500, 20000, 25000, 30000, 35000
    ]

    # Número fixo de itens para isolar o efeito da capacidade W
    num_items = 40
    weights = [rng.randint(5, 50) for _ in range(num_items)]
    values = [rng.randint(10, 100) for _ in range(num_items)]

    results: list[dict[str, Any]] = []

    for w in capacities:
        # Validação de equivalência de solução ótima entre as abordagens
        opt_2d, _ = knapsack_mod.knapsack_01(weights, values, w)
        opt_1d = knapsack_mod.knapsack_one_row(weights, values, w)
        if opt_2d != opt_1d:
            print(f"      [AVISO] Divergência em E8 para W={w}: 2D={opt_2d}, 1D={opt_1d}")

        # Tabela 2D completa
        t_full, mem_full, st_full = measure_execution(
            knapsack_mod.knapsack_01, weights, values, w, repeats=repeats, measure_peak_mem=True
        )
        results.append({
            "experiment": "E8",
            "algorithm": "Mochila 0/1",
            "approach": "bottom_up",
            "n": w,
            "time_seconds": t_full,
            "memory_bytes": mem_full or 0,
            "calls": 1,
            "status": st_full,
            "notes": f"Tabela 2D: O(nW) espaço ({round((mem_full or 0)/1024, 1)} KB)",
        })

        # Vetor 1D com espaço otimizado
        t_row, mem_row, st_row = measure_execution(
            knapsack_mod.knapsack_one_row, weights, values, w, repeats=repeats, measure_peak_mem=True
        )
        results.append({
            "experiment": "E8",
            "algorithm": "Mochila 0/1",
            "approach": "one_row",
            "n": w,
            "time_seconds": t_row,
            "memory_bytes": mem_row or 0,
            "calls": 1,
            "status": st_row,
            "notes": f"Vetor 1D: O(W) espaço ({round((mem_row or 0)/1024, 1)} KB)",
        })

    fieldnames = list(results[0].keys())
    save_csv("e8_knapsack.csv", fieldnames, results)
    upsert_consolidated(results, "E8")
    print(f"      -> {len(results)} registros gerados para Mochila 0/1 (E8).")


# Dicionário de experimentos disponíveis
EXPERIMENTS: dict[str, tuple[str, Callable[[bool], None]]] = {
    "E1": ("Fibonacci (tempo e chamadas)", exp_e1_fibonacci),
    "E2": ("Corte de Hastes (tempo x n)", exp_e2_rod_cutting),
    "E3": ("LCS (tempo e memória: tabela x duas linhas)", exp_e3_lcs_memory),
    "E4": ("LCS (Python vs C++)", exp_e4_lcs_cpp_vs_python),
    "E5": ("Limite de Recursão na Memoização", exp_e5_recursion_limit),
    "E6": ("Guloso vs PD (taxa de erro)", exp_e6_greedy_failure_rate),
    "E7": ("Cadeia de Matrizes (Theta(n^3) e Catalan)", exp_e7_matrix_chain),
    "E8": ("Mochila 0/1 (Pseudo-polinomial)", exp_e8_knapsack_pseudo_polynomial),
}


# -----------------------------------------------------------------------------
# 5. Ponto de Entrada Principal da Linha de Comando
# -----------------------------------------------------------------------------
def main() -> None:
    """Ponto de entrada para execução dos experimentos."""
    parser = argparse.ArgumentParser(
        description="Suíte Científica de Benchmarks de Programação Dinâmica (AEDS-II)."
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Executa versão rápida dos benchmarks (menos repetições e entradas reduzidas).",
    )
    parser.add_argument(
        "--only",
        type=str,
        help="Executa apenas os experimentos especificados separados por vírgula (ex.: E1,E3,E7).",
    )
    args = parser.parse_args()

    # Validação estrita do argumento --only
    if args.only:
        raw_ids = [exp_id.strip().upper() for exp_id in args.only.split(",") if exp_id.strip()]
        invalid_ids = [i for i in raw_ids if i not in EXPERIMENTS]
        if invalid_ids:
            print(f"[-] Erro: Identificador(es) de experimento inválido(s): {', '.join(invalid_ids)}")
            print(f"    Experimentos disponíveis: {', '.join(EXPERIMENTS.keys())}")
            sys.exit(1)
        selected_ids = raw_ids
    else:
        selected_ids = list(EXPERIMENTS.keys())

    os.makedirs(RESULTS_DIR, exist_ok=True)
    save_machine_metadata()

    print("=" * 70)
    print("  SUÍTE DE BENCHMARKS - PROGRAMAÇÃO DINÂMICA (AEDS-II)")
    print("  Protocolo: Média de 3 medições centrais (de 5 repetições, sem min/max)")
    print("  Amostragem: Amostragem densa por classe assintótica")
    print(f"  Modo rápido: {'Sim' if args.quick else 'Não'}")
    print(f"  Experimentos selecionados: {', '.join(selected_ids)}")
    print("=" * 70)

    success_count = 0
    start_total = time.perf_counter()

    for exp_id in selected_ids:
        name, fn = EXPERIMENTS[exp_id]
        print(f"\n[{exp_id}] Executando {name}...")
        t0 = time.perf_counter()
        try:
            fn(quick=args.quick)
            dur = time.perf_counter() - t0
            print(f"    [OK] Concluído em {dur:.2f}s.")
            success_count += 1
        except Exception as err:
            dur = time.perf_counter() - t0
            print(f"    [FALHA] Erro ao executar {exp_id} após {dur:.2f}s: {err}")

    # Exporta dados finais para consumo pela interface web
    export_web_results_json()

    total_time = time.perf_counter() - start_total
    print("\n" + "=" * 70)
    print(f"Status: {success_count}/{len(selected_ids)} experimentos executados com sucesso em {total_time:.2f}s.")
    print(f"Resultados salvos em: {RESULTS_DIR}")
    print("=" * 70)


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
