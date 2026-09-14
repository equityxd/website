@echo off
rem -----------------------------------------------------------
rem  CV Builder Dashboard — launcher
rem  Opens the dashboard in your default browser and runs the
rem  FastAPI server locally.
rem -----------------------------------------------------------
cd /d "%~dp0\.."
python -m pip install -r cv_dashboard/requirements.txt >nul 2>&1

set HOST=127.0.0.1
set PORT=8000

echo -----------------------------------------------------------
echo  CV Builder Dashboard
echo  Host:    %HOST%
echo  Port:    %PORT%
echo  Press Ctrl+C to stop the server.
echo -----------------------------------------------------------

cd /d "%~dp0"
start http://%HOST%:%PORT%/

python -m uvicorn app:app --host %HOST% --port %PORT% --reload
