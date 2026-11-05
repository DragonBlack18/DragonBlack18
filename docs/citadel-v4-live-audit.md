# ✠ Citadel Edition V4 — Auditoria visual da página real do GitHub

**Data:** 05/11/2026  
**Perfil verificado:** https://github.com/DragonBlack18  
**Repositório:** `DragonBlack18/DragonBlack18`  
**Workflow:** [Live GitHub profile visual audit](https://github.com/DragonBlack18/DragonBlack18/actions/runs/42101362432)  
**Commit de teste:** `3243a9e75cc36e10b5be4351f6b254c6bda023a8`  
**Artefato (capturas + audit.json):** [github-profile-live-audit](https://github.com/DragonBlack18/DragonBlack18/actions/runs/42101362432/artifacts/13448348652) — retenção configurada em 14 dias.

## Resultado executivo

**PASS — 8/8 combinações de largura e tema, no Chromium headless executado pelo GitHub Actions.**

| Tema | Viewport | HTTP | Overflow horizontal | Fólios V4 | Atalhos de capítulos | Clique real em PROJECTS |
| :--- | ---: | ---: | ---: | ---: | ---: | :--- |
| Escuro | 360 px | 200 | 0 px | 6/6 | 6/6 resolvidos | PASS |
| Escuro | 390 px | 200 | 0 px | 6/6 | 6/6 resolvidos | PASS |
| Escuro | 768 px | 200 | 0 px | 6/6 | 6/6 resolvidos | PASS |
| Escuro | 1440 px | 200 | 0 px | 6/6 | 6/6 resolvidos | PASS |
| Claro | 360 px | 200 | 0 px | 6/6 | 6/6 resolvidos | PASS |
| Claro | 390 px | 200 | 0 px | 6/6 | 6/6 resolvidos | PASS |
| Claro | 768 px | 200 | 0 px | 6/6 | 6/6 resolvidos | PASS |
| Claro | 1440 px | 200 | 0 px | 6/6 | 6/6 resolvidos | PASS |

No clique automatizado no atalho `#codex-projects`, o destino terminou no topo da área de visualização em todos os cenários (`targetTop = 0 px`, com rolagem efetiva de 3.070 a 3.941 px).

### Renderização e acessibilidade

- O conteúdo **The Crimson Codex** foi detectado na página pública.
- Os seis capítulos Markdown e os seis SVGs V4 de projetos foram encontrados.
- Os seis cartões V4 são clicáveis e possuem nomes alternativos.
- Não foi detectada imagem visível quebrada nem falha de carregamento nas imagens visíveis inspecionadas.
- Não houve overflow horizontal do documento nos oito cenários.
- O tema escuro e o claro foram capturados em telas reais do Chromium, não em uma página simulada.

### Problemas encontrados e resolução

1. **Runner incompatível:** a primeira execução utilizou Ubuntu 26.04, ainda não suportado pelo Playwright selecionado. O workflow foi fixado para `ubuntu-24.04`.
2. **Falso alerta de âncora:** o GitHub adiciona o prefixo `user-content-` aos nomes de âncoras HTML sanitizadas. A verificação foi ajustada para aceitar esse namespace. A validação posterior do **clique real** confirmou que a navegação funciona.
3. **README:** não foi identificado defeito visual ou funcional que justificasse alterar o conteúdo ou substituir os assets da V4 durante esta auditoria.

### Evidências e limites

- O workflow salva **8 screenshots de página inteira** e o arquivo `audit.json`, disponíveis no artefato indicado acima.
- Os testes foram realizados em Chromium Linux hospedado pelo GitHub, usando simulação de viewport e touch no mobile; **não** constituem um teste em celulares físicos.
- A análise não mede Core Web Vitals, consumo de memória, métricas reais de rede, desempenho dos GIFs sob CPU limitada, nem disponibilidade futura de badges externos.
- A auditoria representa o estado da página na execução registrada. Mudanças futuras no GitHub ou em serviços externos podem afetar o resultado.

**Conclusão:** os critérios definidos para a auditoria visual da Citadel Edition V4 passaram integralmente no ambiente testado, sem necessidade de alterar o README ou seus assets históricos.
