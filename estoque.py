import base64
import re

import sqlite3
from datetime import datetime
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem, QFileDialog
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtChart import QChart, QChartView, QPieSeries
from PyQt5.QtGui import QPixmap, QIcon, QPainter
from PyQt5.QtCore import QByteArray, QDate, Qt
from PyQt5 import QtCore
from PyQt5.uic import loadUi
from banco.criar_banco import Banco
from banco.comandos import Query


# class Login():
#     def __init__(self):
#         super().__init__()
#         self.tela_login = uic.loadUi('./interface/tela_login.ui')
#         self.tela_login.btn_login.clicked.connect(self.login)
#         self.tela_login.txt_senha.returnPressed.connect(self.login)

#     def login(self):
#         usuario = self.tela_login.txt_usuario.text()
#         senha = self.tela_login.txt_senha.text()

#         if usuario == 'admin' and senha == 'admin':
#             self.estoque = Estoque()
#             self.estoque.show()
#             self.tela_login.close()

#         else:
#             QMessageBox.warning(self, 'Error', 'Usuário ou Senha inválidos')


class Estoque(QMainWindow):
    def __init__(self, perfil):
        super(Estoque, self).__init__()
        loadUi('./interface/tela_principal.ui', self)
        Banco('./banco/estoque.db')
        self.comandos_db = Query('./banco/estoque.db')
        self.setWindowTitle("Gerenciamento do estoque")
        self.setWindowIcon(QIcon("./interface/icone.ico"))


        if perfil == 'usuario':
            # self.btn_cadastrar_usuario.setVisible(False)
            self.listWidget.item(4).setHidden(True)

        self.carregar_tabela()

        self.livros_mais_vendidos()
        self.livros_em_menor_quantidade()


        # Ações de botões
        ###self.tableWidget.itemClicked.connect(self.carrega_campos)
        self.btn_editar_livro.clicked.connect(self.editar_livros)
        self.btn_adicionar_livro.clicked.connect(self.cadastrar_livro)
        self.cb_editar_livros.activated.connect(self.preencher_lineEdits)
        self.cb_registrar_venda.activated.connect(self.preencher_lineEdits_2)
        self.spinBox.valueChanged.connect(self.calcular_valor)
        self.btn_excluir.clicked.connect(self.excluir_livros)
        self.btn_cadastrar_user.clicked.connect(self.cadastrar_usuario)
        self.cb_editar_livros.mouseReleaseEvent = self.preencher_comboBox
        self.cb_registrar_venda.mouseReleaseEvent = self.preencher_comboBox_2
        self.btn_reg_venda.clicked.connect(self.registrar_venda)
        self.btn_mais_livros.clicked.connect(self.preenche_tabela)
        self.btn_mais_livros.clicked.connect(self.calcular_totais)
        self.btn_remover_livro.clicked.connect(self.excluir_livros_2)
        self.btn_remover_livro.clicked.connect(self.calcular_totais)
        self.btn_excluir_usuario.clicked.connect(self.excluir_usuario)
        self.label_capa.mouseReleaseEvent = self.abre_diretorio_edicao
        self.capa_do_livro.mouseReleaseEvent = self.abre_diretorio_cadastro
        
        # # Navegação de páginas
        # Conecta o sinal itemSelectionChanged ao slot item_selected
        self.listWidget.itemSelectionChanged.connect(self.selecao_menu_lateral)
        
        # Máscaras de LineEdit
        self.t_quantidade.setInputMask('9999')

        self.btn_toggle.clicked.connect(self.leftMenu)

    def selecao_menu_lateral(self):
        selected_items = self.listWidget.selectedItems()
        for item in selected_items:
            if item.text() == "Ver estoque":
                self.stackedWidget.setCurrentWidget(self.tab_livros)
                self.carregar_tabela()
                self.livros_mais_vendidos()
                self.livros_em_menor_quantidade()
            if item.text() == "Editar livros":
                self.stackedWidget.setCurrentWidget(self.tab_editar_livros)
            if item.text() == "Cadastrar livros":
                self.stackedWidget.setCurrentWidget(self.tab_cadastrar_livros)
                self.preencher_listWidget_2()
            if item.text() == "Registrar venda":
                self.stackedWidget.setCurrentWidget(self.tab_registrar_venda)
                self.preencher_data()
            if item.text() == "Gerenciar usuários":
                self.stackedWidget.setCurrentWidget(self.tab_cadastrar_usuario)
                self.preenche_tabela_2()

    def leftMenu(self):
        width = self.left_menu.width()

        if width == 70:
            newWidth = 200
        else:
            newWidth = 70

        self.animation =   QtCore.QPropertyAnimation(
            self.left_menu, b"maximumWidth")
        self.animation.setDuration(500)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

