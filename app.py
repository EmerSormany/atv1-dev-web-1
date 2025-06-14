
#importar a classe Flask
from flask import *

import gestaoBD

#instanciar o servidor Flask
app = Flask(__name__)

#criar banco / tabela
gestaoBD.criarTabela()

usuarios = []

#app.register_blueprint(home_route)

#rota padrão (página principal)
@app.route("/")
def principal():
    return render_template("index.html")

#rota para receber os dados do usuário e cadastrar novo usuário na lista
@app.route("/cadastrarUsuario", methods=["GET","POST"])
def cadastrarUsuario():
    if request.method == 'POST':
        nome = request.form.get('nomeUsuario')
        login = request.form.get('loginUsuario')
        senha = str(request.form.get('senhaUsuario'))

        if(gestaoBD.verificarUsuario(login)==False):
            gestaoBD.inserirUsuario(nome, login, senha)
            mensagem="usuário cadastrado com sucesso"
            return render_template("resultado.html", mensagem=mensagem)
        else:
            mensagem="usuário já existe"
            return render_template("resultado.html", mensagem=mensagem)
    
    return render_template('paginaCadastroUsuario.html')

#rota para receber login e senha e fazer a autenticação (login)
@app.route("/autenticarUsuario", methods=['POST'])
def autenticar():
    login = request.form.get("loginUsuario")
    senha = str(request.form.get("senhaUsuario"))
    
    logado=gestaoBD.login(login, senha)

    if(logado==True):
        return render_template("logado.html")
    else:    
        mensagem="usuario ou senha incorreto"
        return render_template("home.html", mensagem=mensagem)

@app.route("/listarUsuarios")
def listarUsuarios():
    #return render_template("lista.html", lista=lista_usuarios)
    lista_usuariosDB = gestaoBD.listarUsuarios()
    return render_template("lista.html", lista=lista_usuariosDB)

@app.route("/paginaRecuperarSenha")
def paginaRecuperar():
    return render_template("recuperacao.html")

@app.route("/recuperarSenha", methods=['POST'])
def recuperarSenha():
    nome = request.form.get("nomeUsuario")
    login = request.form.get("loginUsuario")
   
    encontrado=False

    if(gestaoBD.verificarUsuario(login)==True):
        encontrado=True

    if(encontrado==True):
        senha = str(gestaoBD.recuperarSenhaBD(nome, login))
        mensagem="sua senha"+senha
        return render_template("recuperacao.html", mensagem=mensagem)
    else:    
        mensagem="usuario nao encontrado"
        return render_template("recuperacao.html", mensagem=mensagem)


#executar o servidor Flask
app.run(debug=True)
