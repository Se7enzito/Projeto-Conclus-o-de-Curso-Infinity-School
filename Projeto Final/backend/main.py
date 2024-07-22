from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from database.dbAPI import GerenciamentoUsers, GerenciamentoObjetos

app = Flask(__name__, template_folder="../frontend/templates")

app.static_folder = '../frontend/src'
app.static_url_path = '/static'

app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

userGerenciamento = GerenciamentoUsers()
objetosGerencimento = GerenciamentoObjetos()

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    
    if request.method == 'POST':
        user = request.form.get('user')
        senha = request.form.get('senha')
        
        if userGerenciamento.containsUser(user):
            if (userGerenciamento.senhaCorreta(user, senha)):
                session['user'] = user
                session['senha'] = senha
                return redirect(url_for('dashboard'))
            else:
                message = 'Usuário ou senha incorretos'
        else:
            message = 'Usuário ou senha incorretos'
            
    return render_template('index.html', message=message)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    user = session.get('user')
    senha = session.get('senha')
    
    if not userGerenciamento.senhaCorreta(user, senha) or not userGerenciamento.containsUser(user):
        return redirect(url_for('index'))
    
    perm = userGerenciamento.getPerm(user)
    
    if (perm == 1):
        perm = "Funcionário"
    elif (perm == 2):
        perm = "Gerente"
    else:
        perm = "Administrador de Segurança"
    
    return render_template('dashboard.html', user=user, permission=perm)

@app.route('/funcionarios', methods=['GET', 'POST'])
def funcionarios():
    user = session.get('user')
    senha = session.get('senha')
    
    if not userGerenciamento.senhaCorreta(user, senha) or not userGerenciamento.containsUser(user):
        return redirect(url_for('index'))
    
    perm = userGerenciamento.getPerm(user)
    
    if (perm != 3):
        return redirect(url_for('dashboard'))
    
    listaFunc = userGerenciamento.getAllUsers()
    
    return render_template('funcionarios.html', user=user, funcs=listaFunc)

@app.route('/recursos_internos/editar', methods=['GET', 'POST'])
def recursos_internos_editar():
    user = session.get('user')
    senha = session.get('senha')
    
    if not userGerenciamento.senhaCorreta(user, senha) or not userGerenciamento.containsUser(user):
        return redirect(url_for('index'))
    
    perm = userGerenciamento.getPerm(user)
    
    if (perm == 1):
        return redirect(url_for('dashboard'))
    
    i = objetosGerencimento.getAllItens()
    
    return render_template('recInternosEdit.html', user=user, items=i)

@app.route('/recursos_internos/ver', methods=['GET', 'POST'])
def recursos_internos_ver():
    user = session.get('user')
    senha = session.get('senha')
    
    if not userGerenciamento.senhaCorreta(user, senha) or not userGerenciamento.containsUser(user):
        return redirect(url_for('index'))
    
    i = objetosGerencimento.getAllItens()
    
    return render_template('recInternosVer.html', user=user, items=i)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('user', None)
    session.pop('senha', None)
    return redirect(url_for('index'))

@app.route('/save_funcionario', methods=['GET', 'POST'])
def save_funcionario():
    if request.method == 'POST':
        user = request.form.get('user')
        senha = request.form.get('senha')
        perm = request.form.get('perm')
        
        if user is None or senha is None or perm is None:
            return "Todos os campos são obrigatórios.", 400

        try:
            perm = int(perm)
        except ValueError:
            return "O valor de perm deve ser um número inteiro.", 400

        userGerenciamento.criarUser(str(user), str(senha), perm)
        
        return redirect(url_for('funcionarios'))
    else:
        return "Método não permitido", 405

@app.route('/rem_funcionario', methods=['GET', 'POST'])
def rem_funcionario():
    if request.method == 'POST':
        user = request.form.get('user')
        
        if user is None:
            return "Todos os campos são obrigatórios.", 400

        userGerenciamento.deletarUser(str(user))
        
        if (session.get('user') == str(user)):
            session.pop('user', None)
            session.pop('senha', None)
            
            return redirect(url_for('logout'))
        
        return redirect(url_for('funcionarios'))
    else:
        return "Método não permitido", 405

