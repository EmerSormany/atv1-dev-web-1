import sqlite3 as sqlite

def criarTabela():
    conn = sqlite.connect('gestaoDB.sqlite')
    cursor = conn.cursor()
    
    cursor.execute('PRAGMA foreign_keys = ON;')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            login TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS convidados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            id_atendente INTEGER NOT NULL,
            FOREIGN KEY (id_atendente) REFERENCES usuarios(id)
        )
    ''')

    conn.commit()
    conn.close()

def inserirUsuario(nome, login, senha):
    conn = sqlite.connect('gestaoDB.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO usuarios (nome, login, senha) VALUES (?, ?, ?)
    ''', (nome, login, senha))
    conn.commit()
    conn.close()

def inserirConvidado(nome, id_atendente):
    conn = sqlite.connect('gestaoDB.sqlite')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO convidados (nome, id_atendente) VALUES (?, ?)
    ''', (nome, id_atendente))

    conn.commit()
    conn.close()

def verificarUsuario(login):
    conn = sqlite.connect('gestaoDB.sqlite')
    cursor = conn.cursor() 
    cursor.execute('SELECT * FROM usuarios WHERE login=?', (login,))
    dados = cursor.fetchall()
    conn.close()
    if dados:
        return dados
    else:
        return False

def listarConvidados():
    conn = sqlite.connect('gestaoDB.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT convidados.id AS id_convidado, convidados.nome AS nome_convidado, usuarios.nome AS nome_atendente
        FROM convidados
        INNER JOIN usuarios ON convidados.id_atendente = usuarios.id
        ORDER BY convidados.id
    ''')
    dados = cursor.fetchall()
    usuarios = []
    for dado in dados:
        usuarios.append(dado)
    conn.close()
    return usuarios

def removerConvidado(id_convidado):
    conn = sqlite.connect('gestaoDB.sqlite')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM convidados WHERE id=?', (id_convidado,))
    conn.commit()
    conn.close()