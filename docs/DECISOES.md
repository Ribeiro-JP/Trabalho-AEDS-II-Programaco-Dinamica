# Registro de Decisões de Projeto (Architecture Decision Log)

Este registro documenta as escolhas de engenharia e simplificações adotadas durante a estruturação inicial da base de código (uma linha por decisão):

- Ambiente virtual Python isolado em `.venv/` com dependências mínimas gerenciadas exclusivamente via `Makefile`.
- Interceptação automática de `NotImplementedError` via hook `pytest_runtest_makereport` em `conftest.py` marcando testes como `SKIPPED`.
- Paleta cromática imutável em gráficos, LaTeX e web: Vermelho `#d62728` (ingênuo), Azul `#1f77b4` (memo), Verde `#2ca02c` (bottom-up), Roxo `#9467bd` (duas linhas) e Cinza `#7f7f7f` (guloso).
- Adoção de dimensões `(n+1)` em tabelas de programação dinâmica para manter indexação 1-baseada idêntica à notação do livro do Cormen.
- Interface web construída com Vanilla HTML5/CSS3/ES6 servida via `python -m http.server`, eliminando dependências de Node.js, npm ou bundlers.
- Binário C++ para experimento E4 compilado diretamente com `g++ -O3 -std=c++17` pelo alvo `make cpp`.
- Reutilização do corpo do Cheat Sheet (`cheatsheet/cheatsheet_body.tex`) tanto no documento avulso quanto no apêndice do relatório via `\input`.
- Integração de dados empíricos de benchmark entre Python e Web através de arquivo JSON estático consolidado em `web/data/results.json`.
- Coleta de metadados de hardware e sistema operacional em `machine.json` para assegurar reprodutibilidade científica das medições.
