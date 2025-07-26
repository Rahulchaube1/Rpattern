@echo off
echo 🚀 RPattern Installation Script
echo Creator: Rahul Chaube
echo ===============================================
echo.

echo Installing Python dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo ❌ Installation failed!
    echo Please make sure you have Python and pip installed.
    pause
    exit /b 1
)

echo.
echo ✅ Dependencies installed successfully!
echo.

echo Running test suite...
python src\test_rpattern.py

if %errorlevel% neq 0 (
    echo.
    echo ⚠️  Some tests failed, but RPattern may still work.
    echo Check the output above for details.
) else (
    echo.
    echo 🎉 All tests passed! RPattern is ready to use.
)

echo.
echo 🚀 Quick Start Commands:
echo   python src\demo.py              # Run full demo
echo   python src\pattern_generator.py # Generate patterns  
echo   python src\pattern_scanner.py   # Scan patterns
echo.

pause
