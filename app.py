from flask import *

from flask import Flask, request, render_template, redirect, url_for, flash, session
#import database
import hashlib
import sqlite3

# Felhasználó hazzáadásához szükséges lépések:
#   1. Nézze meg egy másik file-ban hogy a tesztelni kívánt jelszónak mi a kódja.
#   2. hozzon itt létre egy "password_in_hash_x" változót
#   3. A try-on belül hozzon létre egy parancsoot ami beteszi a helyére a felhasználóneve és jelszót

password_in_hash_1 = "b909abf3d9725ca479f74046b6a1235b973021bb3da7b8e212c113da8a4c86e6"
password_in_hash_2 = "c52c5501c5ddd107202a95915b4466f98773b611a09cf8a283ebbe2760f6236a"
password_in_hash_3 = "f854b2aeb789d616b26acff4df9ff7741d09d5f7a63add238201880e5b10bf2b"
con = sqlite3.connect("login.db")
cur = con.cursor()
try:
    cur.execute("CREATE TABLE login(id INT PRIMARY KEY ,name, password)")
    ins = cur.execute(f"insert into login (name, password) values ('Mariann', '{password_in_hash_1}')")
    con.commit()
    ins = cur.execute(f"insert into login (name, password) values ('asfdasd', '{password_in_hash_2}')")
    con.commit()
    ins = cur.execute(f"insert into login (name, password) values ('oasdasasdasdk', '{password_in_hash_3}')")
    con.commit()
except:
    pass



app = Flask(__name__)
app.secret_key = "szupertitkoskulcs"  # Ezt cseréld le egy erősebb kulcsra!



# Előre meghatározott felhasználónév és jelszó


# Főoldal (index)

try:
    cur.execute("CREATE TABLE esemenyek(id INT PRIMARY KEY ,title, description)")
    ins = cur.execute(f"INSERT OR REPLACE INTO esemenyek (id, title, description) values ('1', ' ', ' ')")
    con.commit()
except:
    pass
@app.route("/add_to_db", methods=["POST"])
def add_to_db():
    con = sqlite3.connect("login.db")
    cur = con.cursor()
    title_in_html = request.form['title']
    description_in_html = request.form['description']
    if title_in_html == "" or description_in_html == "":
        error_message = "A mezők kitöltése kötelező!"
        return redirect(url_for("dashboard", error_message=error_message))

    ins = cur.execute(f"INSERT OR REPLACE INTO esemenyek (id, title, description) values ('1', '{title_in_html}', '{description_in_html}')")
    con.commit()
    return redirect(url_for("dashboard"))


# Bejelentkezés
@app.route("/login", methods=["POST"])
def login():
    con = sqlite3.connect("login.db")
    cur = con.cursor()
    username_in_html = request.form['username']
    password_in_html = request.form['password']
    password_hash = hashlib.sha256(password_in_html.encode("UTF-8")).hexdigest()
    username_in_html_felesleggel = f"('{username_in_html}',)"
    password_hash_felesleggel = f"('{password_in_html}',)"
    print("================================")
    print(f"A felhasználó beírta: {username_in_html_felesleggel}")
    print(f"A felhasználó beírta: {password_hash_felesleggel}")
    print("================================")
    # Hitelesítés az előre megadott adatokkal
    
    cur.execute(f"SELECT name, password FROM login WHERE name = \"{username_in_html}\"")
    login_in_db = cur.fetchall()
    print(login_in_db)
    
    if len(login_in_db) == 0:
        flash("Helytelen felhasználónév vagy jelszó.", "error")
        return redirect(url_for("login_page"))
    if login_in_db[0][1] != password_hash:
        flash("Helytelen felhasználónév vagy jelszó.", "error")
        return redirect(url_for("login_page"))
    session["user"] = username_in_html
    flash("Sikeres bejelentkezés!", "success")
    return redirect(url_for("dashboard"))
    
    
    

# Dashboard (csak bejelentkezett felhasználóknak)
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        flash("Először jelentkezz be!", "error")
        return redirect(url_for("index"))
    return render_template("aloldalak/admin/dashboard.html", user=session["user"])

@app.route("/login_page")
def login_page():
    return render_template("aloldalak/admin/login.html")


# Kijelentkezés
@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Sikeres kijelentkezés.", "success")
    return redirect(url_for("index"))



#=======================================================================================================


app.template_folder = 'templates'
app.static_folder = 'static'


@app.route('/')
def index():
    #print(title, description)
    con = sqlite3.connect("login.db")
    cur = con.cursor()
    cur.execute(f"SELECT title FROM esemenyek")
    title = cur.fetchall()
    title = title[0][0]
    cur.execute(f"SELECT description FROM esemenyek")
    description = cur.fetchall()
    description = description[0][0]
    return render_template('index.html', title=title, description=description)

@app.route('/informacio')
def info():
    return render_template('aloldalak/info.html')

@app.route('/galeria')
def galeria():
    return render_template('aloldalak/galery.html')

@app.route('/kikapcsolodasi_lehetosegek')
def kikapcsolodasi_lehetosegek():
    return render_template('aloldalak/kikapcs.html')

@app.route('/elerhetosegek')
def elerhetosegek():
    return render_template('aloldalak/elerhetosegek.html')

@app.route('/send_message')
def sand_message():
    return render_template('aloldalak/sand_message.html')

@app.route('/kepek/furdo')
def furdo():
    return render_template('aloldalak/imagepage/furdo.html')

@app.route('/kepek/kint')
def kint():
    return render_template('aloldalak/imagepage/kint.html')

@app.route('/kepek/konyha')
def konyha():
    return render_template('aloldalak/imagepage/konyha.html')

@app.route('/kepek/nappali')
def nappali():
    return render_template('aloldalak/imagepage/nappali.html')

@app.route('/kepek/szoba')
def szoba():
    return render_template('aloldalak/imagepage/szoba.html')

@app.route('/kepek/telikert')
def telikert():
    return render_template('aloldalak/imagepage/telikert.html')

@app.route('/kepek/udvar')
def udvar():
    return render_template('aloldalak/imagepage/udvar.html')

@app.route('/segitseg')
def segitseg():
    return render_template('aloldalak/help.html')

@app.route('/kikapcsolodasi_lehetosegek/motorozas')
def motorozas():
    return render_template('aloldalak/moto.html')

@app.route('/sport')
def sport():
    return render_template('aloldalak/sport.html')

if __name__ == '__main__':
    app.run(debug=False)