@echo off
chcp 65001 >nul
title MERLIN PDF TOOL - Setup Checker
color 0E
cls

echo.
echo  ============================================
echo    MERLIN PDF TOOL - SETUP CHECKER
echo  ============================================
echo.
echo  This tool checks if your system is ready
echo  to run MERLIN PDF TOOL.
echo.
echo  Checking requirements...
echo.
echo  --------------------------------------------

set ALL_GOOD=1

:: Check Python
echo  [1/4] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo     X PYTHON NOT FOUND
echo     ^   Install from: https://python.org
echo     ^   IMPORTANT: Check "Add Python to PATH"
    set ALL_GOOD=0
) else (
    for /f "tokens=*" %%a in ('python --version 2^>^&1') do echo     + Found: %%a
)

:: Check pip
echo.
echo  [2/4] Checking pip (Python package manager)...
pip --version >nul 2>&1
if errorlevel 1 (
    echo     X PIP NOT FOUND
echo     ^   Usually installed with Python. Reinstall Python if missing.
    set ALL_GOOD=0
) else (
    for /f "tokens=*" %%a in ('pip --version 2^>^&1') do echo     + Found: %%a
)

:: Check Poppler (pdftoppm)
echo.
echo  [3/4] Checking Poppler (needed for PDF-to-PNG)...
pdftoppm -v >nul 2>&1
if errorlevel 1 (
    echo     X POPPLER NOT FOUND
echo     ^   Download from: https://github.com/oschwartz10612/poppler-windows/releases
echo     ^   Extract to C:\poppler, then add C:\poppler\bin to PATH
    set ALL_GOOD=0
) else (
    echo     + Found: pdftoppm is available
)

:: Check Ghostscript
echo.
echo  [4/4] Checking Ghostscript (needed for PDF compression)...
gswin64c -version >nul 2>&1
if errorlevel 1 (
    gswin32c -version >nul 2>&1
    if errorlevel 1 (
        echo     X GHOSTSCRIPT NOT FOUND
echo     ^   Download from: https://www.ghostscript.com/download/gsdnld.html
echo     ^   Install and check "Add to PATH" during setup
        set ALL_GOOD=0
    ) else (
        for /f "tokens=*" %%a in ('gswin32c --version 2^>^&1') do echo     + Found: Ghostscript 32-bit %%a
    )
) else (
    for /f "tokens=*" %%a in ('gswin64c --version 2^>^&1') do echo     + Found: Ghostscript 64-bit %%a
)

echo.
echo  --------------------------------------------

if %ALL_GOOD%==1 (
    color 0A
    echo.
    echo  +++ ALL CHECKS PASSED +++
    echo.
    echo  Your system is ready! You can now run:
    echo     RUN_MERLIN.bat
    echo.
    echo  The tool will auto-install Python packages
    echo  on first run (pdf2image, pillow, pypdf, reportlab).
    echo.
) else (
    color 0C
    echo.
    echo  !!! SETUP INCOMPLETE !!!
    echo.
    echo  Please install the missing items above,
    echo  then run this checker again.
    echo.
    echo  HOW TO ADD TO PATH:
    echo    1. Press Windows key, type "environment"
    echo    2. Click "Edit the system environment variables"
    echo    3. Click "Environment Variables"
    echo    4. Under "User variables", find "Path" -> Edit
    echo    5. Click "New" and add the folder path
    echo    6. Click OK, then restart Command Prompt
    echo.
)

pause