###--------tab_livros(inicial)------------
    def livros_mais_vendidos(self):
        layout = QVBoxLayout(self.widget)
        chart_view = QChartView(self.widget)
        chart = QChart()
        chart.setTitle("Livros mais vendidos")
        chart.setTheme(QChart.ChartThemeLight)
        chart.setAnimationOptions(QChart.AllAnimations)
        chart_view.setRenderHint(QPainter.Antialiasing)
        chart.createDefaultAxes()

        series = QPieSeries()
        series.setHoleSize(0.30)
        valores = Query.livros_mais_vendidos(self.comandos_db)
        index = 0
        for rotulo, valor in valores:
            if index == 0 or index == 1:
                slice = series.append(f'({valor}) '+rotulo, float(valor))
                slice.setExploded(True)
                slice.setLabelVisible(True)
                index +=1
                continue
            series.append(f'({valor}) '+rotulo, float(valor))
        
        chart.legend().setAlignment(Qt.AlignRight)
        chart.addSeries(series)

        chart_view.setChart(chart)
        layout.addWidget(chart_view)
        # pal = chart_view.window().palette()
        # pal.setColor(QPalette.Window, QColor(0xcee7f0))
        # pal.setColor(QPalette.WindowText, QColor(0x404044))


    def livros_em_menor_quantidade(self):
        layout = QVBoxLayout(self.widget_2)
        chart_view = QChartView(self.widget_2)
        chart = QChart()
        chart.setTitle("Livros em menor quantidade no estoque")
        chart.setTheme(QChart.ChartThemeLight)
        chart.setAnimationOptions(QChart.AllAnimations)
        chart_view.setRenderHint(QPainter.Antialiasing)
        chart.legend().setAlignment(Qt.AlignLeft)
        chart.createDefaultAxes()

        series = QPieSeries()
        #series.setHoleSize(0.40)
        valores = Query.livros_em_menor_quantidade(self.comandos_db)
        index = 0
        for rotulo, valor in valores:
            if index == 0 or index == 1:
                slice = series.append(f'({valor}) '+rotulo, float(valor))
                slice.setExploded(True)
                #slice.setLabelVisible(True)
                index +=1
                continue
            series.append(f'({valor}) '+rotulo, float(valor))
            
        
        chart.addSeries(series)
        
        chart_view.setChart(chart)
        layout.addWidget(chart_view)

    def definir_cabecalho(self):
        self.cur.execute(f"PRAGMA table_info(livros)")
        retorno = self.cur.fetchall()
        colunas = [r[1] for r in retorno]
        self.tableWidget.setColumnCount(len(colunas))
        self.tableWidget.setHorizontalHeaderLabels(colunas)

    def carregar_tabela(self):
        self.conn = sqlite3.connect('./banco/estoque.db')
        self.cur = self.conn.cursor()

        self.tableWidget.setRowCount(0)
        self.definir_cabecalho()
        self.cur.execute(f'SELECT id, titulo, autor, editora, isbn, ano_publicacao, preco, quantidade FROM livros')
        for row_data in self.cur.fetchall():
            row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)
            for column, data in enumerate(row_data):
                self.tableWidget.setItem(
                    row, column,  QTableWidgetItem(str(data)))
        self.tableWidget.resizeColumnsToContents()
    
    def excluir_livros(self):
        linha = self.tableWidget.currentRow()
        if linha == -1:
            QMessageBox.warning(
                self, 'Erro', 'Selecione um item para excluir!')
            return
        id = self.tableWidget.item(linha, 0).text()
        Query.excluir_livros(self.comandos_db, 'livros', id)
        self.carregar_tabela()
        self.livros_mais_vendidos()
        self.livros_em_menor_quantidade()

    # def carrega_campos(self):
    #     linha = self.tableWidget.currentRow()
    #     id = self.tableWidget.item(linha, 0).text()
    #     self.cur.execute(f'SELECT * FROM livros WHERE id=?', (id))
    #     dados = self.cur.fetchone()
    #     self.txt_titulo.setText(dados[1])
    #     self.txt_autor.setText(dados[2])
    #     self.txt_editora.setText(dados[3])
    #     self.txt_isbn.setText(str(dados[4]))
    #     self.txt_ano.setText(str(dados[5]))
    #     self.txt_preco.setText(str(dados[6]))
    #     self.txt_quantidade.setText(str(dados[7]))

    def limpa_campos(self):
        self.txt_titulo.clear()
        self.txt_autor.clear()
        self.txt_editora.clear()
        self.txt_isbn.clear()
        self.txt_ano.clear()
        self.txt_preco.clear()
        self.txt_quantidade.clear()

    
