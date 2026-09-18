# Missão capturaDataset: como rodar

## Arquivos desta pasta
- `capturaDataset.sqf`: script de captura (spawna unidades, randomiza cena/câmera/clima, loga bounding boxes)
- `init.sqf`: chama o script ao iniciar a missão

## Passos

1. Abrir Arma 3 → **Editor** (Eden) → mapa **Tanoa**.
2. Colocar 1 unidade de jogador (qualquer lado, pode ser um civil) num canto afastado.
3. (Opcional, recomendado) Colocar marcadores (F6) chamados `ds_centro_1`, `ds_centro_2`, ... nos pontos de cena: becos, lajes, ruas estreitas, escadas. Sem marcadores, o script usa a posição do jogador como centro único.
4. Salvar a missão (ex.: `dsFavela`). O Arma cria a pasta da missão automaticamente.
5. Fechar o jogo e copiar estes 2 arquivos para a pasta da missão:
   - `C:\Users\marti\Documents\Arma 3\missions\dsFavela.Tanoa\`
   - ou `C:\Users\marti\Documents\Arma 3 - Other Profiles\<perfil>\missions\dsFavela.Tanoa\`
6. Reabrir Arma 3 → **Play Scenario** → `dsFavela`. Deixar rodando; o hint mostra o progresso.

## Saídas
- PNGs em `Documents\Arma 3\Screenshots\`
- Labels (linhas `DSIMG` / `DSLBL`) em `%LOCALAPPDATA%\Arma 3\arma3_<data>.rpt`

## Configuração sugerida do jogo
- Resolução 1920x1080 ou maior (a screenshot sai na resolução de render)
- Video → Interface size: "Small" ou "Normal"
- Desativar Blur e Bloom para imagens mais limpas

## Ajuste de volume
No topo do `capturaDataset.sqf`: `DS_N_IMAGENS` (comece com 30 para validar, depois 500+), `DS_ALT_MIN/MAX`, `DS_PITCH_MIN/MAX`, `DS_MIN_UNIDADES/DS_MAX_UNIDADES`.
