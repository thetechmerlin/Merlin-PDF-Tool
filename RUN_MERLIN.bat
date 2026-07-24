@echo off
chcp 65001 >nul
title MERLIN PDF TOOL
color 0B
cls

echo.
echo  ============================================
echo    WELCOME TO MERLIN PDF TOOL
echo  ============================================
echo.
echo  This toolkit provides 6 offline PDF features:
echo.
echo    [1] MERGE PDFs       - Combine with page numbers
echo    [2] PDF to PNG       - Batch convert at custom DPI
echo    [3] DOWNSAMPLE       - Compress PDF file size
echo    [4] PNG to PDF       - Merge or individual PDFs
echo    [5] JPG to PNG       - Image format conversion
echo    [6] PNG to JPG       - Image format conversion
echo.
echo  --------------------------------------------
echo  FOLDER STRUCTURE:
echo    pdfs/       - Input for Merge and PDF-to-PNG
echo    pngs/       - PNG outputs
echo    lrgpdf/     - Input for PDF compression
echo    smallpdf/   - Compressed PDF outputs
echo    PNGtoPDF/   - PNGs to convert to PDF
echo    JPG/        - Images for format conversion
echo    Conversions/ - Converted image outputs
echo  --------------------------------------------
echo.
echo  Checking Python installation...
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo  X Python not found!
    echo  Please install Python 3.x from https://python.org
    echo  Make sure to check "Add Python to PATH"
    pause
    exit /b 1
)

echo  + Python found
echo  Launching Merlin Engine...
echo.

python "%~dp0merlin_engine.py"

pause