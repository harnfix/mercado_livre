@echo off

rem Atualiza o pip para a versão mais recente
python -m pip install --upgrade pip

rem Instala as dependências listadas no requirements.txt
python -m pip install -r requirements.txt

echo Instalação concluída.