#####################################################
###--------------tab_editar_livros-------------

    def preencher_comboBox(self, event):
        self.cb_editar_livros.clear()
        self.cb_editar_livros.addItem(str(' '[0]))
        self.cur.execute("SELECT titulo FROM livros")
        titulos = str(self.cur.fetchall())
        titulos = re.findall(r"'(.*?)'", titulos)
        self.cb_editar_livros.addItems(titulos)

    def preencher_listWidget(self, titulo):
        # Preencher listWidget
        self.cur.execute('SELECT nome FROM categorias')
        items = str(self.cur.fetchall())
        items = re.findall(r"'(.*?)'", items)
        self.lw_editar_livros.addItems(items)
        # Marcar itens
        livro_id = Query.buscar_id_livro(self.comandos_db, titulo)
        dados = Query.buscar_nome_categoria_livro(self.comandos_db, livro_id)
        categorias = str(dados)
        categorias = re.findall(r"'(.*?)'", categorias)       
        for index in range(len(items)):
            item = self.lw_editar_livros.item(index)
            if item.text() in categorias:
                item.setSelected(True)
                item.setTextAlignment(Qt.AlignHCenter)      

    def preencher_lineEdits(self):
        titulo = self.cb_editar_livros.currentText()
        self.imagem = QPixmap()
        if titulo == ' ':
            self.label_capa.clear()
            self.t_titulo.clear()
            self.t_autor.clear()
            self.t_editora.clear()
            self.t_isbn.clear()
            self.t_ano.clear()
            self.t_preco.clear()
            self.t_quantidade.clear()
            self.lw_editar_livros.clear()
        else:
            dados = Query.buscar_dados_livro(self.comandos_db, titulo)
            self.t_titulo.setText(dados[0])
            self.t_autor.setText(dados[1])
            self.t_editora.setText(str(dados[2]))# adicionar verificação de string para editora
            self.t_isbn.setText(str(dados[3]))
            self.t_ano.setText(str(dados[4]))
            self.t_preco.setText(str(dados[5]))
            self.t_quantidade.setText(str(dados[6]))
            qbyte_array = QByteArray.fromBase64(dados[7])
            self.imagem.loadFromData(qbyte_array)
            self.label_capa.setPixmap(self.imagem)
            self.lw_editar_livros.clear()
            self.preencher_listWidget(titulo)

    def abre_diretorio_edicao(self, event):
        try:
            local = QFileDialog.getOpenFileName()[0]
            self.label_capa.setPixmap(QPixmap(local))
            self.local_imagem = local
        except TypeError:
            pass
    
    def verifica_lineEdits(self):
        titulo = self.t_titulo.text()
        autor = self.t_autor.text()
        editora = self.t_editora.text()
        isbn = self.t_isbn.text()
        ano = self.t_ano.text()
        preco = self.t_preco.text()
        quantidade = self.t_quantidade.text()
    
        self.titulo = titulo.casefold()
        self.autor = autor.casefold()
        self.editora = editora.casefold()
        self.isbn = int(isbn)
        self.ano = int(ano)
        self.preco = float(preco)
        self.quantidade = int(quantidade)

        selected_items = self.lw_editar_livros.selectedItems()
        self.lista_categorias = []
        for item in selected_items:
            self.lista_categorias.append(item.text())

    def editar_livros(self):
        titulo = self.cb_editar_livros.currentText()
        if titulo == ' ':
            QMessageBox.warning(self, 'Erro', 'Selecione um item para editar!')
            return
        #id = self.tableWidget.item(linha, 0).text()
        livro_id = Query.buscar_id_livro(self.comandos_db, titulo)
        self.verifica_lineEdits()
        try:
            capa = self.imagem_para_binario(self.local_imagem)
            Query.editar_livros(self.comandos_db, self.titulo, self.autor, self.editora,
                                self.isbn, self.ano, self.preco, self.quantidade, capa, livro_id,
                                self.lista_categorias)
        except:
            Query.editar_livros_2(self.comandos_db, self.titulo, self.autor, self.editora,
                            self.isbn, self.ano, self.preco, self.quantidade, livro_id,
                            self.lista_categorias)
        QMessageBox.warning(self, 'Sucesso', 'Livro editado com sucesso!')
        self.carregar_tabela()

