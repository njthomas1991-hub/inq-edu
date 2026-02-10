# Fix Cloudinary issue and start Django server
Write-Host "=== FIXING CLOUDINARY PYTHON 3.14 COMPATIBILITY ISSUE ===" -ForegroundColor Yellow

# Step 1: Navigate to backend directory
Set-Location "D:\vs-projects\inq-ed\myproject\backend"

# Step 2: Uninstall cloudinary packages
Write-Host "`nStep 1: Uninstalling Cloudinary packages..." -ForegroundColor Cyan
pip uninstall cloudinary django-cloudinary-storage -y

# Step 3: Run migrations  
Write-Host "`nStep 2: Applying database migrations..." -ForegroundColor Cyan
python manage.py migrate

# Step 4: Start server
Write-Host "`nStep 3: Starting Django development server..." -ForegroundColor Cyan
Write-Host "Server will start at http://localhost:8000" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server`n" -ForegroundColor Yellow

python manage.py runserver