@app.route('/atua_funcionario', methods=['GET', 'POST'])
def atua_funcionario():
    if request.method == 'POST':
        user = request.form.get('user')
        senha = request.form.get('senha')
        perm = request.form.get('perm')
        
        if user is None or senha is None or perm is None:
            return "Todos os campos são obrigatórios.", 400

        try:
            if perm is None or perm == '':
                perm == 0
            else:
                perm = int(perm)
        except ValueError:
            return "O valor de perm deve ser um número inteiro. Valor sendo utilizado: " + perm + ".", 400

        userGerenciamento.atualizarUser(str(user), str(senha), perm)
        
        return redirect(url_for('funcionarios'))
    else:
        return "Método não permitido", 405
    
@app.route('/save_item', methods=['GET', 'POST'])
def save_item():
    if request.method == 'POST':
        item = request.form.get('item')
        tipo = request.form.get('tipo')
        quantidade = request.form.get('quantidade')
        
        if item is None or tipo is None or quantidade is None:
            return "Todos os campos são obrigatórios.", 400

        try:
            quantidade = int(quantidade)
        except ValueError:
            return "O valor de quantidade deve ser um número inteiro.", 400

        objetosGerencimento.adicionarItem(str(item), quantidade, str(tipo))
        
        return redirect(url_for('recursos_internos_editar'))
    else:
        return "Método não permitido", 405

@app.route('/rem_item', methods=['GET', 'POST'])
def rem_item():
    if request.method == 'POST':
        item = request.form.get('item')
        
        if item is None:
            return "Todos os campos são obrigatórios.", 400

        objetosGerencimento.removerItem(str(item))
        
        return redirect(url_for('recursos_internos_editar'))
    else:
        return "Método não permitido", 405

@app.route('/atua_item', methods=['GET', 'POST'])
def atua_item():
    if request.method == 'POST':
        item = request.form.get('item')
        tipo = request.form.get('tipo')
        quantidade = request.form.get('quantidade')
        
        if item is None or tipo is None or quantidade is None:
            return "Todos os campos são obrigatórios.", 400

        try:
            if (quantidade is None or quantidade == ""):
                quantidade = None
            else:
                quantidade = int(quantidade)
        except ValueError:
            return "O valor de quantidade deve ser um número inteiro.", 400

        objetosGerencimento.alterarItem(str(item), quantidade, str(tipo))
        
        return redirect(url_for('recursos_internos_editar'))
    else:
        return "Método não permitido", 405

if __name__ == '__main__':
    gerenciamento = GerenciamentoUsers()
    gerenciamento.criarTabela()
    
    itens = GerenciamentoObjetos()
    itens.criarTabela()
    
    app.run(host='127.0.0.1', port=8000, debug=True)
    
# AJAX
"""
HTML:
<div class="modal fade" id="modalAtua" tabindex="-1" role="dialog" aria-labelledby="modalTitleId"
     aria-hidden="true">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="modalTitleId">Adicionar um Funcionário</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form id="funcionarioForm">
                <div class="modal-body d-flex flex-column">
                    <label for="user">User</label>
                    <input type="text" name="user" id="user" placeholder="">
                    <label for="senha">Senha</label>
                    <input type="text" name="senha" id="senha" placeholder="">
                    <label for="perm">Permissão</label>
                    <p>1 - Funcionários<br>2 - Gerente<br>3 - Administrador de Segurança</p>
                    <input type="number" name="perm" id="perm" placeholder="Digite a permissão do funcionário">
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="submit" class="btn btn-primary">Save</button>
                </div>
            </form>
        </div>
    </div>
</div>

<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script>
    $(document).ready(function() {
        $('#funcionarioForm').on('submit', function(e) {
            e.preventDefault();
            $.ajax({
                type: 'POST',
                url: '{{ url_for("save_funcionario") }}',
                data: {
                    user: $('#user').val(),
                    senha: $('#senha').val(),
                    perm: $('#perm').val()
                },
                success: function(response) {
                    alert('Funcionário salvo com sucesso!');
                },
                error: function(error) {
                    alert('Erro ao salvar funcionário: ' + error.responseText);
                }
            });
        });
    });
</script>

PYTHON:
from flask import jsonify

@app.route('/save_funcionario', methods=['POST'])
def save_funcionario():
    user = request.form.get('user')
    senha = request.form.get('senha')
    perm = request.form.get('perm')

    if user is None or senha is None or perm is None:
        return jsonify({"error": "Todos os campos são obrigatórios."}), 400

    try:
        perm = int(perm)
    except ValueError:
        return jsonify({"error": "O valor de perm deve ser um número inteiro."}), 400

    result = userGerenciamento.atualizarUser(str(user), str(senha), perm)

    if result:
        return jsonify({"success": "Funcionário salvo com sucesso!"}), 200
    else:
        return jsonify({"error": "Erro ao salvar funcionário."}), 500
"""
