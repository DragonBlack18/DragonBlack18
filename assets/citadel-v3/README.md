# The Crimson Codex · Citadel Edition V3

**Masterpiece Refinement / November 2026.** Esta edição é um refinamento incremental da Citadel Edition V2, não uma reconstrução do README.

## Direção de arte

- **Hierarquia editorial:** os seis capítulos usam faixas heráldicas com numerais maiores e títulos mais legíveis.
- **Vitrais e armaria:** as três classes da armaria têm ícones mais reconhecíveis. Os badges originais permanecem no Markdown.
- **Portfólio móvel:** os seis novos cartões são renderizados em **coluna única**, com descrições em texto nativo do GitHub. Os seis cartões V2 permanecem em uma seção expansível.
- **Colofão:** assinatura visual em pedra, marfim e carmesim, sem substituir a capa, o pórtico ou as animações originais.

## Inventário

`chapter-01-identity.svg` a `chapter-06-archive.svg` (6); `project-*.svg` (6); `armory.svg` (1); `colophon.svg` (1). **14 novos SVGs estáticos**.

As artes anteriores continuam armazenadas em `assets/` e `assets/citadel-v2/`. Os GIFs `iron-vow.gif`, `templar-cathedral-watch.gif`, `crimson-eclipse.gif`, `ashen-citadel.gif` e `crimson-gate.gif` não são alterados.

## Compatibilidade

Os assets SVG usam SVG 1.1 declarativo com `viewBox`, atributos `title` e `desc`. Não incluem scripts, fontes remotas, hyperlinks externos ou animações SVG. A reprodução de movimento permanece exclusivamente nos GIFs originais.

O GitHub sanitiza HTML em Markdown: por isso o projeto não depende de CSS do README, JavaScript, carregamento dinâmico ou controle de media queries. Os cartões V3 em coluna única são uma solução deliberada para diminuir o encolhimento no celular.

**Estados e disponibilidade** são descrições editoriais, não verificações em tempo real. Para VYRNODE, o link público aponta para releases e não declara que o código-fonte é público.

## Regressão antes de publicar

1. Verificar a preservação de todos os arquivos preexistentes comparando blobs SHA no Git.
2. Conferir resolução de todas as referências `./assets/*` no README.
3. Conferir os seis links de repositório, seis âncoras e pares de tags HTML.
4. Conferir XML SVG, `title`/`desc`, geometria declarada e ausência de recursos externos.
5. Preservar os quatro blocos de código Markdown e o texto original.
