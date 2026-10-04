# Guia de Trabalho em Grupo e Boas Práticas

Este guia define as regras operacionais da equipe para assegurar colaboração harmoniosa, evitar conflitos de código e garantir que todos dominem o projeto para o seminário.

---

## 1. Fluxo de Git e Ramificações (Branches)

* **Regra de Ouro:** **Nunca faça commits diretamente na branch `main`.**
* **Crie branches temáticas:** Toda nova funcionalidade ou seção deve ser criada a partir de uma branch dedicada:
  ```bash
  git checkout main
  git pull origin main
  git checkout -b p3/corte-de-hastes
  ```
  *Exemplos de nomes:* `p1/introducao`, `p2/diagramas-tikz`, `p3/lcs`, `p4/benchmarks-e1-e3`, `p5/portal-web`.
* **Pull Requests e Revisão:** Ao concluir sua branch, faça push e abra um Pull Request (PR) solicitando a revisão de pelo menos outro colega de grupo antes de fazer merge na `main`.

---

## 2. Donos de Arquivos e Fronteiras Claras

* Cada integrante possui uma lista clara de arquivos sob sua responsabilidade (especificados em `docs/tarefas/Pn_...md`).
* **Respeite os arquivos dos colegas:** Não altere arquivos pertencentes a outro integrante sem combinar previamente no grupo de mensagens.
* Se precisar de dados de outro colega (ex.: P5 precisa do JSON gerado por P4), combine o formato com antecedência.

---

## 3. As Assinaturas em `src/` são um Contrato

* As assinaturas de funções, tipos de dados e nomes de módulos já criados em `src/` são o **contrato formal** entre todos os integrantes e com a suíte de testes em `tests/`.
* **Proibido alterar assinaturas unilateralmente:** Caso sinta necessidade de alterar qualquer assinatura de função em `src/`, leve o tema para discussão prévia no grupo.

---

## 4. Padrão de Commits Semânticos

* Realize commits pequenos, frequentes e atômicos.
* Utilize o padrão de mensagens no formato `tipo: descrição curta em português`:
  * `feat:` nova funcionalidade ou implementação de algoritmo (ex.: `feat: implementa memoizacao no corte de hastes`)
  * `test:` adição ou ajuste de testes unitários (ex.: `test: adiciona casos de borda do lcs`)
  * `docs:` escrita ou ajuste de documentação, LaTeX ou markdown (ex.: `docs: redige secao 2 de fundamentacao`)
  * `fix:` correção de bug ou inconsistência (ex.: `fix: corrige indice k na cadeia de matrizes`)
  * `chore:` tarefas de infraestrutura, Makefile ou dependências (ex.: `chore: atualiza dependencias`)

---

## 5. Rastreamento e Quadro de Tarefas

* Sempre que concluir uma etapa, marque `- [x]` no seu arquivo individual (`docs/tarefas/Pn_...md`) e no quadro geral (`docs/TAREFAS.md`).
* Mantenha a equipe informada no grupo de comunicação sempre que um módulo for concluído e disponibilizado.

---

## 6. Sincronização do Relatório no Overleaf

* O relatório em LaTeX pode ser editado simultaneamente no **Overleaf**.
* Conecte o repositório GitHub diretamente ao Overleaf (caso possua conta Premium/Educacional) ou eleja o integrante **P1** para periodicamente baixar o `.zip` do Overleaf e comitar as alterações na pasta `relatorio/` do GitHub.

---

## 7. Revisão Cruzada e Domínio Coletivo

* **Todos serão avaliados no seminário:** O professor Michel Pires poderá fazer perguntas técnicas a qualquer integrante sobre qualquer parte do projeto.
* Na semana anterior à apresentação, realizaremos uma **revisão cruzada obrigatória**:
  * P1 e P2 testam e rodam o código de P3 e P4.
  * P3 e P4 revisam o relatório em LaTeX e os cálculos de P1 e P2.
  * Todos navegam pelas páginas web de P5 e participam do ensaio geral cronometrado de 40 minutos.
