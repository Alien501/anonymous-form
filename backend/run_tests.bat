@echo off
REM Script to run tests on Windows

echo 🧪 Running tests for Anonymous Form Backend...
echo.

REM Set test environment variables
set SECRET_KEY=test-secret-key-local
set JWT_KEY=test-jwt-key-local
set ENVIRONMENT=development
set COOKIE_DOMAIN=localhost
set CLIENT_URL=http://localhost:3000
set EMAIL_HOST_PASSWORD=test-password
set EMAIL_HOST_USER=test@example.com

REM Run migrations first
echo 📦 Running migrations...
python manage.py migrate --noinput

echo.
echo 🚀 Running tests...
echo.

REM Run tests with coverage
pytest --verbose --cov=. --cov-report=term-missing --cov-report=html --cov-report=xml

if %errorlevel% equ 0 (
    echo.
    echo ✅ All tests passed!
    echo.
    echo 📊 Coverage report generated in htmlcov\index.html
    echo    Open it in your browser to see detailed coverage
) else (
    echo.
    echo ❌ Some tests failed!
    exit /b 1
)

