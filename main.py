import sys
from PyQt5.QtWidgets import QApplication
from tela_login import Login

app = QApplication(sys.argv)
estoque = Login()
estoque.tela_login.show()
app.exec()

'''
- 'pip freeze' para ver pacotes instalados
- 'pip install virtualenv'
- 'python -m venv venv' para criar ambiente virtual
- '.\venv\Scripts\activate.bat' para ativar ambiente virtual
- 'deactivate' para desativar ambiente virtual
- 'pipenv --help' para ver mais comandos do pipenv
- 'pip install -r requirements.txt' para instalar tudo em requirements.txt
'''
# pyinstaller --onefile --noconsole --windowed -i nomeícone.ico nomecódigo.py

# pyinstaller --onefile --noconsole --windowed -i .\icone.ico '.\main.py'
