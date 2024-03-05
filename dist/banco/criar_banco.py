import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5 import uic
from PyQt5.uic import loadUi


class Banco:
    def __init__(self, banco):
        loadUi('./interface/estoque.ui')
        self.conn = sqlite3.connect(banco)
        self.cur = self.conn.cursor()
        self.criar_db()

    def criar_db(self):

        #self.cur.execute('DROP TABLE IF EXISTS usuarios')
        # self.cur.execute('DROP TABLE IF EXISTS livros')
        # self.cur.execute('DROP TABLE IF EXISTS categorias')
        # self.cur.execute('DROP TABLE IF EXISTS vendas')
        # self.cur.execute('DROP TABLE IF EXISTS compras')
        # self.cur.execute('DROP TABLE IF EXISTS livros_vendas')

        # Tabela usuarios
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                user TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                perfil TEXT NOT NULL
                )
        ''')

        # Tabela livros
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS livros (
                id INTEGER PRIMARY KEY,
                titulo TEXT NOT NULL,
                autor TEXT NOT NULL,
                editora TEXT,
                isbn INTEGER,
                ano_publicacao INTEGER,
                preco REAL NOT NULL,
                quantidade INTEGER NOT NULL,
                capa BLOB
                )
        ''')

        # Tabela categorias
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY,
                nome TEXT NOT NULL
                )
        ''')
        # Verificando se a tabela está vazia
        self.cur.execute('SELECT COUNT(*) FROM categorias')
        result = self.cur.fetchone()[0]
        if result == 0:
            # Informações a serem adicionadas às linhas
            informacoes = [
                'autoajuda',
                'biografia',
                'clássicos',
                'ciência',
                'comics',
                'culinária',
                'esportes',
                'espiritualidade',
                'fantasia',
                'ficção',
                'ficção científica',
                'ficção história',
                'filosofia',
                'histórico',
                'humor e comédia',
                'joven adulto',
                'lgbt',
                'literatura infantil',
                'manga',
                'mistério',
                'música',
                'não ficção',
                'negócios',
                'paranormal',
                'poesia',
                'psicologia',
                'religião',
                'romance',
                'suspense',
                'terror',
                'viagens'
            ]
            # Adicionando as informações às linhas da tabela
            for info in informacoes:
                self.cur.execute('INSERT INTO categorias (nome) VALUES (?)', (info,))
        ### Tabela livros_categorias
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS livros_categorias (
                livro_id INTEGER,
                categoria_id INTEGER,
                FOREIGN KEY (livro_id) REFERENCES livros(id),
                FOREIGN KEY (categoria_id) REFERENCES categorias(id)
                )
        ''')

        # # Tabela estoque
        # self.cur.execute('''
        #     CREATE TABLE IF NOT EXISTS estoque (
        #         livro_id INTEGER PRIMARY KEY,
        #         quantidade INTEGER NOT NULL,
        #         FOREIGN KEY (livro_id) REFERENCES livros (id)
        #         )
        # ''')

        # self.cur.execute('DROP TRIGGER IF EXISTS atualiza_estoque')
        # # Trigger para atualizar estoque sempre que livros for atualizada.
        # self.cur.execute('''
        #     CREATE TRIGGER IF NOT EXISTS atualiza_estoque
        #         AFTER UPDATE ON livros
        #         FOR EACH ROW
        #         BEGIN
        #             UPDATE estoque
        #             SET quantidade = NEW.quantidade
        #             WHERE livro_id = NEW.id;
        #         END
        # ''')

        # Tabela Vendas
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS vendas (
                id INTEGER PRIMARY KEY,
                quantidade INTEGER NOT NULL,
                data_venda TEXT NOT NULL,
                valor REAL
                )
        ''')

        ### Tabela livros_vendas
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS livros_vendas (
                livro_id INTEGER,
                venda_id INTEGER,
                quantidade INTEGER,
                FOREIGN KEY (livro_id) REFERENCES livros(id),
                FOREIGN KEY (venda_id) REFERENCES vendas(id)
                )
        ''')

        # # Cria tabela "compras"
        # self.cur.execute('''
        #     CREATE TABLE IF NOT EXISTS compras (
        #         id INTEGER PRIMARY KEY,
        #         data_compra TEXT NOT NULL,
        #         livro_id INTEGER NOT NULL,
        #         quantidade INTEGER NOT NULL,
        #         FOREIGN KEY (livro_id) REFERENCES livros(id)
        #     )
        # ''')

        # quantas vendas ocorreram em um determinado livro
        # SELECT SUM(quantidade) FROM vendas WHERE livro_id = 1;

        # consulta que retornaria o número total de livros em estoque:
        # SELECT SUM(quantidade) FROM estoque;

        # quantos livros em estoque de um determinado título, autor ou categoria
        # SELECT SUM(quantidade) FROM estoque WHERE titulo = 'O Senhor dos Anéis';

        # def realizar_venda(livro_id, quantidade):
        #     with sqlite3.connect("banco.db") as conn:
        #         cursor = conn.cursor()
        #         # Subtrai a quantidade vendida do estoque atual do livro
        #         cursor.execute("UPDATE livros SET quantidade = quantidade - ? WHERE livro_id = ?", (quantidade, livro_id))
        #         # Insere um registro na tabela vendas
        #         cursor.execute("INSERT INTO vendas (livro_id, quantidade) VALUES (?, ?)", (livro_id, quantidade))
        #         # Salva as alterações no banco de dados
        #         conn.commit()
        #         conn.close

        # # inserindo a nova compra
        # cursor.execute("INSERT INTO compras (livro_id, quantidade, data) VALUES (?, ?, ?)", (1, 10, '2023-05-05'))

        # # atualizando a tabela livros com a nova quantidade em estoque
        # cursor.execute("UPDATE livros SET quantidade = quantidade + ? WHERE id = ?", (10, 1))

        # # confirmando a transação
        # conn.commit()

        # # fechando a conexão com o banco de dados
        # conn.close()

        self.conn.commit()
        self.cur.close()
        self.conn.close()

    # def carrega_dados(self, banco):
    #     self.conn = sqlite3.connect(banco)
    #     self.cur = self.conn.cursor()

    #     self.tableWidget.setRowCount(0)
    #     #self.statTable.setFixedWidth(self.statTable.columnWidth(0) + self.statTable.columnWidth(1))
    #     inf = self.cur.execute('PRAGMA table_info(estoque)')
    #     print(inf)
    #     self.cur.execute('SELECT * FROM estoque')
    #     for row_data in self.cur.fetchall():
    #         row = self.tableWidget.rowCount()
    #         self.tableWidget.insertRow(row)
    #         for column, data in enumerate(row_data):
    #             self.tableWidget.setItem(
    #                 row, column,  QTableWidgetItem(str(data)))
    #     self.tableWidget.resizeColumnToContents()

    #     self.cur.close()
    #     self.conn.close()