##################################################
###-----------tab_cadastrar_livros-------------------

    def preencher_listWidget_2(self):
        self.lw_categorias.clear()
        self.cur.execute('SELECT nome FROM categorias')
        categorias = str(self.cur.fetchall())
        categorias = re.findall(r"'(.*?)'", categorias)    
        self.lw_categorias.addItems(categorias)
        for index in range(self.lw_categorias.count()):
            item = self.lw_categorias.item(index)
            item.setTextAlignment(Qt.AlignHCenter)

    def verifica_preenchimento(self):
        self.titulo = self.txt_titulo.text()
        self.autor = self.txt_autor.text()
        self.editora = self.txt_editora.text()
        self.isbn = self.txt_isbn.text()
        self.ano = self.txt_ano.text()
        self.preco = self.txt_preco.text()
        self.quantidade = self.txt_quantidade.text()
        selected_items = self.lw_categorias.selectedItems()
        self.lista_categorias = []
        for item in selected_items:
            self.lista_categorias.append(item.text())
        if self.titulo == '' or self.autor == '' or self.preco == '' or self.quantidade == '':
            QMessageBox.warning(
                self, 'Erro', 'Título, autor, preço e quantidade são campos obrigatórios!')
            return 'erro'
        try:
            if self.isbn != '':
                self.isbn = int(self.isbn)
            self.ano = int(self.ano)
            self.preco = float(self.preco)
            self.quantidade = int(self.quantidade)
        except ValueError:
            QMessageBox.warning(
                self, 'Erro', 'ISBN, ano, preço e quantidade devem ser números!')
            return 'erro'
        self.titulo = self.titulo.casefold()
        self.autor = self.autor.casefold()
        self.editora = self.editora.casefold()
    
    def abre_diretorio_cadastro(self, event):
        try:
            local = QFileDialog.getOpenFileName()[0]
            self.capa_do_livro.setPixmap(QPixmap(local))
            self.local_imagem = local
        except Exception as erro:
            print(erro)
            pass
        #return caminho

    def cadastrar_livro(self):
        if self.verifica_preenchimento() != 'erro':
            capa = self.imagem_para_binario(self.local_imagem)
            Query.cadastrar_novo_livro(self.comandos_db, self.titulo, self.autor, self.editora, self.isbn, self.ano, self.preco, self.quantidade, capa, self.lista_categorias)
            self.carregar_tabela()
            QMessageBox.warning(self, 'Sucesso', 'Livro cadastrado!')
            self.lw_categorias.clearSelection()


