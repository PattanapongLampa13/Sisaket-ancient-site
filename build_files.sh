#!/bin/bash
set -o errexit

echo "Starting build process..."

echo "Installing requirements..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Verifying static files collection..."
if [ -d "staticfiles" ]; then
    echo "✓ staticfiles directory exists"
    echo "Static files count: $(find staticfiles -type f | wc -l)"
    echo "Sample files:"
    find staticfiles -name "*.css" -o -name "*.js" -o -name "*.png" -o -name "*.jpg" | head -10
else
    echo "✗ staticfiles directory not found!"
    exit 1
fi

echo "Build completed successfully!"
