# DIÁRIO DE BORDO

Entradas novas no topo. Formato: `## AAAA-MM-DD [MÁQUINA] título`, depois o que foi feito, o que foi decidido e o que ficou para o outro lado. Nunca apagar entrada antiga.

## 2026-09-17 [MAC] Prompt de reconciliação para o desktop

O autor informou que o desktop avançou muito (modelo já treinado) e que há uma pesquisa feita lá a partir do e-mail de 12/09 ("Levantamento técnico: recriar quarteirão de favela em 3D com alta fidelidade", enviado de si para si). Esse e-mail é o resumo do levantamento cujo PDF completo só existia no Mac e agora está em `05-levantamento-3d/`. `docs/PROMPT-MIGRACAO-DESKTOP.md` foi reescrito (versão 2) para esse cenário: fases com parada para aprovação, regras de precedência (desktop prevalece em experimento e código, repositório prevalece em estrutura e manuscrito, pesquisa é união), divergências registradas em `docs/DIVERGENCIAS.md`. O prompt também está no painel, com botão de copiar.

Para o desktop: tudo que este lado afirma sobre o experimento está desatualizado. Corrigir sem cerimônia, com arquivo de origem para cada número.

## 2026-09-17 [MAC] Reorganização da pasta e repositório único

Feito:
- Pasta `~/Documents/Mestrado/AIM2027/` separada em duas áreas: `dossie-conferencia/` (estratégia AIM 2027, roteiro, 48 missões, eixos, modelos de formato; movidos em bloco, links relativos preservados) e `machine-vision-favelas/` (este projeto).
- As três pastas soltas (PROJETO MACHINE VISION FAVELAS, PROJETO DRONE PCERJ, PESQUISA CV DRONES) foram fundidas aqui, na mesma estrutura numerada do pacote de 11/09 que o desktop recebeu.
- Rascunhos do orientador copiados de `~/Downloads` para `01-artigo/rascunhos-professor/`. Achado: `Machine Vision from the Global South(2).docx`, baixado em 17/09, tem o mesmo MD5 do `(1)` de 10/09. Não existe v3.
- v2 dividida em 8 arquivos Markdown por seção com `01-artigo/ferramentas/docx_para_secoes.py` (só biblioteca padrão, roda igual no Windows). Texto verbatim.
- Auditoria do rascunho refeita e ampliada em `01-artigo/PENDENCIAS.md`.
- Criados `CLAUDE.md`, `STATUS.md`, este diário, `docs/CONTEXTO.md` (conhecimento que estava só na memória do Claude do Mac) e os guias de setup do desktop.

- Repositório privado criado e publicado: https://github.com/LulianoM/machine-vision-favelas. O primeiro commit tem a tag `v2-irigaray-verbatim` (texto do orientador sem nenhuma alteração). Painel web publicado: https://claude.ai/artifact/3XtSXZvhkzovA1ixGZ4rFH

Decidido:
- Um repositório git é a fonte única de verdade. O desktop é a máquina central. A memória automática do Claude não é canal de comunicação entre máquinas.
- Scripts em `03-arma3/scripts/` aqui são os ORIGINAIS de 11/09. As versões do desktop, se evoluíram, prevalecem: o desktop sobrescreve e o git mostra a diferença.

Para o desktop:
- Seguir `docs/PROMPT-MIGRACAO-DESKTOP.md`. O mais urgente é `06-resultados/RESULTADOS.md` e a atualização do `STATUS.md` com o estado real do treino.