###################################
#-------tab_registrar_venda---------    

    def preencher_data(self):
        data_atual = datetime.now()
        d = int(data_atual.strftime("%d"))
        m = int(data_atual.strftime("%m"))
        y = int(data_atual.strftime("%Y"))
        data = QDate(y, m, d)
        self.dateEdit.setDate(data)

    def preencher_comboBox_2(self, event):
        self.cb_registrar_venda.clear()
        self.cb_registrar_venda.addItem(str(' '[0]))
        self.cur.execute("SELECT titulo FROM livros")
        titulos = str(self.cur.fetchall())
        titulos = re.findall(r"'(.*?)'", titulos)
        self.cb_registrar_venda.addItems(titulos)

    def preencher_lineEdits_2(self):
        titulo = self.cb_registrar_venda.currentText()
        imagem = QPixmap()
        if titulo == ' ':
            self.label_capa_2.clear()
            self.label_id_livro.clear()
            self.t_titulo_2.clear()
            self.label_qtd_estoque.clear()
            self.spinBox.setValue(1)
            self.label_preco.clear()
            self.label_valor.clear()
        else:
            livro_id = Query.buscar_id_livro(self.comandos_db, titulo)
            dados = Query.buscar_dados_livro(self.comandos_db, titulo)
            self.label_id_livro.setText(livro_id)
            self.t_titulo_2.setText(dados[0])
            self.label_preco.setText(str(dados[5]))
            self.label_qtd_estoque.setText(str(dados[6]))
            self.spinBox.setMaximum(dados[6])
            self.spinBox.setValue(1)
            self.label_valor.setText(str(self.calcular_valor()))
            
            qbyte_array = QByteArray.fromBase64(dados[7])
            imagem.loadFromData(qbyte_array)
            self.label_capa_2.setPixmap(imagem)

    def calcular_valor(self):
        preco = self.label_preco.text()
        preco = float(preco)
        quantidade = self.spinBox.value()
        valor = preco * quantidade
        self.label_valor.setText(str(valor))
        return valor

    #    #    #    #    #    #    #    #    #    #  
    def calcular_totais(self):
        linhas = self.tableWidget_2.rowCount()
        # Calcula valor total
        valor_total = 0
        for linha in range(linhas):
            item = self.tableWidget_2.item(linha, 2)
            valor = float(item.text())
            valor_total += valor
        self.label_valor_total.setText(str(valor_total))
        # Calcula quantidade total
        qtd_total = 0
        for linha in range(linhas):
            item = self.tableWidget_2.item(linha, 0)
            qtd = int(item.text())
            qtd_total += qtd
        self.label_qtd_total.setText(str(qtd_total))

    def preenche_tabela(self):
        #self.tableWidget_2.setRowCount(0)
        #lala = [2, '25/05/2023', 40.0, 1]
        quantidade = self.spinBox.value()
        data_venda = self.dateEdit.text()
        valor = float(self.label_valor.text())
        livro_id = self.label_id_livro.text()
        dados = [[quantidade, data_venda, valor, livro_id]]
        # Inserindo valores na tabela
        for row_data in dados:
            row = self.tableWidget_2.rowCount()
            self.tableWidget_2.insertRow(row)
            for column, data in enumerate(row_data):
                self.tableWidget_2.setItem(
                    row, column,  QTableWidgetItem(str(data)))
        # Ajustando estoque disponível
        label_estoque = int(self.label_qtd_estoque.text())
        label_estoque -= quantidade
        self.label_qtd_estoque.setText(str(label_estoque))
        self.spinBox.setMaximum(label_estoque)
        # self.tableWidget_2.resizeColumnsToContents()
        # linha = self.tableWidget_2.currentRow()
        # data = self.tableWidget_2.item(linha, 0).text() 
       
    def pegar_valores(self):
        # Pegando todos os valores da tabela
        linhas = self.tableWidget_2.rowCount()
        colunas = self.tableWidget_2.columnCount()
        conteudo_tabela = []
        for linha in range(linhas):
            # Pegando valores da 1ª linha (0)
            conteudo_linha = []
            for col in range(colunas):
                item = self.tableWidget_2.item(linha, col)
                value = item.text()
                conteudo_linha.append(value)
            conteudo_tabela.append(conteudo_linha)
        # print(conteudo_linha)
        # print(conteudo_tabela)
        return conteudo_tabela

    def excluir_livros_2(self):
        linha = self.tableWidget_2.currentRow()
        if linha == -1:
            QMessageBox.warning(
                self, 'Erro', 'Selecione um item para excluir!')
            return
        # Calcula estoque disponível
        livro_id = self.tableWidget_2.item(linha, 3).text()
        if livro_id == self.label_id_livro.text():
            qtd_label = int(self.label_qtd_estoque.text())
            qtd_tabela = int(self.tableWidget_2.item(linha, 0).text())
            estoque = qtd_label + qtd_tabela
            self.label_qtd_estoque.setText(str(estoque))
            self.spinBox.setMaximum(estoque)
        # Apaga linha da tabela
        self.tableWidget_2.removeRow(linha)
        


    #    #    #    #    #    #    #    #    #    #    
    def registrar_venda(self):
        valor_total = self.label_valor_total.text()
        data_venda = self.dateEdit.text()
        qtd_total = int(self.label_qtd_total.text())
        venda_id = Query.registrar_venda(self.comandos_db, qtd_total, data_venda, valor_total)
        
        lista = self.pegar_valores()
        print(lista)
        qtd_vendas_por_livro = len(lista)
        for venda in range(qtd_vendas_por_livro):
            quantidade = int(lista[venda][0])
            data_venda = lista[venda][1]
            valor = float(lista[venda][2])
            livro_id = int(lista[venda][3])
            Query.registrar_venda_2(self.comandos_db, quantidade, livro_id, venda_id)

        QMessageBox.warning(self, 'Sucesso', 'Venda registrada com sucesso!')


