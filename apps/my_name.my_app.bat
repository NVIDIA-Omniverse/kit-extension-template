@echo off
setlocal
call "%~dp0..\kit\kit.exe" "%%~dp0my_name.my_app.kit"  %*
