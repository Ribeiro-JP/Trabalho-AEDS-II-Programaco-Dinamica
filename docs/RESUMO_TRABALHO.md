# Resumo do Trabalho - Programação Dinâmica (Cap. 15 Cormen)

## O trabalho em poucas linhas

* Trabalho Teórico Final de AEDS (CEFET-MG, Prof. Michel Pires). Tema do grupo: Programação Dinâmica, Cap. 15 do Cormen.
* Entregáveis: relatório técnico-científico em LaTeX com algorithm2e, seminário de 40 minutos e repositório público no GitHub com implementação de referência.
* Avaliação (15 pontos): 10 por domínio teórico (relatório, análise do Big-O, formatação e pseudocódigos) e 5 por aplicação e seminário (GitHub, didática e aderência prática).
* Todos os membros devem dominar pesquisa, código e relatório.
* Relatório em 6 seções: 1 Introdução (funil), 2 Fundamentação teórica, 3 Paradigma algorítmico (com diagramas obrigatórios), 4 Análise assintótica (O, Ω, Θ para tempo e memória), 5 Estudo de caso e implementação (GitHub, gráficos, gargalos), 6 Conclusões e referências. Apêndice: cheat sheet de 1 a 2 páginas.

---

## Conceitos importantes

* **Definição:** técnica de projeto para problemas de otimização que resolve cada subproblema uma única vez, guarda o resultado e reutiliza.
* **Subestrutura ótima:** uma solução ótima contém soluções ótimas dos subproblemas. Prova por "cortar e colar" (contradição).
* **Superposição de subproblemas:** a mesma subinstância aparece várias vezes na recursão; é o que torna guardar resultados vantajoso.
* **Os 4 passos do Cormen:** (1) caracterizar a estrutura de uma solução ótima; (2) definir recursivamente o valor; (3) calcular o valor, em geral de baixo para cima; (4) construir a solução a partir das informações guardadas.
* **Memoização (top-down) × bottom-up:** mesma complexidade assintótica; a memoização resolve só o necessário mas depende da pilha de recursão; o bottom-up evita recursão e facilita reduzir memória.
* **Grafo de subproblemas:** vértices são subproblemas e arestas indicam dependência; o tempo é aproximadamente a soma, sobre os vértices, do custo de resolver cada um.
* **PD × guloso × divisão e conquista:** o guloso faz uma escolha local sem revisitar; divisão e conquista tem subproblemas independentes; a PD tem subproblemas sobrepostos e compara alternativas.
* **Reconstrução da solução:** guardar a escolha feita em cada subproblema (tabela s ou b) e percorrer de trás para frente.
* **Ordem de preenchimento:** depende do problema (por tamanho de intervalo na cadeia de matrizes; linha a linha no LCS).
* **Pseudo-polinomial:** custo que depende do valor numérico de uma entrada (mochila O(nW)) e não só do tamanho da sua representação.
* **Onde falha:** ausência de subestrutura ótima (caminho simples mais longo), explosão do número de estados (TSP com Held-Karp, O(n²·2ⁿ)) e memória da tabela.

---

## Problemas do capítulo e complexidades

| Problema | Ideia da recorrência | Tempo | Espaço |
| :--- | :--- | :--- | :--- |
| **Fibonacci** | $F(n) = F(n-1) + F(n-2)$ | ingênuo exponencial; PD $\Theta(n)$ | $\Theta(n)$, ou $\Theta(1)$ com duas variáveis |
| **Corte de hastes (15.1)** | $r(n) = \max_{1 \le i \le n} (p(i) + r(n-i))$ | ingênuo $\Theta(2^n)$; PD $\Theta(n^2)$ | $\Theta(n)$ |
| **Cadeia de matrizes (15.2)** | $m[i,j] = \min_{i \le k < j} (m[i,k] + m[k+1,j] + p_{i-1} \cdot p_k \cdot p_j)$ | $\Theta(n^3)$ | $\Theta(n^2)$ |
| **LCS (15.4)** | $c[i,j]$ por igualdade ou máx dos vizinhos | $\Theta(mn)$ | $\Theta(mn)$, ou $O(\min(m,n))$ só com o comprimento |
| **BST ótima (15.5)** | $e[i,j]$ mínimo sobre as raízes | $\Theta(n^3)$ | $\Theta(n^2)$ |
| **Mochila 0/1** | $V[i,w] = \max$ com e sem o item $i$ | $O(nW)$ | $O(nW)$, ou $O(W)$ |

---

## Glossário rápido

* **Subproblema:** instância menor do problema original com a mesma estrutura matemática.
* **Caso base:** estado elementar cuja resposta é conhecida trivialmente sem recursão ($n=0, 1$, matriz de $1 \times 1$, string vazia).
* **Recorrência:** equação matemática que expressa o valor de uma solução ótima em função das soluções de subproblemas menores.
* **Tabela de memoização:** estrutura de dados (vetor, matriz ou hash table) onde resultados já computados são armazenados.
* **Traceback:** percurso em sentido inverso na tabela de decisões ($s$ ou $b$) para reconstruir a sequência de escolhas ótimas.
* **Parentização:** agrupamento associativo explícito com parênteses em produtos de matrizes indicando a ordem de multiplicação.
* **Subsequência:** sequência de elementos derivados de outra sequência mantendo a ordem relativa, sem exigir contiguidade.
* **Números de Catalan:** sequência combinatória $C_n = \frac{1}{n+1}\binom{2n}{n}$ que enumera parentizações, árvores binárias e caminhos de Dyck.
* **Pseudo-polinomial:** algoritmo cujo tempo é polinomial no valor numérico da entrada (como $W$), mas exponencial no tamanho da sua entrada em bits ($\log_2 W$).
* **Pico de memória:** quantidade máxima instantânea de memória RAM alocada durante a execução (mensurada via `tracemalloc`).