#############################
###--------tab_cadastrar_usuario-----------------

    def preenche_tabela_2(self):
        self.conn = sqlite3.connect('./banco/estoque.db')
        self.cur = self.conn.cursor()

        self.tb_usuarios.setRowCount(0)
        self.cur.execute(f'SELECT * FROM usuarios')
        for row_data in self.cur.fetchall():
            row = self.tb_usuarios.rowCount()
            self.tb_usuarios.insertRow(row)
            for column, data in enumerate(row_data):
                self.tb_usuarios.setItem(
                    row, column,  QTableWidgetItem(str(data)))
    def excluir_usuario(self):
        linha = self.tb_usuarios.currentRow()
        if linha == -1:
            QMessageBox.warning(
                self, 'Erro', 'Selecione um item para excluir!')
            return
        # Calcula estoque disponível
        usuario_id = self.tb_usuarios.item(linha, 0).text()
        print(type(usuario_id), usuario_id)
        Query.excluir_usuario(self.comandos_db, usuario_id)
        # Apaga linha da tabela
        self.tb_usuarios.removeRow(linha)
        

    def cadastrar_usuario(self):
        if self.txt_senha.text() != self.txt_senha_2.text():
            QMessageBox.warning(
                self, 'Erro', 'A senha não é igual!')
            return
        nome = self.txt_nome.text()
        user = self.txt_user.text()
        senha = self.txt_senha.text()
        perfil = self.cb_perfil_usuario.currentText()
        Query.cadastrar_usuario(self.comandos_db, nome, user, senha, perfil)
        QMessageBox.warning(self, 'Sucesso', 'Usuário cadastrado com sucesso!')
        nome = self.txt_nome.clear()
        user = self.txt_user.clear()
        senha = self.txt_senha.clear()
        senha = self.txt_senha_2.clear()

    def imagem_para_binario(self, local_imagem):
        with open(local_imagem, 'rb') as file:
            imagem = file.read()
            imagem_binaria = base64.b64encode(imagem)
        return imagem_binaria #daqui devolve pra inserir no banco
    


    def closeEvent(self, event):
        self.comandos_db.conn.close()




'''

Neste código, integramos um banco de dados SQLite ao nosso sistema de estoque. Também adicionamos validação de entrada de dados nos campos de nome, quantidade e preço, garantindo que eles não estejam vazios e que quantidade e preço sejam números.

Na função `carrega_dados`, carregamos os dados do banco de dados e os exibimos na tabela. Na função `adicionar_item`, inserimos um novo item no banco de dados e atualizamos a tabela. Na função `editar_item`, atualizamos um item existente no banco de dados e atualizamos a tabela. Na função `excluir_item`, excluímos um item do banco de dados e atualizamos a tabela. Na função `carrega_campos`, carregamos os dados de um item selecionado na tabela nos campos de edição.

Na função `limpa_campos`, limpamos os campos de edição após adicionar ou editar um item. Na função `closeEvent`, fechamos a conexão com o banco de dados quando a janela é fechada.

Este código é apenas um exemplo e pode ser adaptado e melhorado para atender às necessidades específicas de um sistema de estoque real.

'''
