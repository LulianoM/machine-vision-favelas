@echo off
setlocal
set "WS=C:\Program Files (x86)\Steam\steamapps\workshop\content\107410"
set "MODS=C:\arma3-favela\mods"
if not exist "%MODS%" mkdir "%MODS%"

call :link 450814997 cba_a3
call :link 497660133 cup_weapons
call :link 823636749 mlo
call :link 2127118261 rjfac
call :link 2223739438 braf
call :link 1195440524 opesp
call :link 2938490553 bfmmaps
call :link 2748362927 bfmstructures
call :link 3027801658 favelaprops
echo.
echo Concluido. Pastas de mod em %MODS%
exit /b

:link
if not exist "%WS%\%1" (
  echo [FALTANDO] @%2  (id %1 ainda nao baixado pela Steam)
  exit /b
)
if exist "%MODS%\@%2" (
  echo [ok] @%2 ja existe
  exit /b
)
mklink /J "%MODS%\@%2" "%WS%\%1" >nul
echo [link] @%2 -^> %1
exit /b
