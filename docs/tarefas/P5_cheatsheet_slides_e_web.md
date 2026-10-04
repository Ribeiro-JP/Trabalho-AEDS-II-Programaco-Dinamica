# Tarefa P5: Cheat Sheet, Slides do Seminário (40 min) e Simuladores Web

**Responsável:** Integrante P5  
**Foco:** Didática, comunicação visual, ferramentas interativas e preparação do material de apresentação da equipe.

---

## 1. Objetivo
Elaborar o Cheat Sheet de 1 a 2 páginas em LaTeX, construir os slides da apresentação de 40 minutos seguindo rigorosamente o roteiro oficial, programar a interatividade em JavaScript das 6 páginas web do portal e coordenar o ensaio cronometrado do grupo.

---

## 2. Arquivos que você edita
* [`cheatsheet/cheatsheet_body.tex`](../../cheatsheet/cheatsheet_body.tex)
* [`cheatsheet/cheatsheet.tex`](../../cheatsheet/cheatsheet.tex)
* [`slides/README.md`](../../slides/README.md) (e apresentação no diretório `slides/`)
* [`web/css/style.css`](../../web/css/style.css)
* [`web/js/shared.js`](../../web/js/shared.js)
* [`web/fib-tree.html`](../../web/fib-tree.html)
* [`web/rod-cutting-duel.html`](../../web/rod-cutting-duel.html)
* [`web/matrix-chain.html`](../../web/matrix-chain.html)
* [`web/lcs-table.html`](../../web/lcs-table.html)
* [`web/benchmarks.html`](../../web/benchmarks.html)
* [`web/quiz.html`](../../web/quiz.html)

---

## 3. Passo a Passo (Checklist)

- [ ] **Cheat Sheet (1 a 2 páginas concisas):**
  - Em `cheatsheet/cheatsheet_body.tex`, completar os 4 blocos obrigatórios:
    * **Bloco 1:** Definição em uma única frase ("Técnica de projeto para problemas de otimização...").
    * **Bloco 2:** Diagrama de decisão em TikZ: fluxograma orientando quando usar PD, Divisão e Conquista ou Algoritmo Guloso.
    * **Bloco 3:** Tabela de complexidades de tempo e espaço (integrar a versão final gerada por P2).
    * **Bloco 4:** Padrão genérico de pseudocódigo comparando o esqueleto Top-Down (Memoizado) vs. Bottom-Up (Iterativo).
  - Compilar `cheatsheet/cheatsheet.tex` e verificar que o conteúdo cabe perfeitamente em no máximo 2 páginas.

- [ ] **Construção dos Slides do Seminário (40 minutos):**
  - Consultar detalhadamente o guia: 👉 [`docs/ROTEIRO_SLIDES.md`](../ROTEIRO_SLIDES.md).
  - Escolher a plataforma (Google Slides, PowerPoint, Canva ou Beamer) e estruturar os 5 blocos:
    * **Bloco 1 (0 a 7 min):** Gancho inicial, problema motivador da barra de aço, conceitos e os 4 passos do Cormen.
    * **Bloco 2 (7 a 18 min):** Construção passo a passo do Corte de Hastes e Cadeia de Matrizes (tabelas e Catalan).
    * **Bloco 3 (18 a 25 min):** Demonstração ao vivo do código, árvore e simulação do LCS na web.
    * **Bloco 4 (25 a 33 min):** Experimentos empíricos, gráficos científicos de P4, comparativo Python x C++ e gargalos de hardware.
    * **Bloco 5 (33 a 40 min):** Duelo guloso x PD, limites da técnica, quiz com a turma e fechamento.
  - Alinhar com cada integrante do grupo o bloco que ele irá apresentar.
  - Exportar a versão final em PDF para `slides/seminario_programacao_dinamica.pdf`.

- [ ] **Desenvolvimento das Páginas Web Interativas (nesta ordem recomendada):**
  - [ ] **1. `web/lcs-table.html`:** Preenchimento animado da matriz $c$ e $b$ com setas de traceback ('↖', '↑', '←') e controles (Play, Pausa, Passo, Reiniciar).
  - [ ] **2. `web/fib-tree.html`:** Renderização de árvore de recursão com slider para $n \in [1..6]$ e botão para alternar memoização (destacando repetições em vermelho).
  - [ ] **3. `web/rod-cutting-duel.html`:** Comparador guloso vs. PD com tabela de preços editável e botão para carregar contra-exemplo (ex.: $n=4$, preços $[0, 1, 5, 8, 9]$ com resultado 9 vs. 10).
  - [ ] **4. `web/matrix-chain.html`:** Preenchimento visual das tabelas $m$ e $s$ por diagonais e exibição da parentização ótima formatada.
  - [ ] **5. `web/quiz.html`:** Quiz com 8 perguntas de múltipla escolha cobrindo a teoria, com feedback e cálculo de pontuação.
  - [ ] **6. `web/benchmarks.html`:** Renderização dos gráficos de desempenho lendo o JSON consolidado gerado por P4 (`web/data/results.json`).

- [ ] **Ensaio Geral e Plano B:**
  - Organizar um ensaio geral cronometrado (40 minutos cravados) com simulação de perguntas da banca.
  - Gravar vídeo curto ou capturas de tela das páginas web e demonstrações práticas como plano B caso haja falha de projetor ou conexão.

---

## 4. Critério de Pronto
* O Cheat Sheet compila em no máximo 2 páginas com formatação impecável.
* A apresentação em slides cobre todos os blocos e dura entre 38 e 40 minutos no ensaio.
* Todas as páginas web abrem via `make web` sem erros no console do navegador.

---

## 5. Dicas Úteis
* Não utilize frameworks pesados (React, Vue, Webpack) nas páginas web: mantenha HTML5, Vanilla CSS e Vanilla JS para que funcionem diretamente com `python -m http.server`.
* Se precisar de gráficos na web, utilize Chart.js diretamente via CDN (cdnjs.cloudflare.com).

---

## 6. Avise Quando Terminar
* Avise toda a equipe para agendar o ensaio cronometrado final da apresentação!
