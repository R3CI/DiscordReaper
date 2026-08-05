@echo off
setlocal enabledelayedexpansion
title DiscordReaper - Fix
color 0A

echo.
echo  DiscordReaper - Setup Check
echo  ----------------------------
echo.

set PASS=0
set FAIL=0

echo [1/7] Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo  [FAIL] Python not found in PATH.
    echo         https://python.org/downloads  -- check "Add Python to PATH"
    set /a FAIL+=1
    goto :check_pip_skip
)

for /f "tokens=2" %%v in ('python --version 2^>^&1') do set PYVER=%%v
echo  [OK]   Python %PYVER%

for /f "tokens=1,2 delims=." %%a in ("%PYVER%") do (
    set PYMAJ=%%a
    set PYMIN=%%b
)
if %PYMAJ% LSS 3 (
    echo  [FAIL] Need Python 3.8+, you have %PYVER%
    set /a FAIL+=1
) else if %PYMAJ% EQU 3 if %PYMIN% LSS 8 (
    echo  [FAIL] Need Python 3.8+, you have %PYVER%
    set /a FAIL+=1
) else (
    set /a PASS+=1
)

:check_pip
echo [2/7] pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo  [FAIL] pip missing, trying ensurepip...
    python -m ensurepip --upgrade
    python -m pip --version >nul 2>&1
    if errorlevel 1 (
        echo  [FAIL] Could not install pip. Run: python -m ensurepip --upgrade
        set /a FAIL+=1
        goto :check_requirements
    )
)
for /f "tokens=2" %%v in ('python -m pip --version 2^>^&1') do set PIPVER=%%v
echo  [OK]   pip %PIPVER%
set /a PASS+=1
goto :check_requirements

:check_pip_skip
echo  [SKIP] pip (Python not found)

:check_requirements
echo [3/7] Requirements...
if not exist "requirements.txt" (
    echo  [FAIL] requirements.txt not found - wrong folder?
    set /a FAIL+=1
    goto :check_webview2
)
python -m pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo  [FAIL] Install failed. Run: python -m pip install -r requirements.txt
    set /a FAIL+=1
) else (
    echo  [OK]   All packages installed
    set /a PASS+=1
)

:check_webview2
echo [4/7] WebView2 Runtime...
reg query "HKLM\SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}" >nul 2>&1
if not errorlevel 1 (
    echo  [OK]   WebView2 found (system)
    set /a PASS+=1
    goto :check_imports
)
reg query "HKCU\SOFTWARE\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}" >nul 2>&1
if not errorlevel 1 (
    echo  [OK]   WebView2 found (user)
    set /a PASS+=1
    goto :check_imports
)
echo  [WARN] WebView2 not found. May still work if Edge is installed.
echo         https://developer.microsoft.com/en-us/microsoft-edge/webview2/

:check_imports
echo [5/7] Imports...
python -c "import webview" >nul 2>&1
if errorlevel 1 (echo  [FAIL] webview  -- pip install pywebview & set /a FAIL+=1) else (echo  [OK]   webview & set /a PASS+=1)

python -c "import requests" >nul 2>&1
if errorlevel 1 (echo  [FAIL] requests  -- pip install requests & set /a FAIL+=1) else (echo  [OK]   requests & set /a PASS+=1)

python -c "from ruamel.yaml import YAML" >nul 2>&1
if errorlevel 1 (echo  [FAIL] ruamel.yaml  -- pip install ruamel.yaml & set /a FAIL+=1) else (echo  [OK]   ruamel.yaml & set /a PASS+=1)

python -c "from curl_cffi import requests" >nul 2>&1
if errorlevel 1 (echo  [FAIL] curl_cffi  -- pip install curl_cffi & set /a FAIL+=1) else (echo  [OK]   curl_cffi & set /a PASS+=1)

echo [6/7] Files...
set MISSING=0
for %%f in (main.py src\gui.py src\spread.py src\checker.py src\admincap.py src\evaluator.py src\rarechecker.py src\tokencapture.py src\__init__.py src\utils\discord.py src\utils\files.py src\utils\config.py src\utils\sessionmanager.py src\utils\logging.py src\utils\http.py) do (
    if not exist "%%f" (
        echo  [FAIL] Missing: %%f
        set /a MISSING+=1
        set /a FAIL+=1
    )
)
if %MISSING% EQU 0 (echo  [OK]   All files present & set /a PASS+=1)

echo [7/7] Project import...
python -c "from src import *; from src.utils.files import files; from src.gui import startgui" >nul 2>&1
if errorlevel 1 (
    echo  [FAIL] Import error. Run this for details:
    echo         python -c "from src import *; from src.utils.files import files; from src.gui import startgui"
    set /a FAIL+=1
) else (
    echo  [OK]   OK
    set /a PASS+=1
)

echo.
echo  %PASS% passed, %FAIL% failed
if %FAIL% EQU 0 (echo  Ready. Run: python main.py) else (echo  Fix the errors above then run: python main.py)
echo.
pause
endlocal
