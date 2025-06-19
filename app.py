
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

app.secret_key = '123456789acd' # usar vaiável de ambiente para segurança

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
            mensagem="Usuário cadastrado com sucesso. Faça login para acessar o sistema."
            return render_template("paginaLogin.html", mensagem=mensagem)
        else:
            mensagem="Usuário já existe"
            return render_template("paginaCadastroUsuario.html", mensagem=mensagem)
    
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
                session['usuario'] = {
                    'id': encontrado[0][0],
                    'nome': encontrado[0][1],
                    'email': encontrado[0][2]
                }

                mensagem="Usuario logado com sucesso"

                return render_template("indexLogado.html", mensagem=mensagem)
            else:    
                mensagem="Usuario ou senha incorreto"
                return render_template("paginaLogin.html", mensagem=mensagem)
        else:
            mensagem="Você não possui cadastro, por favor, cadastre-se."
            return render_template("paginaCadastroUsuario.html", mensagem=mensagem)
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

# rota para acessar a página logado
@app.route("/logado")
@usuarioLogado
def logado():
    return render_template("indexLogado.html")

# rota para buscr convidados na lista
@app.route("/listarConvidados")
@usuarioLogado
def listarConvidados():
    lista_convidadosDB = gestaoBD.listarConvidados()

    return render_template("listarConvidados.html", titulo='Lista de Convidados', convidados=lista_convidadosDB)

# rota para cadastrar convidado
@app.route("/cadastrarConvidado", methods=[ 'GET' ,'POST'])
@usuarioLogado
def cadastrarConvidado():
    if request.method == 'POST':
        nome = request.form.get('nomeConvidado')
        id_atendente = session['usuario']['id']

        gestaoBD.inserirConvidado(nome, id_atendente)

        mensagem="Convidado cadastrado com sucesso"
        return render_template("resultado.html", mensagem=mensagem)
    else:
        return render_template("paginaCadastroConvidado.html")

# rota para recuperar senha
@app.route("/recuperarSenha", methods=['GET', 'POST'])
def paginaRecuperar():
    if request.method == 'POST':
        email = request.form.get("emailUsuario")
        encontrado = gestaoBD.verificarUsuario(email)
        if encontrado:
            mensagem = f"Dados recuperados são login: {encontrado[0][2]} e senha: {encontrado[0][3]}"
            return render_template("paginaRecuperarSenha.html", mensagem=mensagem)
        else:
            return render_template("paginaRecuperarSenha.html", mensagem="Usuário não encontrado")
            
    return render_template("paginaRecuperarSenha.html")

# rota para buscar convidado pelo nome
@app.route("/buscarConvidado", methods=['GET', 'POST'])
@usuarioLogado
def buscarConvidado():
    if request.method == 'POST':
        nome = request.form.get('nomeConvidado')
        lista_convidadosDB = gestaoBD.listarConvidados()
        
        for convidado in lista_convidadosDB:
            _, nome_convidado, _ = convidado
            if nome_convidado.lower() == nome.lower():

                return render_template("listarConvidados.html", titulo='Convidado Pelo Nome', convidados=[convidado])

        mensagem = "Nenhum convidado encontrado com esse nome."
        return render_template("resultado.html", mensagem=mensagem)
    
    return render_template("paginaBuscarConvidado.html")

# rota para remover convidado
@app.route("/removerConvidado", methods=['POST'])
@usuarioLogado
def removerConvidado():
    if request.method == 'POST':
        id_convidado = request.form.get('id')

        gestaoBD.removerConvidado(id_convidado)
        mensagem = "Convidado removido com sucesso"
        return render_template("resultado.html", mensagem=mensagem)
    
    return render_template("paginaRemoverConvidado.html")

@app.route("/alterarSenha", methods=['GET', 'POST'])
@usuarioLogado
def alterarSenha():
    if request.method == 'POST':
        senha_antiga = request.form.get('senhaAntiga')
        nova_senha_1 = request.form.get('senhaNova1')
        nova_senha_2 = request.form.get('senhaNova2')

        if nova_senha_1 != nova_senha_2:
            mensagem = "As novas senhas não coincidem"
            return render_template("resultado.html", mensagem=mensagem)
        else:
            usuario = gestaoBD.verificarUsuario(session['usuario']['email'])

            if usuario[0][3] == senha_antiga:
                gestaoBD.atualizarSenhaUsuario(session['usuario']['id'], nova_senha_1)
                mensagem = "Senha alterada com sucesso"
                return render_template("resultado.html", mensagem=mensagem)
            else:
                mensagem = "Senha antiga incorreta"
                return render_template("resultado.html", mensagem=mensagem)
            

    return render_template("paginaAlterarSenha.html")

# rota para deslogar
@app.route("/deslogar")
def deslogar():
    session.pop('usuario', None)
    return render_template("paginaLogin.html", mensagem="Você foi deslogado com sucesso.")

#executar o servidor Flask
app.run(debug=True)
