@echo off
setlocal EnableDelayedExpansion

echo ==============================================
echo       Medical Diagnosis System Launcher
echo ==============================================

REM Get the absolute path to the project root and models directory
set "PROJECT_ROOT=%~dp0"
set "MODELS_DIR=%PROJECT_ROOT%models"

REM Remove any potential trailing spaces
set "MODELS_DIR=%MODELS_DIR: =%"

REM Change to the codebase directory 
cd /d "%PROJECT_ROOT%codebase"
if errorlevel 1 (
  echo Error: Could not change to codebase directory.
  goto :error
)

REM Check if models directory exists at project root
if not exist "%MODELS_DIR%" (
  echo Notice: Models directory not found at %MODELS_DIR%
  echo Creating models directory at project root...
  mkdir "%MODELS_DIR%"
)

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
  echo Error: Python is not installed. Please install Python 3 and try again.
  goto :error
)

REM Get the local IP address
for /f "tokens=*" %%a in ('powershell -Command "Get-NetIPAddress -AddressFamily IPv4 -InterfaceIndex $(Get-NetConnectionProfile | Select-Object -ExpandProperty InterfaceIndex) | Select-Object -ExpandProperty IPAddress"') do (
  set "IP_ADDRESS=%%a"
)
if not defined IP_ADDRESS (
  set "IP_ADDRESS=localhost"
)

REM Check for port 5000 usage and force kill if needed
netstat -ano | find ":5000" > nul
if %ERRORLEVEL% EQU 0 (
  echo Warning: Port 5000 is already in use.
  echo Attempting to close the application using port 5000...
  
  for /f "tokens=5" %%a in ('netstat -ano ^| find ":5000"') do (
    if not "%%a"=="" (
      echo Killing process with PID %%a
      taskkill /F /PID %%a /T
      if !ERRORLEVEL! EQU 0 (
        echo Successfully closed the application.
      ) else (
        echo Failed to close the application. Please close it manually.
      )
    )
  )
)

REM Start the server with the models directory path
echo Starting server...
set "MODELS_PATH=%MODELS_DIR%"

start "Medical Diagnosis Server" cmd /c "set MODELS_PATH=%MODELS_DIR% && python server.py > server_log.txt 2>&1"

REM Wait for the server to start and check its health
echo Waiting for server to initialize...
echo This may take up to 8 seconds...

REM Give the server some time to start before checking
timeout /t 3 /nobreak > nul

set SERVER_READY=0
for /l %%i in (1, 1, 5) do (
  timeout /t 1 /nobreak > nul
  echo Checking server health %%i/5...
  curl -s http://localhost:5000/health > nul 2>&1
  if !ERRORLEVEL! EQU 0 (
    set SERVER_READY=1
    echo Server is ready!
    goto :server_ready
  )
)

:server_check_result
if %SERVER_READY% EQU 0 (
  echo Error: Server failed to start properly.
  echo Checking server log for errors:
  if exist server_log.txt (
    type server_log.txt
  ) else (
    echo No server log file found.
  )
  goto :error
)

:server_ready
echo ==============================================
echo Medical Diagnosis System is now running!
echo ==============================================
echo.
echo Access the web interface at:
echo   http://localhost:5000  (local access)
echo   http://%IP_ADDRESS%:5000  (network access)
echo.
echo Opening web browser...
start "" http://localhost:5000

echo Press any key to exit and shutdown the server...
pause > nul

REM Clean up when user exits
echo Cleaning up...
taskkill /f /fi "WINDOWTITLE eq Medical Diagnosis Server" >nul 2>&1
echo Done.
goto :eof

:error
echo An error occurred during startup.
pause
exit /b 1