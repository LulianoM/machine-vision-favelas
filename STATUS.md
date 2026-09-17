# STATUS

Retrato atual do projeto. Reescrever a cada marco. Histórico fica em `DIARIO.md`.

Última atualização: 2026-09-17, [MAC]

## Artigo

| Item | Estado |
|---|---|
| Versão vigente do orientador | v2 de 2026-09-10 (`01-artigo/rascunhos-professor/2026-09-10_v2_Irigaray.docx`). O arquivo baixado em 17/09 é idêntico a ela: não há v3 |
| Manuscrito por seção | Feito em 17/09, 8 arquivos em `01-artigo/manuscrito/`, texto verbatim da v2 |
| Pendências do rascunho | Levantadas e verificadas em `01-artigo/PENDENCIAS.md`. Nenhuma resolvida ainda |
| Seção "Conclusion" | Só tem Limitations, Delimitations e Future Research. Falta o fecho |
| Resultados empíricos | Nenhum número no artigo. Dependem do desktop (ver abaixo) |

## Experimento (desktop)

| Item | Estado |
|---|---|
| Pacote de 11/09 recebido no desktop | Sim. Segundo o autor (17/09), o desktop avançou muito, o modelo já foi treinado e há uma pesquisa feita lá a partir do e-mail de 12/09 |
| Estado real do pipeline (missão ARMA 3, dataset, treino, mAP) | Fora do repositório. Nenhum número, script ou documento do desktop chegou aqui ainda. Esperar divergência com o que este lado registra |
| `06-resultados/RESULTADOS.md` | Não existe ainda. É a primeira coisa que o desktop deve trazer |

## Infraestrutura entre as máquinas

| Item | Estado |
|---|---|
| Estrutura do repositório no Mac | Pronta em 17/09 |
| Repositório privado no GitHub | Criado em 17/09: https://github.com/LulianoM/machine-vision-favelas (primeiro commit marcado com a tag `v2-irigaray-verbatim`) |
| Desktop clonado e migrado para o repositório | Pendente. Roteiro em `docs/SETUP-DESKTOP.md` e `docs/PROMPT-MIGRACAO-DESKTOP.md` |
| Tailscale nas duas máquinas, SSH no desktop | Pendente |
| Acesso remoto à tela do desktop (ARMA 3 precisa de interface gráfica) | Pendente |
| Painel web do projeto | Publicado em 17/09 (privado). Fonte em `painel/painel.html` |

Painel: https://claude.ai/artifact/3XtSXZvhkzovA1ixGZ4rFH

## Próximos passos, em ordem

1. [AUTOR, no desktop] Seguir `docs/SETUP-DESKTOP.md`: Tailscale, OpenSSH, clonar o repositório.
2. [DESKTOP] Rodar o prompt de reconciliação (`docs/PROMPT-MIGRACAO-DESKTOP.md`, versão 2): inventário, tabela de divergências, cópia de código, resultados e pesquisa para o repositório, correção deste arquivo com o estado real. Não depende de Tailscale nem de SSH, só do clone.
3. [MAC ou DESKTOP] Resolver `01-artigo/PENDENCIAS.md` começando pelas 13 referências ausentes (conferir cada DOI no Crossref).
4. [AUTOR] Devolver ao orientador a lista de pendências e combinar como ele quer receber as edições (.docx com controle de alterações ou texto limpo).
5. [AUTOR] E-mail para cartografia.ipp@prefeitura.rio pedindo a nuvem LiDAR e o MDS de 2024 do recorte do Jacarezinho.

## Bloqueios

- Nenhum número de sim-to-real disponível para o artigo até o desktop reportar.
