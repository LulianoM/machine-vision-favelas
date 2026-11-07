@echo off
setlocal
set "ARMA=C:\Program Files (x86)\Steam\steamapps\common\Arma 3"
set "M=C:\arma3-favela\mods"

set "MODPARAM=%M%\@cba_a3;%M%\@cup_weapons;%M%\@mlo;%M%\@rjfac;%M%\@braf;%M%\@opesp;%M%\@bfmmaps;%M%\@bfmstructures;%M%\@favelaprops"

echo Iniciando Arma 3 (client) com mods de favela...
start "" "%ARMA%\arma3_x64.exe" -mod="%MODPARAM%" -noSplash -skipIntro -world=empty
