@echo off
cd /d %userprofile%\Documents

rem Verifica se a pasta venvs existe
if not exist venvs (
    echo Criando a pasta venvs...
    mkdir venvs
)

cd venvs

rem Verifica se o virtualenv está instalado
where virtualenv > nul
if %errorlevel% neq 0 (
    echo Instalando o virtualenv...
    pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org virtualenv
)

if not exist posicatvenv (
    virtualenv posicatvenv
)

rem start .



cd /d %userprofile%\Documents\venvs\posicatvenv\Scripts

call activate

cd /d Q:\Clubes e Fundos\_PosiCatcher_Bot

pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt

python main.py

pause
