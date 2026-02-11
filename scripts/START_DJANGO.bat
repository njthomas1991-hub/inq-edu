@echo off
echo ====================================
echo  FIXING DJANGO SERVER STARTUP ISSUE
echo ====================================
echo.

cd /d "D:\vs-projects\inq-ed\myproject"

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo Uninstalling Cloudinary (Python 3.14 incompatible)...
pip uninstall cloudinary django-cloudinary-storage -y

echo.
echo Running database migrations...
cd backend
python manage.py migrate

echo.
echo ====================================
echo  STARTING DJANGO SERVER
echo ====================================
echo Server will run at: http://localhost:8000
echo Press Ctrl+C to stop the server
echo.

python manage.py runserver

pause
