# ✠ Citadel Edition V4 — The Final Codex

**Escopo:** acabamento editorial do README profissional do perfil `DragonBlack18`, preservando a história visual das edições anteriores.

## Identidade

- Pedra negra: `#08070A`; vinho profundo: `#1A0B13`.
- Marfim (texto principal): `#F1DED2`; cobre (detalhes): `#D5B08B`; carmesim (heráldica): `#C94B5F`.
- Tipografia ornamental dentro dos SVGs: Georgia para títulos; Consolas/monospace para pequenas inscrições **não essenciais**. O texto principal dos projetos permanece em Markdown nativo.
- SVGs declarativos, sem JavaScript, imagens externas, fontes remotas ou animações SVG.

## Inventário V4

| Arquivo | Uso |
| --- | --- |
| `folio-rule-a.svg`, `folio-rule-b.svg` | Separadores discretos e alternados entre os seis capítulos; não carregam informação essencial |
| `project-deploycraft.svg`, `project-omniforge.svg`, `project-vyrnode.svg` | Fólios compactos da galeria: implantação, ferramentas e monitoramento |
| `project-vitality.svg`, `project-atlas.svg`, `project-iiad.svg` | Fólios compactos: gestão, assistente de IA e incubadora |
| `colophon.svg` | Selo final ornamental |

Os **nove SVGs V4 somam 15.512 bytes** no repositório. Não são criadas animações novas.

## Hierarquia do README

1. O terminal, a imagem de capa, o pórtico e os cinco GIFs originais continuam referenciados.
2. Os seis antigos cabeçalhos V3, a armaria V3, os seis cartões V3 e o colofão V3 permanecem em seções expansíveis do README. Nenhum arquivo anterior é regravado ou excluído.
3. A galeria V4 permanece em coluna única com nomes e descrições em texto Markdown legível no celular.
4. A galeria V2 e a tabela técnica original continuam disponíveis.

## Manutenção

Ao modificar o README, execute `python3 scripts/verify_readme.py` a partir da raiz. O workflow `.github/workflows/readme-integrity.yml` também realiza verificações estruturais em push e pull request.

O validador **não substitui** uma inspeção visual na página publicada. O registro e as limitações da auditoria estão em `docs/citadel-v4-audit.md`.
