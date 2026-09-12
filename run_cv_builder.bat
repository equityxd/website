@echo off
setlocal

REM ============================================
REM   CV Builder — Launcher
REM   Double-click this file to run the whole process:
REM     1. Collect the Job Description (GUI) and set up files
REM     2. Launch pi (the LLM) so documents can be generated
REM ============================================

cd /d C:\MyDev\MyCV

echo ============================================
echo   CV Builder — Launcher
echo ============================================
echo.

REM ---- Step 1: Data collection GUI ----
echo [1/2] Opening the Data Collection GUI...
echo        Paste the Job Description (or a URL) and press OK.
echo.
python collect_cv.py

if errorlevel 1 (
    echo.
    echo [!] The collector stopped with an error.
    pause
    exit /b 1
)

REM ---- Step 2: Launch pi (LLM) ----
echo.
echo [2/2] Launching pi (LLM terminal)...
echo.
start "" cmd /c "pi"

endlocal
