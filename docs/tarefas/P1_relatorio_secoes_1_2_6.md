# Tarefa P1: Relatório Técnico (Seções 1, 2, 6), Referências e Montagem Final

**Responsável:** Integrante P1  
**Foco:** Fundamentação teórica rigorosa, introdução motivadora, limites da PD e coordenação editorial no Overleaf.

---

## 1. Objetivo
Redigir com rigor acadêmico a introdução, a fundamentação teórica formal e as conclusões do relatório em LaTeX, alimentar a bibliografia em BibTeX, configurar o projeto no Overleaf e coordenar a montagem integrada final com as contribuições dos demais membros.

---

## 2. Arquivos que você edita
* [`relatorio/main.tex`](../../relatorio/main.tex) (nomes dos integrantes, capa e ajustes gerais de preâmbulo)
* [`relatorio/secoes/01_introducao.tex`](../../relatorio/secoes/01_introducao.tex)
* [`relatorio/secoes/02_fundamentacao.tex`](../../relatorio/secoes/02_fundamentacao.tex)
* [`relatorio/secoes/06_conclusoes.tex`](../../relatorio/secoes/06_conclusoes.tex)
* [`relatorio/referencias.bib`](../../relatorio/referencias.bib)

---

## 3. Passo a Passo (Checklist)

- [ ] **Configuração do Overleaf:**
  - Subir o projeto no Overleaf importando a pasta `relatorio/` e `cheatsheet/` (ou sincronizando via integração GitHub).
  - Conferir que o documento compila sem erros em PDF.
  - Atualizar os nomes completos e e-mails dos integrantes na capa de `relatorio/main.tex`.

- [ ] **Seção 1 - Introdução (Estrutura em Funil):**
  - **Contextualização ampla:** Apresentar a relevância dos problemas de otimização combinatória em computação e engenharia.
  - **O Gargalo:** Explicar a limitação de algoritmos puramente recursivos (árvore exponencial por recomputação repetida).
  - **Objetivos do Grupo:** Expor com clareza o propósito da pesquisa sobre Programação Dinâmica (Cap. 15 do Cormen).
  - **Roteiro do Documento:** Fornecer um parágrafo conciso delineando a leitura dos capítulos subsequentes.

- [ ] **Seção 2 - Fundamentação Teórica Formal:**
  - **Definição Canônica:** Formalizar a Programação Dinâmica como método para problemas com subproblemas sobrepostos.
  - **Subestrutura Ótima:** Apresentar a definição matemática e demonstrar formalmente a propriedade utilizando a técnica de *"cortar e colar"* (cut-and-paste) por contradição no problema do Corte de Hastes.
  - **Superposição de Subproblemas:** Contrastar a sobreposição da PD com a independência de subproblemas na Divisão e Conquista.
  - **Grafo de Subproblemas:** Formalizar o DAG de estados e como sua topologia determina a ordem de resolução.
  - **Os Quatro Passos do Cormen:** Detalhar estruturação, recorrência, computação (Bottom-Up vs. Top-Down) e reconstrução.
  - **PD vs. Algoritmos Gulosos vs. Divisão e Conquista:** Quadro comparativo claro de critérios de aplicabilidade.
  - **Explosão Combinatória e Catalan:** Demonstrar a fórmula dos números de Catalan $C(n-1) = \frac{1}{n}\binom{2n-2}{n-1}$ e justificar por que $P(n) = \Omega(4^n / n^{3/2})$ torna a força bruta inviável na cadeia de matrizes.

- [ ] **Seção 6 - Conclusões e Limitações:**
  - **Onde a PD Brilha:** Síntese dos problemas resolvidos eficientemente.
  - **Onde a PD Falha:** Discutir detalhadamente:
    * Ausência de subestrutura ótima (problema do caminho simples mais longo em grafos).
    * Explosão de estados (Caixeiro Viajante - algoritmo de Held-Karp $O(n^2 \cdot 2^n)$).
    * Complexidade pseudo-polinomial (Mochila 0/1 dependente de $W$ e não da quantidade de bits).
    * Gargalo de memória espacial em tabelas multidimensionais.
  - **Trabalhos Futuros:** Possibilidades de paralelização e algoritmos aproximativos.

- [ ] **Referências Bibliográficas:**
  - Adicionar no `referencias.bib` artigos clássicos (Bellman, 1957; Needleman-Wunsch, 1970) além do livro do Cormen.
  - Garantir que toda entrada do arquivo `.bib` seja explicitamente citada no texto com `\cite{...}`.

- [ ] **Montagem e Revisão Final:**
  - Integrar os textos e figuras produzidos por P2 (Cap. 3 e 4) e P4 (Cap. 5).
  - Coordenar a leitura cruzada e conferir a ausência de *warnings* ou erros de compilação.

---

## 4. Critério de Pronto
* O documento compila limpo no Overleaf sem erros.
* Todos os teoremas e propriedades possuem demonstrações ou justificativas matemáticas formais.
* O texto atende a todas as exigências conceituais do enunciado da disciplina.

---

## 5. Dicas Úteis
* Mantenha o texto impessoal na terceira pessoa ("observa-se", "propõe-se") ou primeira do plural acadêmico ("demonstramos").
* Crie commits semânticos frequentes: `docs: redige secao 1 introducao`, `docs: fundamentacao corte e colar`.

---

## 6. Avise Quando Terminar
* Avise **P2** e **P4** assim que o ambiente no Overleaf estiver compartilhado e pronto para edição simultânea.
* Ao concluir a primeira versão das Seções 1 e 2, avise **P5** para que ele aproveite a fundamentação nos slides.
