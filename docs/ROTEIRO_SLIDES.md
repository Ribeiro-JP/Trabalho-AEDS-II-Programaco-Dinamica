# Roteiro dos Slides e Dinâmica do Seminário (40 Minutos)

O seminário dura 40 minutos. A ideia é construir o algoritmo passo a passo, e não ler slides. Divisão sugerida de tempo e de apresentadores (cada integrante fica com um bloco).

---

## Regras gerais dos slides

* Uma ideia por slide, com pouco texto: figura, tabela ou trecho curto de código.
* Mesmas cores dos gráficos (ingênuo vermelho, memo azul, bottom-up verde, duas linhas roxo, guloso cinza).
* Frase de transição entre os blocos ("agora o [Nome] mostra isso funcionando").
* Animar a tabela do LCS, as tabelas da cadeia de matrizes e a árvore de recursão por etapas; usar as páginas `web/` como apoio ao vivo.

---

## Bloco 1 (0 a 7 min): gancho e conceitos

* **Abertura:** título, integrantes e disciplina.
* **Problema motivador:** barra de aço e tabela de preços (1, 5, 8, 9). "Qual o melhor corte para tamanho 4?" (a turma tenta antes da resposta).
* **Fibonacci ingênuo:** código curto e árvore de recursão com repetições destacadas.
* **Subestrutura ótima:** definição e ideia da prova de "cortar e colar".
* **Superposição de subproblemas:** definição e exemplo na árvore.
* **Os 4 passos do Cormen em um slide.**

---

## Bloco 2 (7 a 18 min): construção passo a passo

* **Corte de hastes (cerca de 7 min):** recorrência; versão ingênua e custo $\Theta(2^n)$ (ideia da prova $T(n) = 1 + \sum T(j)$); memoização (a árvore "encolhe"); bottom-up com a tabela sendo preenchida; reconstrução dos cortes; quadro memo × bottom-up com prós e contras.
* **Cadeia de matrizes (cerca de 4 min):** o problema (a ordem muda o custo, não o resultado); a explosão das parentizações (Catalan: 42 para 6 matrizes); a recorrência por intervalos; as tabelas $m$ e $s$ preenchidas por diagonais no exemplo do Cormen ($[30, 35, 15, 5, 10, 20, 25]$, custo 15125); a parentização ótima; custo $\Theta(n^3)$.

---

## Bloco 3 (18 a 25 min): código e repositório

* **Mapa do repositório** (estrutura de pastas).
* **Demonstração ao vivo:** Fibonacci ingênuo virando memoizado, mostrando o contador de chamadas.
* **Demonstração do LCS:** `web/lcs-table.html` com duas palavras sugeridas pela turma (e, se der tempo, `web/matrix-chain.html`).
* **Como rodar tudo** (`make setup`, `make test`, `make bench`).
* **Plano B:** prints ou vídeo curto gravado da demonstração.

---

## Bloco 4 (25 a 33 min): experimentos e estudo de caso

* **Estudo de caso:** mini diff e alinhamento de DNA com o LCS e a distância de edição.
* **Gráficos E1 e E2:** tempo × $n$ (ingênuo × memo × bottom-up), escala log.
* **Gráfico E3:** memória da tabela completa × duas linhas.
* **Gráfico E4:** Python × C++.
* **Gráfico E7:** cadeia de matrizes, nº de parentizações × $n$ contra o tempo da PD.
* **Gargalos:** limite de recursão (E5), tamanho da tabela 2D, localidade de cache.
* **Discussão crítica:** o que mudou do esperado na teoria para o medido.

---

## Bloco 5 (33 a 40 min): análise, limites e fechamento

* **Tabela de complexidades** (tempo e espaço, com $O$, $\Omega$ e $\Theta$).
* **Duelo guloso × PD** (E6 e `rod-cutting-duel.html`): por que o guloso falha.
* **Onde a PD falha:** mochila pseudo-polinomial, explosão de estados, ausência de subestrutura ótima.
* **Debate aberto:** "dá para reduzir a memória do LCS e ainda recuperar a subsequência?"
* **Quiz final** (`web/quiz.html`).
* **Conclusões, o cheat sheet e agradecimentos.**

---

## Dicas para a apresentação ser dinâmica e divertida

* **Aposta do Fibonacci:** cronômetro na tela, a turma chuta quanto tempo `fib(40)` ingênuo leva; rodar e depois rodar o memoizado.
* **Problema da barra de aço:** quatro voluntários tentam achar o melhor corte antes da teoria.
* **Duelo guloso × PD:** dois times, um escolhe pela razão preço/centímetro, outro preenche a tabela; revelar 9 contra 10 e deixar a turma descobrir por quê.
* **Tabela viva:** dois voluntários dão duas palavras (podem ser os nomes) e a turma preenche o LCS no quadro, célula por célula.
* **Ordem das matrizes:** três voluntários escolhem como multiplicar 3 matrizes pequenas e a turma compara os custos.
* **Gráfico misterioso:** mostrar o gráfico de tempo sem legenda e pedir para a turma adivinhar qual curva é qual técnica.
* **Caça ao bug:** mostrar uma recorrência com erro sutil (caso base errado) e a turma encontra.
* **Quiz no fim** (`quiz.html`, Kahoot ou Mentimeter) e um verdadeiro ou falso de 1 minuto, com pontos simbólicos.
* **Live coding curto:** transformar o Fibonacci ingênuo em memoizado na frente da turma.
* **Transições combinadas entre os apresentadores:** todos devem saber responder sobre a parte dos outros.
* **Ensaio cronometrado com perguntas cruzadas** antes do dia, e plano B para projetor, notebook ou internet.
