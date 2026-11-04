@echo off
rem Retoma a rodada 6 do projeto machine-vision-favelas (PLANO-RODADA6.md, secao 4). Duplo clique, ou
rem um atalho retoma_rodada6.lnk na pasta Inicializar (criado so com o OK do autor). Abre o supervisor
rem numa janela minimizada propria e sai. O supervisor lanca a cadeia se ela nao estiver rodando e
rem apaga o atalho de inicializacao quando a rodada termina. Nunca pelo Agendador de Tarefas nem pelo
rem WMI: ali o Blender nasce sem o MPFB.
rem Pode ser executado a qualquer momento: se ja houver supervisor rodando, o novo sai sozinho.
cd /d C:\arma3-favela\blender
start "rodada6 - nao feche" /min "C:\arma3-favela\venv\Scripts\python.exe" -u "C:\projetos\machine-vision-favelas\07-blender\scripts\supervisiona_rodada6.py"
