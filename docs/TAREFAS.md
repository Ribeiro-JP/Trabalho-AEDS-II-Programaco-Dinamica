# Quadro de Tarefas da Equipe - Programação Dinâmica (AEDS-II)

Este documento centraliza as responsabilidades de cada integrante, as dependências de trabalho e o checklist operacional simplificado.

---

## 1. Distribuição de Responsabilidades da Equipe

| Integrante | Papel Principal | Frentes de Trabalho |
| :--- | :--- | :--- |
| **João Gabriel** | **Relatório Técnico Completo & Coordenação** | Redação integral das Seções 1 a 6 em LaTeX no Overleaf (introdução, fundamentação, pseudocódigos `algorithm2e`, TikZ, análise assintótica, interpretação dos resultados de Alisson e conclusões). |
| **João Pedro** | **Códigos de Referência (Python & C++)** | Implementação das 4 versões de Fibonacci, Corte de Hastes, Cadeia de Matrizes, LCS, estudos de caso (Diff e DNA) e o binário C++17 (`cpp/lcs.cpp`). |
| **Alisson** | **Benchmarks, Resultados & Web** | Execução dos benchmarks empíricos (E1 a E8), geração dos gráficos a 200 DPI, criação das páginas web interativas em `web/` e documentação de resultados no `README.md`. |
| **Carlos** | **Apresentação & Slides (40 min)** | Construção dos slides do seminário (Google Slides, PowerPoint, Canva ou Beamer) seguindo o roteiro de 5 blocos e as dinâmicas interativas da aula. |
| **Paulo** | **Cheat Sheet & Apoio Web** | Elaboração do Cheat Sheet de 1 a 2 páginas em LaTeX (`cheatsheet/`) e auxílio para Alisson no desenvolvimento do portal web interativo. |

---

## 2. Checklist por Integrante

### João Pedro (Código Base em Python e C++)
* [ ] Implementar `src/fibonacci.py` (Naive, Memo, Bottom-Up, $O(1)$ Espaço).
* [ ] Implementar `src/rod_cutting.py` (Corte de Hastes, Reconstrução e Heurística Gulosa).
* [ ] Implementar `src/matrix_chain.py` (Multiplicação em Cadeia de Matrizes, Parentização Ótima e Catalan).
* [ ] Implementar `src/lcs.py` (Subsequência Comum Máxima, Traceback, Otimização de duas linhas e Formatação).
* [ ] Apoiar nos estudos de caso: `src/case_study/diff_tool.py` e `src/case_study/dna_alignment.py`.
* [ ] Implementar o algoritmo LCS Bottom-Up em C++17 em `cpp/lcs.cpp` (compilável via `make cpp`).
* [ ] Garantir que `make test` passe em todos os testes unitários sem `SKIPPED`.

### Alisson (Benchmarks, Resultados e Web)
* [ ] Implementar o runner científico `benchmarks/run_benchmarks.py` (mediana de 5 execuções, semente fixa e `tracemalloc`).
* [ ] Executar os experimentos empíricos E1 a E7 (E8 opcional), gerando os dados em `benchmarks/results/` e o consolidado `web/data/results.json`.
* [ ] Gerar os gráficos padronizados em 200 DPI com `benchmarks/plot_results.py` em `docs/figures/`.
* [ ] Programar as páginas interativas em `web/`:
  - `web/fib-tree.html` (árvore com slider e memoização).
  - `web/rod-cutting-duel.html` (comparativo guloso vs. PD com tabela editável).
  - `web/matrix-chain.html` (preenchimento por diagonais das tabelas $m$ e $s$).
  - `web/lcs-table.html` (matriz animada com setas de traceback).
  - `web/benchmarks.html` (gráficos interativos lendo `data/results.json`).
  - `web/quiz.html` (quiz conceitual de 8 perguntas).
* [ ] Atualizar o `README.md` raiz com os dados e conclusões de benchmark obtidos.

### Carlos (Slides e Seminário)
* [ ] Consultar o roteiro minuto a minuto em [`docs/ROTEIRO_SLIDES.md`](ROTEIRO_SLIDES.md).
* [ ] Estruturar a apresentação em 5 blocos bem definidos (0 a 7 min, 7 a 18 min, 18 a 25 min, 25 a 33 min, 33 a 40 min).
* [ ] Incorporar as dinâmicas interativas recomendadas (aposta do Fibonacci, problema do corte de barra, voluntários multiplicando matrizes).
* [ ] Alinhar com o grupo quem fala em cada bloco e guardar o arquivo final e o PDF em `slides/`.

### Paulo (Cheat Sheet e Apoio Web)
* [ ] Preencher os 4 blocos obrigatórios em `cheatsheet/cheatsheet_body.tex`:
  - 1. Definição essencial em uma frase.
  - 2. Diagrama de decisão em TikZ ("Quando utilizar esta abordagem?").
  - 3. Tabela comparativa de complexidades de tempo e espaço.
  - 4. Padrões de pseudocódigo Top-Down vs. Bottom-Up.
* [ ] Conferir que `cheatsheet/cheatsheet.tex` compila perfeitamente em 1 a 2 páginas.
* [ ] Auxiliar Alisson no desenvolvimento do front-end das páginas interativas em `web/`.

### João Gabriel (Relatório Técnico Completo e Coordenação Geral)
* [ ] Subir o projeto no Overleaf e conferir a compilação de `relatorio/main.tex`.
* [ ] Redigir Seção 1 (Introdução em modelo funil).
* [ ] Redigir Seção 2 (Fundamentação teórica formal, prova de cortar e colar, superposição de subproblemas e números de Catalan).
* [ ] Redigir Seção 3 (Modelagem algorítmica em `algorithm2e` e diagramas em TikZ).
* [ ] Redigir Seção 4 (Análise assintótica rigorosa com $O, \Omega, \Theta$).
* [ ] Redigir Seção 5 (Estudos de caso reais e análise dos gráficos gerados por Alisson).
* [ ] Redigir Seção 6 (Conclusões, limitações da técnica, mochila pseudo-polinomial e problemas NP-difíceis).
* [ ] Coordenar a revisão final cruzada antes da entrega e da apresentação.

---

## 3. Resumo Teórico da Cadeia de Matrizes (Cormen 15.2)

* **O Problema:** Dadas $n$ matrizes com dimensões `dims = [p0, p1, ..., pn]`, encontrar a parentização que minimiza o número de multiplicações escalares.
* **Recorrência:** 
  $$m[i, i] = 0$$
  $$m[i, j] = \min_{i \le k < j} \{ m[i, k] + m[k+1, j] + p_{i-1} \cdot p_k \cdot p_j \}$$
* **Ordem de Preenchimento:** Por diagonais sucessivas (comprimento de subcadeia $l = 2 \dots n$), e não linha a linha.
* **Explosão de Catalan:** $n$ matrizes possuem $P(n) = C(n-1) = \frac{1}{n}\binom{2n-2}{n-1}$ parentizações possíveis, crescendo como $\Omega(4^n / n^{3/2})$. Para 6 matrizes são 42; para 15 são mais de 2,6 milhões.
* **Complexidade:** Tempo $\Theta(n^3)$ e Espaço $\Theta(n^2)$.
* **Instância Oficial do Cormen:** `dims = [30, 35, 15, 5, 10, 20, 25]` (6 matrizes) $\to$ custo mínimo **15.125** multiplicações e parentização ótima `((A1(A2A3))((A4A5)A6))`.
