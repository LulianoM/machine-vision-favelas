@echo off
rem Lanca r_sel.py (item 4 de O-QUE-FALTA-NO-SERVIDOR.md) na sua propria janela e grava o log.
rem Pode ser executado de novo a qualquer momento: cada etapa so roda se a saida nao existir e o
rem treino retoma de last.pt. Lancar da sessao com
rem   Start-Process cmd.exe -ArgumentList '/c "C:\projetos\machine-vision-favelas\07-blender\scripts\lanca_r_sel.cmd"' -WindowStyle Minimized
cd /d C:\arma3-favela\blender
"C:\arma3-favela\venv\Scripts\python.exe" -u -X utf8 "C:\projetos\machine-vision-favelas\07-blender\scripts\r_sel.py" >> C:\arma3-favela\blender\r_sel.log 2>&1
