from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Configuração do banco de dados
DATABASE = 'cadastro.db'

# Função para inicializar o banco de dados
def inicializar_banco():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY,
        nome TEXT NOT NULL,
        idade INTEGER
    )
    """)
    conn.commit()
    conn.close()

# Inicializa o banco de dados ao iniciar o app
inicializar_banco()

# Rota inicial (formulário de cadastro)
@app.route('/')
def index():
    return render_template('cadastro.html')

# Rota para cadastrar novos clientes
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form['nome']
    idade = request.form['idade']

    # Validação básica
    if not nome or len(nome) < 3:
        return "Nome deve ter pelo menos 3 caracteres."
    try:
        idade = int(idade)
        if idade <= 0:
            return "Idade deve ser um número positivo."
    except ValueError:
        return "Idade deve ser um número válido."

    # Inserir no banco de dados
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO clientes (nome, idade) VALUES (?, ?)", (nome, idade))
    conn.commit()
    conn.close()

    return redirect('/clientes')

# Rota para listar todos os clientes
@app.route('/clientes')
def listar_clientes():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM clientes")
    clientes = c.fetchall()
    conn.close()
    return render_template('clientes.html', clientes=clientes)

# Rota para exibir o formulário de edição
@app.route('/editar/<int:id>')
def editar(id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM clientes WHERE id = ?", (id,))
    cliente = c.fetchone()
    conn.close()
    return render_template('editar.html', cliente=cliente)

# Rota para atualizar os dados do cliente
@app.route('/atualizar/<int:id>', methods=['POST'])
def atualizar(id):
    nome = request.form['nome']
    idade = request.form['idade']

    # Validação básica
    if not nome or len(nome) < 3:
        return "Nome deve ter pelo menos 3 caracteres."
    try:
        idade = int(idade)
        if idade <= 0:
            return "Idade deve ser um número positivo."
    except ValueError:
        return "Idade deve ser um número válido."

    # Atualizar no banco de dados
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("UPDATE clientes SET nome = ?, idade = ? WHERE id = ?", (nome, idade, id))
    conn.commit()
    conn.close()

    return redirect('/clientes')

# Rota para deletar um cliente
@app.route('/deletar/<int:id>')
def deletar(id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("DELETE FROM clientes WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect('/clientes')

if __name__ == '__main__':
    app.run(debug=True)