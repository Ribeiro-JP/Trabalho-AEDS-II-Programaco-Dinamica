# Guia Especial: Multiplicação em Cadeia de Matrizes (Cormen Seção 15.2)

Este documento aprofunda o problema da **Cadeia de Matrizes**, obrigatório no projeto acadêmico, alinhando a teoria matemática, o preenchimento algorítmico, os testes de validação e a dinâmica de apresentação em sala.

---

## 1. O Problema
Dada uma sequência de $n$ matrizes $\langle A_1, A_2, \dots, A_n \rangle$, onde cada matriz $A_i$ possui dimensões $p_{i-1} \times p_i$ (representadas por um vetor `dims` de comprimento $n+1$), desejamos computar o produto:
$$A_1 \cdot A_2 \cdots A_n$$
efetuando o **mínimo número de multiplicações escalares**.

* **Propriedade da Multiplicação:** A multiplicação de matrizes é **associativa** ($ (A \cdot B) \cdot C = A \cdot (B \cdot C) $), logo qualquer parentização produzirá o mesmo resultado numérico.
* **Impacto no Custo:** A ordem escolhida altera dramaticamente o custo computacional.  
  *Exemplo:* Para $A_1 (10 \times 100)$, $A_2 (100 \times 5)$ e $A_3 (5 \times 50)$:
  * $(A_1 A_2) A_3$: $10 \times 100 \times 5 + 10 \times 5 \times 50 = 5.000 + 2.500 = \mathbf{7.500}$ multiplicações.
  * $A_1 (A_2 A_3)$: $100 \times 5 \times 50 + 10 \times 100 \times 50 = 25.000 + 50.000 = \mathbf{75.000}$ multiplicações (10 vezes mais custoso!).

---

## 2. Por que Programação Dinâmica?
1. **Subestrutura Ótima:** Se a partição ótima de $A_i \dots A_j$ divide o produto em $A_i \dots A_k$ e $A_{k+1} \dots A_j$, então a parentização do prefixo $A_i \dots A_k$ deve ser ótima para esse subproblema, e a do sufixo $A_{k+1} \dots A_j$ também deve ser ótima. Prova-se por *"cortar e colar"* (se houvesse parentização melhor para qualquer dos lados, poderíamos colá-la e reduzir o custo total).
2. **Superposição de Subproblemas:** Ao calcular cadeias de diferentes tamanhos, as mesmas subcadeias $A_i \dots A_k$ reaparecem repetidamente em diferentes ramos da recursão.

---

## 3. Recorrência Matemática
Seja $m[i, j]$ o custo mínimo de multiplicações escalares para calcular $A_i \dots A_j$ (para $1 \le i \le j \le n$):

$$m[i, i] = 0 \quad (\forall i)$$

$$m[i, j] = \min_{i \le k < j} \left\{ m[i, k] + m[k+1, j] + p_{i-1} \cdot p_k \cdot p_j \right\} \quad (\text{para } i < j)$$

A tabela auxiliar $s[i, j]$ registra o índice $k$ que atingiu o valor mínimo, viabilizando a reconstrução da solução ótima.

---

## 4. Ordem de Preenchimento: Diagonais Crescentes
Diferente do problema do LCS (que pode ser preenchido linha a linha ou coluna a coluna), a cadeia de matrizes **exige preenchimento por comprimento crescente de subcadeia** ($l = 2, 3, \dots, n$):
1. Primeiro preenche-se a diagonal principal ($l = 1$: $m[i, i] = 0$).
2. Depois a diagonal de cadeias de tamanho $2$ ($l = 2$: $m[1, 2], m[2, 3], \dots$).
3. Sucessivamente até atingir o canto superior direito $m[1, n]$ ($l = n$).

Essa ordem garante que, quando formos avaliar $m[i, j]$, os valores menores $m[i, k]$ e $m[k+1, j]$ já estarão calculados e disponíveis na tabela.

---

## 5. Explosão Combinatória e Números de Catalan
O número total de maneiras distintas de parentizar o produto de $n$ matrizes é dado pelos **Números de Catalan** $C(n-1)$:

$$P(n) = C(n-1) = \frac{1}{n} \binom{2n - 2}{n - 1}$$

| $n$ (nº de matrizes) | $1$ | $2$ | $3$ | $4$ | $5$ | $6$ | $10$ | $15$ | $20$ |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **$P(n)$ parentizações** | 1 | 1 | 2 | 5 | 14 | **42** | 4.862 | 2.674.440 | 1.767.263.190 |

Como $P(n) = \Omega\left(\frac{4^n}{n^{3/2}}\right)$, uma busca exaustiva (força bruta) é computacionalmente impraticável mesmo para cadeias modestas ($n \ge 15$).

---

## 6. Complexidade Assintótica
* **Tempo:** $\Theta(n^3)$ — existem $\approx \frac{n^2}{2}$ subproblemas $(i, j)$, e para cada um avaliamos até $n$ pontos de partição $k$ (laço triplo).
* **Espaço:** $\Theta(n^2)$ — tabelas bidimensionais $m$ e $s$ de dimensões $(n+1) \times (n+1)$.

---

## 7. Exemplo Canônico do Cormen (Referência Oficial do Projeto)
Utilize este conjunto de dados em **todos os artefatos** (testes, relatório, gráficos, slides e web):

* **Dimensões:** `dims = [30, 35, 15, 5, 10, 20, 25]` ($n = 6$ matrizes)
  - $A_1: 30 \times 35$
  - $A_2: 35 \times 15$
  - $A_3: 15 \times 5$
  - $A_4: 5 \times 10$
  - $A_5: 10 \times 20$
  - $A_6: 20 \times 25$
* **Custo Mínimo:** $m[1, 6] = \mathbf{15.125}$ multiplicações escalares.
* **Parentização Ótima:** `((A1(A2A3))((A4A5)A6))`

---

## 8. Alocação entre os Integrantes
* **P3 (Código):** Implementar funções de `src/matrix_chain.py` e passar nos testes de `tests/test_matrix_chain.py`.
* **P4 (Benchmarks):** Executar experimento **E7** comparando o tempo cúbico da PD contra a explosão de Catalan.
* **P2 (Relatório Técnico):** Escrever os pseudocódigos `Matrix-Chain-Order` e `Print-Optimal-Parens`, desenhar as matrizes $m$ e $s$ em TikZ e formalizar a análise $\Theta(n^3)$.
* **P1 (Fundamentação):** Explicar a subestrutura ótima e a dedução dos números de Catalan no relatório.
* **P5 (Seminário & Web):** Desenvolver `web/matrix-chain.html` e conduzir a dinâmica interativa no seminário.

---

## 9. Dinâmica Sugerida para o Seminário (Bloco 2)
1. **Chamada de Voluntários:** Chame 3 voluntários da turma e dê as dimensões de 3 matrizes pequenas na lousa ($10 \times 100$, $100 \times 5$, $5 \times 50$).
2. **Desafio:** Peça para um voluntário calcular $(A_1 A_2) A_3$ e o outro calcular $A_1 (A_2 A_3)$.
3. **Revelação:** Compare os resultados ($7.500$ vs. $75.000$) e mostre que a ordem altera o custo em 10 vezes.
4. **Escala:** Mostre na sequência que para 6 matrizes já existem **42 parentizações**, e com 15 matrizes já são mais de **2,6 milhões**, evidenciando o poder da Programação Dinâmica $\Theta(n^3)$.
