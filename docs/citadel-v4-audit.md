# Relatório de auditoria — Citadel Edition V4

**Data:** 05/11/2026  
**Repositório:** `DragonBlack18/DragonBlack18`  
**Base revisada antes da atualização:** `278ffa7a58dbe0c0d2338568510ac9bba9cb070a`  
**Escopo:** estrutura do README, preservação do histórico, gráficos SVG V4, legibilidade local, links e referências.

## 1. Auditoria visual local

Foram renderizadas **8 prévias locais** com Chromium headless e uma estrutura de artigo que reproduz as larguras, os cartões SVG V4 e os textos de apoio. **Não são screenshots da página real do GitHub.**

| Largura de viewport | Tema escuro | Tema claro | Overflow horizontal | SVGs da galeria ausentes |
| --- | --- | --- | --- | --- |
| 360 px | PASS | PASS | 0 px | 0 |
| 390 px | PASS | PASS | 0 px | 0 |
| 768 px | PASS | PASS | 0 px | 0 |
| 1440 px | PASS | PASS | 0 px | 0 |

Na prévia com largura de 360 px, o menor título de fólio apresentou aproximadamente **21 px efetivos**. As caixas de texto medidas pelo SVG `getBBox()` não avançaram sobre a área reservada aos símbolos em nenhuma das oito configurações. A prévia local apresentou **zero falhas de renderização de SVG**.

## 2. Verificações de arte e acessibilidade

- **9/9 SVGs V4:** XML bem-formado (lxml), `viewBox`, `title`/`desc` e sem scripts ou fontes/imagens externas.
- Textos de nomes e descrições de projetos aparecem como conteúdo nativo do README, além das ilustrações.
- Os links da galeria têm nomes alternativos específicos; imagens estritamente ornamentais têm `alt=""`.
- Contraste teórico das cores declaradas (superfície `#1A0B13`): marfim `#F1DED2` = **14,64:1**, cobre `#D5B08B` = **9,46:1** e texto secundário `#C9A69E` = **8,56:1**. Estes resultados são sobre cores nominais, não medições de pixels dos gradientes.

## 3. Integridade e desempenho

- Novos assets SVG estáticos: **9 arquivos, 15.512 bytes** (soma dos arquivos locais finais).
- Os arquivos originais das edições V2 e V3 permanecem no Git, sem reescrita.
- A imagem do templário, as imagens de capa e todos os cinco GIFs permanecem referenciados.
- Para reduzir repetição na apresentação inicial, as artes V3 ficam em seções expansíveis; **não se afirma** que um navegador necessariamente deixará de baixá-las.
- O validador `scripts/verify_readme.py` foi exercitado em um **fixture local** com caso de sucesso e caso de falha por arquivo ausente (ambos com resultado esperado). O workflow GitHub Actions executa esse validador nos próximos pushes e PRs.

## 4. Limitações declaradas

- O ambiente local não tinha acesso de navegação à página pública do GitHub. Por isso **não foi possível capturar a renderização real hospedada**, nem garantir igualdade exata com a sanitização HTML, CSS e fontes usadas pelo GitHub.
- A prévia visual não incluiu todas as imagens históricas do README; focou nos componentes novos e na galeria responsiva.
- Os GIFs foram preservados em nível de arquivo; **não** passaram por inspeção quadro a quadro nem por nova compressão.
- Badges externos do Shields.io e respostas HTTP de terceiros não foram inspecionados na prévia offline.
- Não foi feita medição de Core Web Vitals da página pública.

## 5. Critério de publicação

Publicar somente quando o comparativo de árvores Git confirmar **zero remoções e zero mudanças de blobs históricos**, todas as referências `./assets` resolverem e o README mantiver seus capítulos, blocos de código, links internos e projetos originais. Após a publicação, conferir o novo `HEAD` e as referências pelo conector do GitHub.

**Conclusão técnica:** as verificações locais dos componentes V4 passaram. A nota máxima de experiência visual fica condicionada à inspeção manual da página efetivamente renderizada pelo GitHub em dispositivos reais.
