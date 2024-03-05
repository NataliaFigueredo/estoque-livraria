from PyQt5.QtWidgets import QMessageBox, QLineEdit
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from estoque import Estoque
from banco.criar_banco import Banco
from banco.comandos import Query


class Login():
    def __init__(self):
        super().__init__()
        self.tela_login = uic.loadUi('./interface/tela_login.ui')
        Banco('./banco/estoque.db')
        self.comandos_db = Query('./banco/estoque.db')
        self.tela_login.setWindowTitle("Acesso ao estoque")
        self.tela_login.setWindowIcon(QIcon("./interface/icone.ico"))
        self.tela_login.btn_login.clicked.connect(self.validar_login)
        self.tela_login.txt_senha.returnPressed.connect(self.validar_login)
        self.tela_login.mostraSenha.clicked.connect(self.mostra_senha)

    # def login(self):
    #     usuario = self.tela_login.txt_usuario.text()
    #     senha = self.tela_login.txt_senha.text()

    #     if usuario == 'admin' and senha == 'admin':
    #         self.estoque = Estoque()
    #         self.estoque.show()
    #         self.tela_login.close()
    #     else:
    #         QMessageBox.warning(self.tela_login, 'Error',
    #                             'Usuário ou Senha inválidos')

    def mostra_senha(self):
        if self.tela_login.mostraSenha.isChecked():
            self.tela_login.mostraSenha.setIcon(
                QIcon('./interface/eye_visible.png'))
            self.tela_login.txt_senha.setEchoMode(QLineEdit.Normal)
        else:
            self.tela_login.mostraSenha.setIcon(
                QIcon('./interface/eye_hidden.png'))
            self.tela_login.txt_senha.setEchoMode(
                QLineEdit.Password)

    def validar_login(self):
        usuario = self.tela_login.txt_usuario.text()
        senha = self.tela_login.txt_senha.text()
        perfil = self.comandos_db.validar_usuario(usuario, senha)

        if perfil == 'administrador' or perfil == 'usuario':
            self.estoque = Estoque(perfil)
            self.estoque.show()
            self.tela_login.close()
        else:
            QMessageBox.warning(self.tela_login, 'Error',
                                'Usuário ou Senha inválidos')


# app = QApplication(sys.argv)
# estoque = Login()
# estoque.tela_login.show()
# app.exec()
