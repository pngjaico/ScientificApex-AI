@echo off
cd /d "%~dp0"

where opencode >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    opencode "%~dp0"
    goto end
)

if exist "%LOCALAPPDATA%\Programs\ai.opencode.desktop\OpenCode.exe" (
    start "" "%LOCALAPPDATA%\Programs\ai.opencode.desktop\OpenCode.exe" "%~dp0"
    goto end
)

if exist "%LOCALAPPDATA%\Programs\ai.opencode.desktop\resources\opencode-cli.exe" (
    "%LOCALAPPDATA%\Programs\ai.opencode.desktop\resources\opencode-cli.exe" "%~dp0"
    goto end
)

echo [ERRO] Binario do OpenCode nao encontrado no PATH nem em %LOCALAPPDATA%\Programs\ai.opencode.desktop.
pause

:end
