import sqlite3 as sqlite

def criarTabela():
    conn = sqlite.connect('gestaoDB.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            login TEXT NOT NULL,
            senha TEXT NOT NULL
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

def verificarUsuario(login):
    pass

def listarUsuarios():
    conn = sqlite.connect('gestaoDB.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios order by id desc')
    dados = cursor.fetchall()
    usuarios = []
    for dado in dados:
        usuarios.append(dado)
    conn.close()
    return usuarios

def login(login, senha):
    conn = sqlite.connect('gestaoDB.sqlite')
    cursor = conn.cursor()
    #cursor.execute(f"SELECT * FROM usuarios WHERE login='{login}' and senha='{senha}'")
    cursor.execute("SELECT * FROM usuarios WHERE login=? and senha=?", (login, senha))
    dados = cursor.fetchall()
    conn.close()
    if len(dados) > 0:
        return True
    else:
        return False