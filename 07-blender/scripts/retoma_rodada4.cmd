@echo off
rem Retoma a rodada 4 do projeto machine-vision-favelas (atalho na pasta Inicializar, pedido do
rem autor em 25/09; rodada 4 em 27/09). Abre o supervisor numa janela minimizada propria e sai. O supervisor lanca a
rem cadeia se ela nao estiver rodando e se apaga da inicializacao quando a rodada termina.
rem Pode ser executado a qualquer momento: se ja houver supervisor rodando, o novo sai sozinho.
cd /d C:\arma3-favela\blender
start "rodada4 - nao feche" /min "C:\arma3-favela\venv\Scripts\python.exe" -u "C:\projetos\machine-vision-favelas\07-blender\scripts\supervisiona_rodada4.py"
