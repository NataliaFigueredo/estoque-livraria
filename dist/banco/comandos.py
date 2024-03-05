import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem, QTableWidget
from PyQt5.uic import loadUi
import re


class Query:
    def __init__(self, banco):
        self.conn = sqlite3.connect(banco)
        self.cur = self.conn.cursor()
        self.tela = loadUi('./interface/tela_principal.ui')

    # def carregar_dados(self, tabela):
    #     self.cur.execute(f'SELECT * FROM {tabela}')

    # def carregar_livros_estoque(self):
    #     self.cur.execute(
    #         'SELECT estoque.livro_id, livros.titulo, estoque.quantidade AS estoque_quantidade, livros.quantidade AS livros_quantidade FROM estoque JOIN livros ON estoque.livro_id = livros.id')


    def livros_mais_vendidos(self):
        self.cur.execute('''
            SELECT livros.titulo, COUNT(livros_vendas.venda_id) AS quantidade
                FROM livros
                INNER JOIN livros_vendas ON livros.id = livros_vendas.livro_id
                GROUP BY livros.id
                ORDER BY quantidade DESC
        ''')
        self.conn.commit()
        return self.cur.fetchall()
    
    def livros_em_menor_quantidade(self):
        self.cur.execute('''
            SELECT titulo, quantidade
                FROM livros
                ORDER BY quantidade ASC
        ''')
        self.conn.commit()
        return self.cur.fetchall()

    def cadastrar_novo_livro(self, titulo, autor, editor, isbn, ano, preco, quantidade, capa, lista_categorias):
        self.cur.execute(
            f'INSERT OR IGNORE INTO livros(titulo, autor, editora, isbn, ano_publicacao, preco, quantidade, capa) VALUES(?, ?, ?, ?, ?, ?, ?, ?)', (titulo, autor, editor, isbn, ano, preco, quantidade, capa))
        livro_id = self.cur.lastrowid
        #self.conn.commit()
        for categoria in lista_categorias:
            categoria_id = self.buscar_id_categoria(categoria)
            self.cur.execute(f'INSERT INTO livros_categorias(livro_id, categoria_id) VALUES(?,?)', (livro_id, categoria_id))
        self.conn.commit()

    # def cadastra_estoque(self, livro_id, quantidade):
    #     self.cur.execute(
    #         'INSERT OR IGNORE INTO estoque(livro_id, quantidade) VALUES(?,?)', (livro_id, quantidade))
    #     self.conn.commit()

    # def atualizar_estoque(self, quantidade, id):
    #     self.cur.execute(
    #         'UPDATE estoque SET quantidade=? WHERE livros.titulo=?', (quantidade, id))

    # def buscar_capa_livro(self, id):
    #     self.cur.execute(
    #         f'SELECT capa FROM livros WHERE id=?', (id,))
    #     self.conn.commit()
    #     capa = self.cur.fetchone()[0]
    #     return capa

    def buscar_id_livro(self, titulo):
        self.cur.execute(f'SELECT id FROM livros WHERE titulo=?', (titulo,))
        self.conn.commit()
        id = str(self.cur.fetchall())
        id = re.sub(r"[^0-9]", "", id)
        return id

    def buscar_dados_livro(self, titulo):
        id = self.buscar_id_livro(titulo)
        self.cur.execute(
            f'SELECT titulo, autor, editora, isbn, ano_publicacao, preco, quantidade, capa FROM livros WHERE id=?', (id,))
        self.conn.commit()
        return self.cur.fetchone()

    def editar_livros(self, titulo, autor, editora, isbn, ano, preco, quantidade, capa, livro_id, lista_categorias):
        self.cur.execute(
            f'UPDATE livros SET titulo=?, autor=?, editora=?, isbn=?, ano_publicacao=?, preco=?, quantidade=?, capa=? WHERE id=?', (titulo, autor, editora, isbn, ano, preco, quantidade, capa, livro_id))
        self.cur.execute(f'DELETE FROM livros_categorias WHERE livro_id=?', (livro_id,))
        for categoria in lista_categorias:
            categoria_id = self.buscar_id_categoria(categoria)
            self.cur.execute(f'INSERT INTO livros_categorias(livro_id, categoria_id) VALUES(?,?)', (livro_id, categoria_id))
        self.conn.commit()
    
    def editar_livros_2(self, titulo, autor, editora, isbn, ano, preco, quantidade, livro_id, lista_categorias):
        self.cur.execute(
            f'UPDATE livros SET titulo=?, autor=?, editora=?, isbn=?, ano_publicacao=?, preco=?, quantidade=? WHERE id=?', (titulo, autor, editora, isbn, ano, preco, quantidade, livro_id))
        self.cur.execute(f'DELETE FROM livros_categorias WHERE livro_id=?', (livro_id,))
        for categoria in lista_categorias:
            categoria_id = self.buscar_id_categoria(categoria)
            self.cur.execute(f'INSERT INTO livros_categorias(livro_id, categoria_id) VALUES(?,?)', (livro_id, categoria_id))
        self.conn.commit()

    def registrar_venda(self, qtd_total, data_venda, valor_total):
        self.cur.execute(
            'INSERT INTO vendas(quantidade, data_venda, valor) VALUES(?,?,?)', (qtd_total, data_venda, valor_total))
        venda_id = self.cur.lastrowid
        self.conn.commit()
        return venda_id
    
    def registrar_venda_2(self, quantidade, livro_id, venda_id):
        self.cur.execute('UPDATE livros SET quantidade = quantidade - ? WHERE id=?', (quantidade, livro_id))
        
        self.cur.execute('INSERT INTO livros_vendas (livro_id, venda_id, quantidade) VALUES (?, ?, ?)', (livro_id, venda_id, quantidade))

        self.conn.commit()

    def buscar_id_categoria(self, categoria):
        self.cur.execute(f'SELECT id FROM categorias WHERE nome=?', (categoria,))
        self.conn.commit()
        id_categoria = self.cur.fetchone()[0]
        return id_categoria

    def buscar_nome_categoria_livro(self, livro_id):
        self.cur.execute('''
            SELECT categorias.nome
                FROM categorias
                INNER JOIN livros_categorias ON categorias.id = livros_categorias.categoria_id
                WHERE livros_categorias.livro_id = ?
        ''', (livro_id,))
        self.conn.commit()
        categorias = self.cur.fetchall()
        return categorias


    def excluir_livros(self, tabela, id):
        self.cur.execute(f'DELETE FROM {tabela} WHERE id=?', (id,))
        self.conn.commit()

    def cadastrar_usuario(self, nome, user, senha, perfil):
        self.cur.execute(
            'INSERT INTO usuarios(nome, user, senha, perfil) VALUES(?,?,?,?)', (nome, user, senha, perfil))
        self.conn.commit()

    def validar_usuario(self, user, senha):
        self.cur.execute('SELECT * FROM usuarios')
        for linha in self.cur.fetchall():
            if linha[2].casefold() == user.casefold() and linha[3] == senha and linha[4] == 'Administrador':
                return 'administrador'
            elif linha[2].casefold() == user.casefold() and linha[3] == senha and linha[4] == 'Usuário':
                return 'usuario'
            else:
                continue
        return 'sem acesso'
    
    def excluir_usuario(self, id):
        self.cur.execute('DELETE FROM usuarios WHERE id=?', (id,))
        self.conn.commit()
