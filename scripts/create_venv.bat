echo Creating Python Virtual Environment
call py -3.8 -m venv ../py-env
call ../py-env/Scripts/activate.bat
call pip install -r ../requirements.txt
echo Virtual Environment Created