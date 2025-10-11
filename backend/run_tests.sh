#!/bin/bash

# Script to run tests locally

echo "🧪 Running tests for Anonymous Form Backend..."
echo ""

# Set test environment variables
export SECRET_KEY="test-secret-key-local"
export JWT_KEY="test-jwt-key-local"
export ENVIRONMENT="development"
export COOKIE_DOMAIN="localhost"
export CLIENT_URL="http://localhost:3000"
export EMAIL_HOST_PASSWORD="test-password"
export EMAIL_HOST_USER="test@example.com"

# Run migrations first
echo "📦 Running migrations..."
python manage.py migrate --noinput

echo ""
echo "🚀 Running tests..."
echo ""

# Run tests with coverage
pytest --verbose --cov=. --cov-report=term-missing --cov-report=html --cov-report=xml

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ All tests passed!"
    echo ""
    echo "📊 Coverage report generated in htmlcov/index.html"
    echo "   Open it in your browser to see detailed coverage"
else
    echo ""
    echo "❌ Some tests failed!"
    exit 1
fi

