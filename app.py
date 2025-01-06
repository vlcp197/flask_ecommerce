from flask import Flask, redirect, render_template, request, jsonify, url_for, session, flash
from functools import wraps
import sqlite3
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import bcrypt

DATABASE = "database.db"

def verify_user(username, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        stored_password_hash = result[0].encode('utf-8')
        if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash):
            return True
    return False

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            flash("Logue para acessar esta página", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__, template_folder="template", static_folder="static")
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.secret_key = "teste"

@app.route("/")
def home():
    conn = get_db_connection()
    posts = conn.execute("SELECT * FROM posts ORDER BY ROWID").fetchall()
    conn.close()
    return render_template("base.html", posts=posts, now=datetime.now().year)

@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    conn = get_db_connection()
    posts = conn.execute("SELECT * FROM posts ORDER BY nome ASC").fetchall()
    conn.close()
    return render_template("/admin/admin.html", posts=posts)

@app.route("/create", methods=["POST"])
def create():
    name = request.form["name"]
    description = request.form["description"]
    price = request.form["price"]

    conn = get_db_connection()
    conn.execute("INSERT INTO posts (nome, descricao,preco ) VALUES (?, ?, ?)", (name, description, price))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route("/update_name/<int:id>", methods=["POST"])
def update_name(id):
    name = request.form['name']

    conn = get_db_connection()
    conn.execute('UPDATE posts SET nome = ? WHERE id = ?', (name,  id))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route("/update_price/<int:id>", methods=["POST"])
def update_price(id):
    price = request.form['price']

    conn = get_db_connection()
    conn.execute('UPDATE posts SET preco = ? WHERE id = ?', (price,  id))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route("/update_desc/<int:id>", methods=["POST"])
def update_desc(id):
    description = request.form['description']

    conn = get_db_connection()
    conn.execute('UPDATE posts SET descricao = ? WHERE id = ?', (description,  id))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/update-image/<int:id>', methods=['POST'])
def update_image(id):
    if 'image' not in request.files:
        return jsonify({'status': 'error', 'message': 'Nenhuma imagem enviada.'})

    image = request.files['image']

    if image.filename == '':
        return jsonify({'status': 'error', 'message': 'Arquivo inválido.'})

    filename = secure_filename(image.filename)
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    conn = get_db_connection()
    conn.execute('UPDATE posts SET imagem = ? WHERE id = ?', (filename, id))
    conn.commit()
    conn.close()

    new_image_url = url_for('static', filename='uploads/' + filename)
    return jsonify({'status': 'success', 'new_image_url': new_image_url})

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if verify_user(username, password):
            session["logged_in"] = True
            flash("Logado com sucesso", "success")
            return redirect(url_for('admin'))
        else:
            flash("Usuário ou senha inválida", "danger")

    return render_template("/admin/login.html")

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Você deslogou.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)