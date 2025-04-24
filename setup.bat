@echo off
SETLOCAL ENABLEEXTENSIONS

echo Starting setup for Action Suggester on Windows...

REM 1. Create virtual environment
echo Creating virtual environment...
python -m venv env

REM 2. Activate virtual environment
call env\Scripts\activate.bat

REM 3. Upgrade pip and install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM 4. Rename .example.env to .env
if exist ".example.env" (
    echo Renaming .example.env to .env...
    rename .example.env .env
) else (
    echo .example.env not found. Skipping rename.
)

REM 5. Ask user to manually create PostgreSQL database
echo  Please ensure your PostgreSQL database is created manually.
echo    You can use pgAdmin or run SQL in psql:
echo.
echo    CREATE DATABASE actionsuggester;
echo.
pause

REM 6. Apply Django migrations
echo  Applying Django migrations...
python manage.py makemigrations
python manage.py migrate

REM 7. Final instructions
echo  Setup complete!
echo To activate your virtual environment next time, run:
echo    env\Scripts\activate
echo To start the development server, run:
echo    python manage.py runserver

pause
ENDLOCAL
