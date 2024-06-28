# app/database.py
import os
import sqlite3

db_file = 'C:\\mercado_livre.db'

# Verificar se o arquivo do banco de dados existe
if not os.path.exists(db_file):
    print(f'O arquivo {db_file} não existe na pasta especificada.')

# Tentar conectar ao banco de dados
try:
    conn = sqlite3.connect(db_file)
    print(f'Successfully connected to {db_file}')
except sqlite3.Error as e:
    print(f'Error connecting to database: {e}')

# Função para criar a tabela de produtos se não existir
def criar_tabela():
    caminho_banco_dados = 'C:\\mercado_livre.db'
    conn = sqlite3.connect(caminho_banco_dados)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco TEXT NOT NULL,
            link TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Função para salvar produtos no banco de dados
def salvar_produtos(produtos):
    caminho_banco_dados = 'C:\\mercado_livre.db'
    conn = sqlite3.connect(caminho_banco_dados)
    cursor = conn.cursor()
    for produto in produtos:
        cursor.execute('''
            INSERT INTO produtos (nome, preco, link) VALUES (?, ?, ?)
        ''', (produto['nome'], produto['preco'], produto['link']))
    conn.commit()
    conn.close()

# Função para listar todos os produtos salvos no banco de dados
def listar_produtos():
    caminho_banco_dados = 'C:\\mercado_livre.db'
    conn = sqlite3.connect(caminho_banco_dados)
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome, preco, link FROM produtos')
    produtos = cursor.fetchall()
    conn.close()
    return produtos

# Função para excluir um produto pelo seu ID
def remover_produto(id_produto):
    caminho_banco_dados = 'C:\\mercado_livre.db'
    conn = sqlite3.connect(caminho_banco_dados)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM produtos WHERE id = ?', (id_produto,))
    conn.commit()
    conn.close()
