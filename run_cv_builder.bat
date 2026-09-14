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

REM Derive the JD filename stem (strip the directory) for output naming.
set JD_STEM=%JD_FILE:~18%

REM 1) Tailor the RenderCV YAML to the JD, 2) render it to PDF + previews.
python tailor_cv.py "%JD_FILE%" "3 Custom CV/CV-%JD_STEM%_CV1.yaml"
python build_cv.py --yaml "3 Custom CV/CV-%JD_STEM%_CV1.yaml"

if errorlevel 1 (
    echo.
    echo [!] Document generation failed.
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
