# Tarefa P4: Estudos de Caso Práticos, Benchmarks Empíricos, C++ e Seção 5

**Responsável:** Integrante P4  
**Foco:** Aplicações do mundo real (Diff e DNA), medições científicas de desempenho (tempo e memória), implementação em C++17 e redação da Seção 5.

---

## 1. Objetivo
Desenvolver as ferramentas práticas de estudo de caso, implementar a suíte completa de experimentos automatizados (`benchmarks/run_benchmarks.py`), gerar gráficos científicos com visual consistente (`benchmarks/plot_results.py`), implementar o comparativo em C++17 (`cpp/lcs.cpp`) e redigir a Seção 5 do relatório técnico com a discussão crítica dos dados empíricos.

---

## 2. Arquivos que você edita
* [`src/case_study/diff_tool.py`](../../src/case_study/diff_tool.py)
* [`src/case_study/dna_alignment.py`](../../src/case_study/dna_alignment.py)
* [`benchmarks/run_benchmarks.py`](../../benchmarks/run_benchmarks.py)
* [`benchmarks/plot_results.py`](../../benchmarks/plot_results.py)
* [`cpp/lcs.cpp`](../../cpp/lcs.cpp)
* [`relatorio/secoes/05_estudo_de_caso.tex`](../../relatorio/secoes/05_estudo_de_caso.tex)
* [`web/data/results.json`](../../web/data/results.json)
* [`README.md`](../../README.md) (seções de Resultados e Gargalos Observados)

---

## 3. Passo a Passo (Checklist)

- [ ] **Estudos de Caso Práticos:**
  - Em `src/case_study/diff_tool.py`:
    * Implementar `diff_lines(a_lines, b_lines)` aplicando LCS com linhas como elementos para gerar saída unificada com marcadores `"  "`, `"+ "`, `"- "`.
    * Testar com os arquivos reais `data/texto_a.txt` e `data/texto_b.txt`.
  - Em `src/case_study/dna_alignment.py`:
    * Implementar `edit_distance(a, b)` (Levenshtein) com custos unitários.
    * Implementar `align(a, b)` realizando o traceback global com inserção de gaps (`-`).
    * Testar com `data/dna_a.fasta` e `data/dna_b.fasta`.
  - Executar `make test` e garantir que a suíte `test_case_study.py` passa com sucesso.

- [ ] **Implementação do LCS em C++17 (`cpp/lcs.cpp`):**
  - Implementar o algoritmo LCS Bottom-Up em C++17 de forma eficiente com `std::vector<std::vector<int>>` ou array plano contíguo.
  - Aceitar strings ou tamanhos via linha de comando e reportar tempo decorrido via `std::chrono::high_resolution_clock`.
  - Garantir compilação limpa com `make cpp`.

- [ ] **Runner de Benchmarks Científicos (`benchmarks/run_benchmarks.py`):**
  - Configurar protocolo rigoroso: mediana de 5 repetições, semente aleatória fixa (`random.seed(42)`), medição de tempo com `time.perf_counter` e memória com `tracemalloc`.
  - Implementar corte de segurança (timeout de 10s) para as abordagens ingênuas exponenciais.
  - Gerar arquivo de metadados do ambiente `benchmarks/results/machine.json` registrando processador, clock, memória RAM, SO e versões do Python/g++.
  - Preencher as funções para todos os experimentos planejados:
    * **E1**: Fibonacci - tempo e chamadas recursivas ($\text{Naive } \Theta(2^n)$ vs. $\text{PD } \Theta(n)$).
    * **E2**: Corte de Hastes - tempo vs. $n$ ($\text{Naive } \Theta(2^n)$ vs. $\text{PD } \Theta(n^2)$).
    * **E3**: LCS - tempo e pico de memória ($\Theta(m \cdot n)$ tabela completa vs. $\Theta(\min(m, n))$ duas linhas).
    * **E4**: LCS - Comparativo de Linguagem (Python vs. C++17).
    * **E5**: Limite de Recursão do Python - estouro de pilha (`RecursionError`) na memoização.
    * **E6**: Guloso vs. PD no corte de hastes - % de contra-exemplos onde o guloso falha.
    * **E7**: Cadeia de Matrizes - tempo da PD $\Theta(n^3)$ vs. crescimento dos números de Catalan $C(n-1)$.
    * **E8 (Opcional)**: Mochila 0/1 - tempo vs. capacidade $W$ (pseudo-polinomial).
  - Exportar os dados consolidados em CSV para `benchmarks/results/` e em formato JSON para `web/data/results.json`.

- [ ] **Geração de Gráficos Científicos (`benchmarks/plot_results.py`):**
  - Salvar figuras em PNG com resolução de 200 DPI em `docs/figures/` e `relatorio/figuras/`.
  - Utilizar eixos e legendas totalmente em Português do Brasil.
  - Empregar escala logarítmica (semilog ou log-log) onde houver contraste exponencial x polinomial.
  - Respeitar a paleta de cores imutável do projeto:
    * Ingênuo: Vermelho `#d62728`
    * Memoização: Azul `#1f77b4`
    * Bottom-Up: Verde `#2ca02c`
    * Duas Linhas: Roxo `#9467bd`
    * Guloso: Cinza `#7f7f7f`

- [ ] **Redação da Seção 5 do Relatório e README:**
  - Redigir `relatorio/secoes/05_estudo_de_caso.tex` com a interpretação científica dos gráficos.
  - Atualizar a seção de "Resultados" e "Gargalos Observados" no `README.md` com números e constatações reais.
  - Discutir os gargalos observados: limite de recursão no Python, localidade de cache em matrizes, gargalo de interpretação frente ao código C++ nativo e footprint de memória.

---

## 4. Critério de Pronto
* `make bench` e `make bench-quick` executam do início ao fim sem erros, gerando arquivos de dados reais.
* Gráficos em alta resolução (200 DPI) gerados e referenciados no relatório.
* **Nenhum número de benchmark ou resultado foi inventado.**

---

## 5. Dicas Úteis
* Para o experimento E4, use o módulo `subprocess` do Python para invocar `./cpp/lcs` passando os mesmos parâmetros e capturando o tempo de execução.
* Para medir memória com precisão, chame `tracemalloc.start()` e `tracemalloc.get_traced_memory()` imediatamente antes e depois do algoritmo.

---

## 6. Avise Quando Terminar
* Avise **P5** assim que `web/data/results.json` estiver populado, para que a página `benchmarks.html` exiba os dados reais.
* Avise **P1** quando a Seção 5 do relatório estiver escrita para a integração final.
