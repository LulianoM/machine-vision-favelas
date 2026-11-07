@echo off
set ODM_NONINTERACTIVE=1
pushd C:\ODM
echo cwd=%CD%
call C:\ODM\win32env.bat
python -X utf8 C:\ODM\run.py %*
popd
