@echo off

REM Check if virtual environment exists
if not exist ".venv" (
    python -m venv .venv
    echo Created new virtual environment
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Install requirements if they exist
if exist "requirements.txt" (
    pip install -r requirements.txt
    echo Installed requirements
) else (
    echo Warning: requirements.txt not found
)

REM Run the main program
python main.py

REM Deactivate virtual environment
deactivate