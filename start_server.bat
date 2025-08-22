@echo off
echo Starting Arogya Backend Server...
echo.

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Running migrations...
python manage.py makemigrations
python manage.py migrate

echo.
echo Starting Django server on 0.0.0.0:8000...
echo Server will be accessible from mobile devices at http://192.168.1.74:8000
echo.
python manage.py runserver 0.0.0.0:8000
