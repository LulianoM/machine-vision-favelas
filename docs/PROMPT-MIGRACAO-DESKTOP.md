# Prompt de reconciliação para o Claude Code do desktop

Versão 2, de 2026-09-17. Substitui a versão anterior, que supunha pouca divergência. Abrir o Claude Code na pasta de trabalho ATUAL do desktop (a que nasceu do pacote de 11/09 e onde o treino aconteceu) e colar o bloco abaixo.

---

Contexto. Este projeto (artigo "Machine Vision from the Global South" e o experimento ARMA 3 para YOLO) viveu até hoje em duas máquinas que não se enxergavam. Você, no desktop, avançou muito: pipeline, datasets, modelo treinado, e uma pesquisa feita a partir do e-mail de 12/09. O MacBook, em paralelo, reorganizou o projeto num repositório git privado que passa a ser a fonte única de verdade: https://github.com/LulianoM/machine-vision-favelas. O lado do Mac NÃO sabe nada do que aconteceu aqui; os arquivos de lá dizem "estado desconhecido" e "nada treinado", e isso está desatualizado. Sua tarefa é reconciliar os dois lados dentro do repositório, sem perder nada daqui e sem apagar nada de lá. Espere divergências e trate cada uma às claras.

Trabalhe em fases e pare nos pontos marcados PARE para eu aprovar.

## Fase 0. Preparar e ler

