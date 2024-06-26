
start cmd /K "" runnerFrontend.bat 
cd ..
cd .\backend\ 
if exist "requirements_satisfied.txt" goto already_run
echo "requirements installed" > "requirements_satisfied.txt"
pip install -r requirements.txt
goto already_run

:already_run
python app.py
