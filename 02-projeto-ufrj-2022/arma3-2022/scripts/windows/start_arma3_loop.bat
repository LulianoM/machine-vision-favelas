@echo off
cd /d "C:\Program Files (x86)\Steam\steamapps\common\Arma 3"
set "WS=C:\Program Files (x86)\Steam\steamapps\common\Arma 3\!Workshop"
start "" "arma3_x64.exe" -beservice -nosplash -noPause -skipIntro -mod="%WS%\@CBA_A3;%WS%\@CUP Weapons;%WS%\@VSM All-In-One Collection;%WS%\@RJFAC - Rio's Factions;%WS%\@@Construções BR;%WS%\@BRAF - Brazilian Armed Forces A3"