1. Se `C:\projetos\machine-vision-favelas` não existir: confira `gh auth status` (conta LulianoM; se faltar, `winget install GitHub.cli` e `gh auth login`), depois `gh repo clone LulianoM/machine-vision-favelas C:\projetos\machine-vision-favelas`. Se já existir, `git pull --rebase`.
2. No clone, configure só localmente: `git config user.name "Luciano Martins Figueira"` e `git config user.email martinslucianofigueira@gmail.com`.
3. Leia por inteiro, no clone: `CLAUDE.md`, `STATUS.md`, `DIARIO.md`, `docs/CONTEXTO.md`, `docs/ARQUITETURA.md`, `01-artigo/PENDENCIAS.md`, `06-resultados/README.md`. As regras do `CLAUDE.md` valem a partir de agora.
4. Leia também a sua própria memória de projeto do Claude Code nesta máquina (`%USERPROFILE%\.claude\projects\`, pasta correspondente a este diretório, subpasta `memory`) e qualquer `CLAUDE.md` ou nota que exista na pasta de trabalho atual. Memória não é compartilhada entre máquinas: o que houver de útil ali precisa virar arquivo no repositório.

## Fase 1. Inventário, só leitura

Não copie nem altere nada ainda. Se houver treino, captura ou avaliação rodando agora, não interrompa. Levante e me mostre:

1. Árvore da pasta de trabalho atual com tamanho por subpasta, e se ela já é um repositório git próprio (se for: quantos commits, branch, se há remoto).
2. Código: para cada arquivo de `03-arma3/scripts/`, se é igual, alterado ou novo em relação ao que está no clone (lá estão os originais de 11/09). Liste também scripts e notebooks fora dessa pasta.
3. Dados: cada dataset (caminho, tamanho, número de imagens e de rótulos, classes, splits, convenção de anotação modal ou amodal, data), screenshots brutas do ARMA, arquivos `.rpt`, missão do ARMA 3 (caminho da pasta da missão e dos `.sqf` em uso).
4. Treino: cada run (caminho, data, modelo base, épocas, imgsz, batch, tempo de treino, GPU), onde estão os pesos `best.pt` e `last.pt`, e as métricas finais que constam em arquivo (`results.csv`, saída de `val`).
5. Avaliação sim-to-real: o que já foi medido no VisDrone ou em qualquer imagem real (zero-shot, fine-tuning com fração de dado real, sintético mais real), com o arquivo que comprova cada número.
6. Documentos: `RESULTADOS.md`, logs de decisão, relatórios, PDFs, HTML, artifacts publicados (com URL), e tudo que for saída de pesquisa.
7. A pesquisa feita a partir do e-mail: o e-mail é o de 2026-09-12, enviado de mim para mim, assunto "Levantamento técnico: recriar quarteirão de favela em 3D com alta fidelidade" (link: https://mail.google.com/mail/u/0/#search/martinsluciano+/FMfcgzQhWTkJgzVrcxJSzrXSFTFHtMJF). Ele é o resumo de um levantamento de 22 páginas cujo PDF completo só existia no Mac e que agora está no clone em `05-levantamento-3d/`. Localize tudo que foi produzido aqui a partir dele (leitura de Liao et al. 2026 e do G-MAD, ortofoto e LiDAR do IPP, prova de conceito de quadra, cenas 3D, qualquer decisão de engine). Se o link apontar para outro e-mail, me avise em vez de supor.
8. Ambiente: versão do Windows, GPU e driver (`nvidia-smi`), Python, PyTorch, CUDA, Ultralytics, caminho de instalação do ARMA 3, e onde fica o ambiente virtual.

PARE. Me mostre o inventário resumido em tabelas e espere meu OK.

## Fase 2. Plano de reconciliação

Monte e me mostre uma tabela de divergências entre o que existe aqui e o que o repositório afirma. Regras de precedência:

- Experimento, código, pipeline, datasets, treino, métricas e ambiente: o DESKTOP prevalece. O que está em `03-arma3/` no clone são os originais de 11/09; suas versões sobrescrevem e o git guarda a diferença.
- Estrutura de pastas, protocolo de sessão, regras do `CLAUDE.md`, manuscrito por seção e `PENDENCIAS.md`: o REPOSITÓRIO prevalece. O conteúdo daqui se encaixa na estrutura de lá. Se algo não couber (cenas 3D, recortes da ortofoto do IPP, dados GIS), proponha pasta numerada nova, por exemplo `07-cenas-3d/` ou `08-dados-ipp/`, com README de manifesto e os arquivos pesados fora do git.
- Conhecimento e pesquisa: vale a união. Onde a pesquisa daqui confirmar, ampliar ou contradisser `docs/CONTEXTO.md` ou `05-levantamento-3d/`, não sobrescreva em silêncio. Registre em `docs/DIVERGENCIAS.md`: o que o Mac afirma, o que o desktop encontrou, a evidência de cada lado, e a sua recomendação. Eu decido.
- Afirmações do repositório que ficaram falsas porque você avançou devem ser corrigidas: `STATUS.md` (seção Experimento e Bloqueios), a frase "As classes atuais são pessoas vistas de cima" em `docs/CONTEXTO.md` se não for mais verdade, os itens C5 e D4 de `01-artigo/PENDENCIAS.md`, e o painel.

Se a pasta atual já for um repositório git com histórico, não descarte esse histórico: me proponha como preservá-lo (por exemplo, importar como branch `historico-desktop` ou guardar um `git bundle` fora do repositório) e espere minha escolha.

PARE. Me mostre a tabela de divergências e o plano de cópia (origem, destino, o que fica de fora e por quê) e espere meu OK.

## Fase 3. Executar

1. Código para `03-arma3/scripts/` (e subpastas que fizerem sentido). Se os scripts têm caminho absoluto da pasta antiga embutido, não conserte agora: liste em `docs/DIVERGENCIAS.md` e proponha a correção (variável de ambiente ou arquivo de configuração) para depois.
2. `06-resultados/RESULTADOS.md`: traga o que existir e acrescente no topo uma "Ficha do experimento para o artigo" com: datasets (imagens, rótulos, classes, splits, convenção de anotação), parâmetros de randomização da cena, modelo e hiperparâmetros, hardware e tempo de treino, métricas no sintético, métricas em imagem real (zero-shot, com fração de real, sintético mais real). Cada número com o arquivo de origem e o comando que o gerou. Número que só existir em conversa ou na sua memória e não em arquivo: regenere com `yolo val` se for barato, senão marque `[SEM ARQUIVO DE ORIGEM]` e não o use.
3. `06-resultados/<nome-do-run>/` para cada run relevante: `args.yaml`, `results.csv`, gráficos PNG e até 10 previews com caixas. Nada de pesos.
4. `06-resultados/ONDE-ESTAO-OS-DADOS.md`: caminho absoluto, tamanho, data e SHA256 de cada arquivo de pesos; caminho, tamanho e contagem de cada dataset. É o que permite ao outro lado saber o que existe sem receber o arquivo.
5. Pesquisa: os documentos produzidos aqui vão para `05-levantamento-3d/desktop/` (ou para a pasta nova aprovada na Fase 2), com um `LEIA-ME.md` de uma página: o que é novo em relação ao levantamento de 12/09, o que muda no desenho do experimento e o que muda no texto do artigo. Toda citação com DOI ou arXiv marcada como conferida ou não conferida. Nunca inventar DOI.
6. `docs/AMBIENTE-DESKTOP.md` com o item 8 do inventário.
7. `docs/CONTEXTO.md`: acrescente uma seção "Vindo do desktop" com o conhecimento da sua memória e das suas notas que o Mac precisa ter. Corrija a linha do tempo com as datas reais do que foi feito aqui.
8. `STATUS.md`: reescreva a seção "Experimento (desktop)" com o estado real, atualize "Próximos passos" e "Bloqueios". `DIARIO.md`: nova entrada no topo, `## AAAA-MM-DD [DESKTOP] Reconciliação com o repositório`, com feito, decidido e o que fica para o Mac.
9. `01-artigo/PENDENCIAS.md`: não resolva pendências de texto agora. Só atualize C5 e D4 apontando para `06-resultados/RESULTADOS.md`, e acrescente itens novos na seção D se a pesquisa daqui trouxer algo que o artigo precisa citar.

## Fase 4. Conferir e publicar

1. `git status` e `git diff --stat`. Confirme que não entrou: pesos, datasets, screenshots brutas, `.rpt`, zips, rasters, e nada de origem PCERJ. Arquivo acima de 5 MB no stage é sinal de erro: pare e me mostre.
2. Commits separados por assunto (código, resultados, pesquisa, estado), mensagens em português. `git pull --rebase` antes do `git push`, porque o Mac pode ter publicado nesse intervalo. Nunca `push --force`.
3. Painel: leia o artifact https://claude.ai/artifact/3XtSXZvhkzovA1ixGZ4rFH, atualize em `painel/painel.html` os blocos marcados com `ESTADO` (carimbo com `[DESKTOP]`, bloco do experimento, os três números se existirem com arquivo de origem, próximos passos, diário) e republique passando esse endereço em `url`. Sem `url` nasce outro painel, o que não queremos. Commit e push da fonte.

## Fase 5. Mudar a base de trabalho

Me diga o que é preciso para passar a trabalhar só em `C:\projetos\machine-vision-favelas`: ambiente virtual (recriar ou apontar), caminhos nos scripts, pasta da missão do ARMA 3, onde os datasets continuam morando. Proponha, não execute sem meu OK. A pasta antiga fica intacta como arquivo morto até eu mandar apagar.

## Regras que valem o tempo todo

- Não apague nem mova nada da pasta antiga. Copie.
- Os ortomosaicos do Jacarezinho e de Manguinhos são dados operacionais da PCERJ: não entram no git, no painel, em pacote nem em serviço externo. Nenhuma coordenada em nível de endereço, nenhuma imagem que identifique morador.
- Não invente número, métrica, citação ou DOI. Na dúvida, mostre o arquivo.
- Em conflito entre os dois lados, não escolha sozinho: registre em `docs/DIVERGENCIAS.md` e me pergunte.
- Pergunte antes de qualquer ação destrutiva ou de reescrever histórico.
- Escreva em português, sem travessão (use vírgula, dois-pontos ou parênteses).
- Relatório final: o que entrou no repositório, o que ficou de fora e onde está, as divergências abertas que dependem de mim, e os três números de sim-to-real com a origem de cada um (ou a informação de que ainda não existem).
