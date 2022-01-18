@echo off

call %~dp0HSE_Bot\venv\Scripts\activate

cd %~dp0HSE_Bot

python app.py

pause