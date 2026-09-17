# Prompt de migração para o Claude Code do desktop

Abrir o Claude Code na pasta ANTIGA de trabalho do desktop (a que veio do pacote de 11/09) e colar o bloco abaixo.

---

Este projeto passou a ter um repositório git único, compartilhado com o MacBook, clonado em `C:\projetos\machine-vision-favelas`. A pasta em que você está agora é a antiga, criada a partir do pacote de 11/09. Sua tarefa é levar para o repositório tudo que foi produzido aqui, sem perder nada e sem levar o que não deve ir. Faça nesta ordem:

1. Leia, no repositório novo: `CLAUDE.md`, `STATUS.md`, `DIARIO.md` e `docs/CONTEXTO.md`. As regras de lá valem a partir de agora.

2. Faça o inventário desta pasta antiga e me mostre antes de copiar qualquer coisa:
   - quais arquivos de `03-arma3/scripts/` mudaram em relação aos originais (compare com os do repositório novo, que são os originais de 11/09) e quais scripts novos existem;
   - se existe `RESULTADOS.md` e o que ele registra;
   - onde estão datasets, screenshots do ARMA, arquivos `.rpt`, pastas `runs/` e pesos `.pt`, com tamanho de cada um;
   - qualquer nota, log ou decisão escrita fora desses lugares.

3. Copie para o repositório novo:
   - scripts alterados e novos para `03-arma3/scripts/` (sobrescreva: o git mostra a diferença);
   - `RESULTADOS.md` para `06-resultados/RESULTADOS.md`;
   - de cada treino: `results.csv`, `args.yaml` e os gráficos PNG para `06-resultados/<nome-do-run>/`. Até 10 imagens de preview com caixas por run;
   - NÃO copie pesos, datasets, screenshots brutas nem `.rpt`. Eles ficam onde estão.

4. Crie `06-resultados/ONDE-ESTAO-OS-DADOS.md` com o caminho absoluto, o tamanho e a data de cada dataset, pasta de runs e arquivo de pesos desta máquina, para que o outro lado saiba o que existe e onde.

5. Crie `docs/AMBIENTE-DESKTOP.md`: versão do Windows, GPU e driver (`nvidia-smi`), versão do Python, do PyTorch, do CUDA e do Ultralytics, caminho da instalação do ARMA 3 e da pasta da missão.

6. Atualize `STATUS.md`, seção "Experimento (desktop)", com o estado real: o que já rodou, o que está rodando, métricas obtidas (só as que estão em arquivo, com o comando que as gerou), o que travou. Acrescente no topo de `DIARIO.md` uma entrada `## AAAA-MM-DD [DESKTOP] Migração para o repositório`.

7. Rode `git status` e confira que nenhum arquivo grande nem sensível entrou. Depois commit e `git push`.

8. Me diga se o ambiente virtual do Python precisa ser recriado na pasta nova ou se dá para apontar para o atual. A partir daqui vamos trabalhar só em `C:\projetos\machine-vision-favelas`.

Regras: não apague nada desta pasta antiga. Não invente número: métrica sem arquivo de origem não entra. Ortomosaicos do Jacarezinho e de Manguinhos são dados sensíveis da PCERJ e não entram no git em hipótese alguma. Escreva em português, sem travessão. Pergunte antes de qualquer ação destrutiva.
