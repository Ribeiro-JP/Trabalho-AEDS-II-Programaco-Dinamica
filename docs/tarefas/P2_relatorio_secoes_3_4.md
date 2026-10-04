# Tarefa P2: Relatório Técnico (Seções 3 e 4), Pseudocódigos, Diagramas TikZ e Análise Assintótica

**Responsável:** Integrante P2  
**Foco:** Modelagem formal dos algoritmos em `algorithm2e`, criação de diagramas em TikZ e demonstrações matemáticas assintóticas ($O, \Omega, \Theta$).

---

## 1. Objetivo
Escrever as Seções 3 (Paradigma Algorítmico) e 4 (Análise Assintótica) do relatório técnico em LaTeX, incluindo pseudocódigos rigorosos, ilustrações conceituais em TikZ obrigatórias pelo enunciado e a tabela-resumo de complexidades que alimentará o Cheat Sheet de P5.

---

## 2. Arquivos que você edita
* [`relatorio/secoes/03_paradigma.tex`](../../relatorio/secoes/03_paradigma.tex)
* [`relatorio/secoes/04_analise.tex`](../../relatorio/secoes/04_analise.tex)
* [`relatorio/tikz/`](../../relatorio/tikz/) (novos arquivos `.tikz` ou `.tex` incluídos no relatório)
* [`relatorio/figuras/`](../../relatorio/figuras/)

---

## 3. Passo a Passo (Checklist)

- [ ] **Pseudocódigos Completos com `algorithm2e`:**
  - **Fibonacci:**
    * `Fib-Naive(n)` (recursivo puro)
    * `Memoized-Fib(n, memo)` (com dicionário/vetor)
    * `Bottom-Up-Fib(n)` (preenchimento iterativo linear)
  - **Corte de Hastes (Cormen 15.1):**
    * `Cut-Rod(p, n)`
    * `Memoized-Cut-Rod(p, n)` e rotina auxiliar `Memoized-Cut-Rod-Aux(p, n, r)`
    * `Bottom-Up-Cut-Rod(p, n)`
    * `Extended-Bottom-Up-Cut-Rod(p, n)` (devolvendo receitas $r$ e escolhas $s$)
    * `Print-Cut-Rod-Solution(p, n)` (reconstrução dos cortes)
  - **Cadeia de Matrizes (Cormen 15.2):**
    * `Matrix-Chain-Order(p)` (laço triplo por diagonais $l = 2..n$)
    * `Print-Optimal-Parens(s, i, j)` (reconstrução recursiva)
  - **Subsequência Comum Máxima - LCS (Cormen 15.4):**
    * `LCS-Length(X, Y)` (preenchimento das matrizes $c$ e $b$)
    * `Print-LCS(b, X, i, j)` (traceback da sequência)

- [ ] **Diagramas Conceituais em TikZ (Obrigatórios no enunciado):**
  - [ ] **Diagrama (a):** Árvore de recursão do `Cut-Rod` para $n = 4$, colorindo nós repetidos para evidenciar a explosão combinatória redundante.
  - [ ] **Diagrama (b):** Matriz de programação dinâmica do LCS para as sequências `"ABCBDAB"` e `"BDCABA"` com setas de traceback direcionais.
  - [ ] **Diagrama (c):** Grafo direcionado acíclico (DAG) de dependências dos subproblemas do corte de haste ou cadeia de matrizes.
  - [ ] **Diagrama (d):** Tabelas $m$ e $s$ preenchidas para o exemplo oficial do Cormen ($dims = [30, 35, 15, 5, 10, 20, 25]$).
  - [ ] **Diagrama (e - opcional):** Estado da pilha e tabela durante a execução da memoização.

- [ ] **Análise Assintótica Rigorosa (Tempo e Espaço):**
  - **Método Fundamental da PD:** Explicar a fórmula $\text{Tempo} = \sum (\text{número de subproblemas}) \times (\text{custo de transição})$.
  - **Prova do Corte Ingênuo:** Provar por indução matemática que a recorrência $T(n) = 1 + \sum_{j=0}^{n-1} T(j)$ resulta em $T(n) = 2^n = \Theta(2^n)$.
  - **Deduções:**
    * Corte de Hastes Bottom-Up: $\Theta(n^2)$ tempo e $\Theta(n)$ espaço.
    * Cadeia de Matrizes: demonstrar o laço triplo somando $\sum_{l=2}^n (n-l+1)(l-1) = \Theta(n^3)$ tempo e $\Theta(n^2)$ espaço.
    * LCS: demonstrar $\Theta(m \cdot n)$ tempo e espaço, e a otimização para $\Theta(\min(m, n))$ espaço mantendo apenas duas linhas.

- [ ] **Tabela-Resumo Oficial de Complexidades:**
  - Sintetizar todas as complexidades em uma tabela formal usando `booktabs`, comparando ingênuo x memoização x bottom-up x espaço.
  - Disponibilizar esses dados para P5 transpor para o Cheat Sheet.

---

## 4. Critério de Pronto
* Todos os algoritmos citados estão formalizados em `algorithm2e` com indentação e comentários.
* Os diagramas TikZ compilam perfeitamente sem sobreposição de nós ou textos ilegíveis.
* Todas as análises assintóticas possuem notação matemática estrita ($O, \Omega, \Theta$) e justificativa teórica.

---

## 5. Dicas Úteis
* Para TikZ, teste compilar pequenos blocos isolados antes de inserir no `main.tex`.
* Mantenha as mesmas cores padronizadas nos nós do TikZ (ingênuo vermelho `#d62728`, memo azul `#1f77b4`, bottom-up verde `#2ca02c`).

---

## 6. Avise Quando Terminar
* Avise **P5** assim que a tabela de complexidades estiver fechada, pois ela é necessária para o Cheat Sheet.
* Avise **P1** quando as seções 3 e 4 estiverem prontas para a costura com a introdução e fundamentação.
