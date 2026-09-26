@echo off
echo STARTING SETUP...
echo.

:: Check for Node.js
node -v >nul 2>&1
if %ERRORLEVEL% NEQ 0 goto NODE_MISSING

:: ONE: Node is found
echo [V] Node.js is installed.
echo.
echo [*] Installing dependencies...
call npm install
if %ERRORLEVEL% NEQ 0 goto NPM_FAIL

:: TWO: Dependencies installed
echo.
echo [V] Setup complete!
echo.
echo [*] Starting Astro server...
echo [*] Press Ctrl+C to stop the server later.
echo.
call npm run dev
goto END

:NODE_MISSING
echo [!] Node.js is NOT installed (or not in your PATH).
echo.
echo [*] I will open the download page for you.
echo [*] Please download and install the "LTS" version.
echo.
timeout /t 3
start https://nodejs.org/
echo.
echo [!] After installing, close this window and run setup.bat again.
goto END

:NPM_FAIL
echo [!] npm install failed.
echo [!] Please check your internet connection and try again.
goto END

:END
echo.
echo [!] Script finished. Press any key to close.
pause
