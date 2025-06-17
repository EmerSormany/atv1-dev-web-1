
#importar a classe Flask
from flask import *

# importa wraps, que permite manter nomes origianais das funções
from functools import wraps

# importa a conexao de banco de dados
import gestaoBD

#instanciar o servidor Flask
app = Flask(__name__)

#criar banco / tabela
gestaoBD.criarTabela()

usuarios = []

app.secret_key = '123456789acd'

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
            mensagem="Usuário cadastrado com sucesso"
            return render_template("resultado.html", mensagem=mensagem)
        else:
            mensagem="Usuário já existe"
            return render_template("resultado.html", mensagem=mensagem)
    
    return render_template('paginaCadastroUsuario.html')

#rota para receber login e senha e fazer a autenticação (login)
@app.route("/autenticarUsuario", methods=[ 'GET' ,'POST'])
def autenticar():
    if request.method == 'POST':
        email = request.form.get("loginUsuario")
        senha = request.form.get("senhaUsuario")

        encontrado = gestaoBD.verificarUsuario(email)

        if(encontrado):
            if(encontrado[0][3] == senha):
                mensagem="Usuario logado com sucesso"
                session['usuario_id'] = encontrado[0][0]
                return render_template("resultado.html", mensagem=mensagem)
            else:    
                mensagem="Usuario ou senha incorreto"
                return render_template("resultado.html", mensagem=mensagem)
        else:
            mensagem="Você não possui cadastro, por favor, cadastre-se."
            return render_template("resultado.html", mensagem=mensagem)
    else:
        return render_template("paginaLogin.html")

# middleware para proteger rotas de acesso sem login
def usuarioLogado(f):
    @wraps(f)
    def funcaoDecorada(*args, **kwargs):
        if "usuario" not in session:
            return render_template("paginaLogin.html", mensagem="Você precisa estar logado para acessar esta página.")
        return f(*args, **kwargs)
    return funcaoDecorada

# rota para buscr convidados na lista
@app.route("/listarConvidados")
@usuarioLogado
def listarUsuarios():
    lista_usuariosDB = gestaoBD.listarUsuarios()
    return render_template("listarConvidados.html", lista=lista_usuariosDB)

@app.route("/cadastrarConvidado", methods=[ 'GET' ,'POST'])
@usuarioLogado
def cadastrarConvidado():
    if request.method == 'POST':
        nome = request.form.get('nomeConvidado')
        id_atendente = session['usuario_id']

        gestaoBD.inserirConvidado(nome, id_atendente)

        mensagem="Convidado cadastrado com sucesso"
        return render_template("resultado.html", mensagem=mensagem)
    else:
        return render_template("paginaCadastroConvidado.html")

@app.route("/recuperarSenha", methods=['GET', 'POST'])
def paginaRecuperar():
    if request.method == 'POST':
        email = request.form.get("emailUsuario")
        encontrado = gestaoBD.verificarUsuario(email)
        if encontrado:
            mensagem = f"Dados recuperados são login: {encontrado[0][2]} e senha: {encontrado[0][3]}"
            return render_template("resultado.html", mensagem=mensagem)
        else:
            return render_template("resultado.html", mensagem="Usuário não encontrado")
            
    return render_template("paginaRecuperarSenha.html")


#executar o servidor Flask
app.run(debug=True)
