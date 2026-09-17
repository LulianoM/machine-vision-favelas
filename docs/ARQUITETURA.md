# Como as duas máquinas compartilham o projeto

Decisão registrada em 2026-09-17.

## O problema

O projeto vive em duas máquinas que não se enxergam. O desktop Windows (GPU, ARMA 3, sempre ligado) recebeu um pacote `.rar` em 11/09 e evoluiu o treino por conta própria. O MacBook ficou com o artigo, o levantamento 3D, a bibliografia e a memória do Claude. Cada Claude só conhece a sua metade, e a memória automática do Claude Code é local por máquina.

São três necessidades distintas, e cada ferramenta cogitada resolve no máximo uma:

| Necessidade | O que exige |
|---|---|
| 1. Verdade única | Texto, código e estado do projeto num lugar só, com histórico e sem conflito silencioso |
| 2. Acesso à máquina | Do Mac, rodar comando, ver log, copiar arquivo grande e operar a tela do desktop |
| 3. Visão rápida | Uma página para ver o estado do projeto de qualquer aparelho |

## As opções cogitadas

| Opção | Serve para | Por que não é a espinha |
|---|---|---|
| Obsidian | Ler e escrever notas com conforto | É editor, não transporte. Para sincronizar depende de Obsidian Sync (pago), iCloud ou Drive, e herda os problemas deles. Pode abrir a pasta do repositório como vault, só para leitura |
| Google Drive | Trocar .docx com o orientador; guardar os binários grandes e sensíveis que já estão lá | Sincronização sem histórico de verdade e com conflito silencioso ("cópia em conflito"). Corrompe pasta `.git`. Sofre com dezenas de milhares de imagens pequenas. O conector do Claude não baixa arquivo acima de 10 MB. Dado da PCERJ não deve ganhar mais cópias em nuvem |
| Cloudflare Tunnel | Publicar um serviço web do desktop para terceiros, com URL fixa | Resolve publicar, não acessar a própria máquina. URL fixa exige domínio na Cloudflare; o modo rápido troca de URL a cada reinício. Expõe um serviço à internet, o que pede camada de autenticação. Para uso pessoal, Tailscale faz o mesmo papel sem expor nada |
| Artifact (página no claude.ai) | Painel de estado, legível do celular, atualizável pelos dois Claudes (é por conta, não por máquina) | É vitrine, não banco de dados. O conteúdo de verdade precisa existir em arquivo versionado |

## O desenho adotado

```
                    GitHub (repositório privado)
                    fonte única: texto, código, estado
                       ^                      ^
             git push/pull            git push/pull
                       |                      |
   MACBOOK (cliente leve) ==== Tailscale ==== DESKTOP (central)
   - acessa o desktop          rede privada   - ARMA 3, datasets, treino, pesos
   - escreve offline           ssh, scp,      - working copy principal
                               tela remota    - publica o painel
                       \                      /
                        v                    v
                   Painel do projeto (artifact privado)
```

1. Verdade única: repositório git privado no GitHub. Os dois Claudes leem `CLAUDE.md`, `STATUS.md` e `DIARIO.md` ao começar e escrevem ao terminar. É o único mecanismo que os dois entendem nativamente, tem histórico, funciona offline e avisa quando há conflito em vez de sobrescrever.
2. Acesso à máquina: Tailscale nas duas pontas. Sobre ele, SSH (comando, log, `scp` e `rsync` de arquivo grande), tela remota com Parsec ou Moonlight (o ARMA 3 precisa de interface gráfica) e, se um dia houver TensorBoard, `http://desktop:6006` direto do navegador do Mac.
3. Visão rápida: o painel em artifact, com a fonte HTML dentro do repositório (`painel/`), para que qualquer um dos dois Claudes consiga atualizar.

O desktop é a máquina central, como proposto: é onde ficam a working copy principal e tudo que é pesado. O GitHub existe para o dia em que o desktop estiver inalcançável (queda de luz, reinício do Windows Update, internet de casa fora) e para o histórico.

## O que trafega por onde

| Conteúdo | Canal |
|---|---|
| Artigo, scripts, métricas, estado, decisões | git |
| Datasets, screenshots, pesos, PDFs de papers | Ficam no desktop. Cópia pontual por `scp` ou `rsync` via Tailscale |
| .docx de e para o orientador | E-mail ou Drive, arquivado em `01-artigo/rascunhos-professor/` |
| Ortomosaicos da PCERJ | Não trafegam. Ficam onde já estão |
| Memória automática do Claude | Não trafega. O que importa vai para `docs/CONTEXTO.md` |

## Quando rever esta decisão

- Se o orientador ou um terceiro precisar ver algo rodando no desktop (TensorBoard, demo): aí sim Cloudflare Tunnel com domínio e Cloudflare Access na frente.
- Se o volume de PDFs e figuras a compartilhar crescer: Git LFS ou uma pasta compartilhada via SMB pelo Tailscale.
