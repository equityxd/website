@echo off
setlocal

REM ============================================
REM   CV Builder — Launcher
REM   Double-click this file to run the whole process:
REM     1. Collect the Job Description (GUI) and save it
REM     2. Auto-generate the tailored documents from that JD
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

REM ---- Step 2: Auto-generate documents from the collected JD ----
echo.
echo [2/2] Generating tailored documents from the collected JD...
echo.

REM Locate the most recently created JD file in "2 Job description".
REM `/od` sorts oldest-first, so keeping the last entry yields the newest.
set JD_FILE=
for /f "delims=" %%a in ('dir /b /od "2 Job description\*.txt" 2>nul') do (
    set JD_FILE=2 Job description\%%a
)

if not defined JD_FILE (
    echo.
    echo [!] No JD .txt file found in "2 Job description".
    echo     Run the collector first (paste the JD and press 'Run process').
    pause
    exit /b 1
)

echo        Using JD: 2 Job description\%JD_FILE%
echo.

REM 1) Generate the JD-tailored CV (.typ + PDF) via the .typ generator.
REM    gen_cv_typ.py <JD.txt>  ->  3 Custom CV/CV-20260912-0005_CV1.typ / .pdf
python gen_cv_typ.py "%JD_FILE%"

if errorlevel 1 (
    echo.
    echo [!] CV generation failed.
    pause
    exit /b 1
)

REM Generate 1 cover letter + 1 interview-prep (Word) and update the monitoring tracker.
python generate_documents.py "2 Job description\%JD_FILE%"

if errorlevel 1 (
    echo.
    echo [!] Cover letter / interview-prep / tracker generation failed.
    pause
    exit /b 1
)

echo.
echo Done — your tailored document(s) are generated.
pause

endlocal
