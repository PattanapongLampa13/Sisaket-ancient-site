#!/bin/bash

# Exit on error
set -o errexit

# Clean previous builds
rm -rf staticfiles
# Build the project
echo "Building the project..."
python3.9 -m pip install -r requirements.txt

echo "Collect Static..."
python3.9 manage.py collectstatic --noinput --clear
#!/bin/bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
