# Tarefa P3: Implementação do Código Base dos Algoritmos (Python)

**Responsável:** Integrante P3  
**Foco:** Implementação limpa, eficiente e tipada dos algoritmos centrais do Cormen até a suíte de testes passar 100%.

---

## 1. Objetivo
Preencher os stubs de código Python em `src/`, transformando os esqueletos com `raise NotImplementedError` em código funcional de referência que satisfaça todos os testes unitários já escritos em `tests/`.

---

## 2. Arquivos que você edita
* [`src/fibonacci.py`](../../src/fibonacci.py)
* [`src/rod_cutting.py`](../../src/rod_cutting.py)
* [`src/matrix_chain.py`](../../src/matrix_chain.py)
* [`src/lcs.py`](../../src/lcs.py)
* [`src/knapsack.py`](../../src/knapsack.py) *(opcional)*

> [!WARNING]
> **Contrato de Código:** As assinaturas das funções, nomes de parâmetros e tipos de retorno já definidos nos stubs são um **contrato** com os demais integrantes e com os testes unitários. **Não altere as assinaturas** sem aviso prévio à equipe!

---

## 3. Passo a Passo (Checklist e Ordem Obrigatória)

Execute na ordem abaixo. Faça **commit e push** ao concluir cada módulo para que P4 e P5 possam começar a consumir seu código imediatamente.

- [ ] **Módulo 1: Fibonacci (`src/fibonacci.py`)**
  - Implementar `fib_naive(n, counter)` com suporte ao `CallCounter`.
  - Implementar `fib_memo(n, counter)` (usando dicionário ou lista de cache).
  - Implementar `fib_bottom_up(n)` (preenchendo vetor de tamanho $n+1$).
  - Implementar `fib_o1_space(n)` (armazenando apenas os dois termos anteriores).
  - Executar `make test` e verificar se os testes de Fibonacci deixam de ser `SKIPPED` e passam como **`PASSED`**.
  - *Commit:* `feat(p3): implementa algoritmos de fibonacci`

- [ ] **Módulo 2: Corte de Hastes (`src/rod_cutting.py`)**
  - Implementar `cut_rod_naive(p, n, counter)`.
  - Implementar `cut_rod_memo(p, n, counter)`.
  - Implementar `cut_rod_bottom_up(p, n)`.
  - Implementar `cut_rod_extended(p, n)` devolvendo a tupla `(receita, s)`.
  - Implementar `reconstruct_cuts(s, n)` retornando a lista de pedaços da solução ótima.
  - Implementar `cut_rod_greedy_ratio(p, n)` com a heurística de densidade de valor ($p_i / i$) para fins comparativos.
  - Executar `make test` e garantir passagem em todos os testes do corte de hastes.
  - *Commit:* `feat(p3): implementa corte de hastes e heuristica gulosa`

- [ ] **Módulo 3: Multiplicação em Cadeia de Matrizes (`src/matrix_chain.py`)**
  - Implementar `count_parenthesizations(n)` via fórmula dos números de Catalan $C(n-1)$.
  - Implementar `matrix_chain_naive(dims, counter)`.
  - Implementar `matrix_chain_memo(dims)`.
  - Implementar `matrix_chain_order(dims)` com laço triplo preenchendo as matrizes $m$ e $s$ por comprimento crescente $l = 2..n$.
  - Implementar `optimal_parens(s, i, j)` gerando a string formatada como `((A1(A2A3))((A4A5)A6))`.
  - Executar `make test` e verificar se os testes da cadeia de matrizes passam.
  - *Commit:* `feat(p3): implementa cadeia de matrizes e parentizacao otima`

- [ ] **Módulo 4: Subsequência Comum Máxima - LCS (`src/lcs.py`)**
  - Implementar `lcs_naive(x, y, counter)`.
  - Implementar `lcs_memo(x, y)`.
  - Implementar `lcs_table(x, y)` retornando as matrizes $c$ (comprimentos) e $b$ (direções de traceback).
  - Implementar `lcs_string(x, y)` realizando a reconstrução da LCS.
  - Implementar `lcs_length_two_rows(x, y)` com otimização de espaço para $\Theta(\min(m, n))$.
  - Implementar `format_table(c, x, y)` gerando visualização em texto da grade.
  - Executar `make test` e garantir passagem em todos os testes do LCS.
  - *Commit:* `feat(p3): implementa lcs completo e otimizacao de duas linhas`

- [ ] **Módulo 5 (Opcional): Mochila 0/1 (`src/knapsack.py`)**
  - Se houver tempo disponível, implementar `knapsack_01` e `knapsack_one_row`.

---

## 4. Critério de Pronto
* `make test` executa sem falhas e **não resta nenhum teste com status `SKIPPED`** nos módulos de `fibonacci`, `rod_cutting`, `matrix_chain` e `lcs`.
* O código segue estritamente o PEP 8 e passa sem alertas de linter ou tipagem.

---

## 5. Dicas Úteis
* O `CallCounter` possui o método `counter.increment()`. Verifique sempre se `counter is not None` antes de incrementar.
* Atenção aos índices: na cadeia de matrizes do Cormen, as matrizes são indexadas de 1 a $n$. Ao criar matrizes em Python, você pode usar dimensão $(n+1) \times (n+1)$ para manter a indexação 1-baseada exatamente igual ao livro.

---

## 6. Avise Quando Terminar
* Avise **P4** a cada módulo pronto para que ele possa iniciar a coleta de dados de benchmarks imediatamente!
* Avise **P5** assim que `rod_cutting.py`, `matrix_chain.py` e `lcs.py` estiverem funcionais para a integração com as páginas web.
