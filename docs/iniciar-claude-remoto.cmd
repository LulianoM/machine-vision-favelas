@echo off
rem Sobe o Claude Code em modo Remote Control na raiz do repositorio.
rem A sessao aparece em https://claude.ai/code e no app do Claude (aba Code).
rem Esta janela precisa ficar aberta.
cd /d "%~dp0.."
claude remote-control --name "desktop-favelas"
pause
