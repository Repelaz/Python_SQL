from flask import Flask, render_template, request, flash, url_for, redirect
import fdb

app = Flask(__name__)

app.config['SECRET_KEY'] = 'RAPAIZE'

host = 'localhost'
database = r'C:\Users\Aluno\Downloads\BANCO\BANCO.FDB'
user = 'sysdba'
password = 'sysdba'

con = fdb.connect(host = host, database = database, user = user, password = password)

class Livro:
    def __init__(self, id_livro, titulo, autor, ano_publicado):
        self.id_livro = id_livro
        self.titulo = titulo
        self.autor = autor
        self.ano_publicado = ano_publicado

@app.route('/')
def index():
    cursor = con.cursor()
    cursor.execute('SELECT id_livro, titulo, autor, ano_publicado FROM livro')
    livros = cursor.fetchall()
    cursor.close()
    return render_template('livros.html', livros = livros)

@app.route('/novo')
def novo():
    return render_template('novo.html', titulo = 'Novo Livro')

@app.route('/criar', methods=['POST'])
def criar():
    titulo = request.form['titulo']
    autor = request.form['autor']
    ano_publicado = request.form['ano_publicado']

    cursor = con.cursor()

    try:
        cursor.execute("SELECT 1 FROM livro WHERE TITULO = ?", (titulo,))
        if cursor.fetchone():
            flash("Erro: Livro já cadastrado.", "error")
            return redirect(url_for('novo'))

        cursor.execute("INSERT INTO livro (TITULO, AUTOR, ANO_PUBLICADO) "
                       "VALUES (?, ?, ?)", (titulo, autor, ano_publicado))
        con.commit()

    finally:
        cursor.close()

    flash("Livro cadastrado com sucesso!", "success")
    return redirect(url_for('index'))

@app.route('/atualizar')
def atualizar():
    return render_template('editar.html', titulo = 'Editar Livro')

@app.route('/editar/<int:id>', methods = ['GET', 'POST'])
def editar(id):
    cursor = con.cursor()
    cursor.execute('SELECT id_livro, titulo, autor, ano_publicado '
                   'FROM livro WHERE ID_LIVRO = ?', (id,))
    livro = cursor.fetchone()

    if not livro:
        cursor.close()
        flash('Livro não encontrado', 'error')
        return redirect(url_for('index'))
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        ano_publicado = request.form['ano_publicado']

        cursor.execute('update livro set titulo = ?, autor = ?, ano_publicado = ? where id_livro = ?',
                       (titulo, autor, ano_publicado, id))

        con.commit()
        cursor.close()
        flash('Livro atualizado com sucesso!', 'sucess')
        return redirect(url_for('index'))

    cursor.close()
    return render_template('editar.html', livro = livro, titulo = 'Editar Livro')

@app.route('/deletar/<int:id>', methods = ['POST'])
def deletar(id):
    cursor = con.cursor()

    try:
        cursor.execute('DELETE FROM livo where id_livro = ?', (id, ))
        con.commit()
        flash('Livro Excluido com sucesso!', 'sucess')
    except Exception as e:
        con.rollback()
        flash('Erro ao excluir o livro.', 'error')

    finally:
        cursor.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

