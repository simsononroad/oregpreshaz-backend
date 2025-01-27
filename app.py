#!/srv/www/gyuris.hu/op.gyuris.hu/.venv/bin/python
from flask import *
import time
from flask import Flask, request, render_template, redirect, url_for, flash, session
#import database
import hashlib
import sqlite3
import datetime
import hashlib
from datetime import datetime



now = datetime.now()


def normal_to_hash(atalakitando, encode):
    password = atalakitando
    if encode == "":
        encode = "UTF-8"
    password_hash = hashlib.sha256(password.encode(encode)).hexdigest()
    return password_hash


# Felhasználó hazzáadásához szükséges lépések:
#   1. Nézze meg egy másik file-ban hogy a tesztelni kívánt jelszónak mi a kódja.
#   2. hozzon itt létre egy "password_in_hash_x" változót
#   3. A try-on belül hozzon létre egy parancsoot ami beteszi a helyére a felhasználóneve és jelszót


password_in_hash_2 = "9ad025d4631deee59e4d7d881d97f615f7cdb91a8ce639ab651ca445d431ef6b"

con = sqlite3.connect("db/login.db")
cur = con.cursor()
try:
    cur.execute("CREATE TABLE messages(id INTEGER PRIMARY KEY AUTOINCREMENT ,name, message, date, in_one)")
    cur.execute("CREATE TABLE login(id INTEGER PRIMARY KEY AUTOINCREMENT ,name, password, perm)")
    
    ins = cur.execute(f"insert into login (name, password, perm) values ('Dani', '{password_in_hash_2}', 'admin')")
    con.commit()
    
except:
    pass

# Táblák létrehozása
try:
    cur.execute("CREATE TABLE esemenyek(id INT PRIMARY KEY ,title, description, date, people)")
    ins = cur.execute(f"INSERT OR REPLACE INTO esemenyek (id, title, description, date, people) values ('1', ' ', ' ', ' ', ' ')")
    con.commit()
except:
    pass
try:
    cur.execute("CREATE TABLE user(id INTEGER PRIMARY KEY AUTOINCREMENT,name, password, days, date)")
    ins = cur.execute(f"INSERT OR REPLACE INTO esemenyek (id, title, description, date, people) values ('1', ' ', ' ', ' ', ' ')")
    con.commit()
except:
    pass
try:
    cur.execute("CREATE TABLE szovegek(id INT PRIMARY KEY ,values_of_hogyesz, info_of_hogyesz, kikapcsolodas_motor)")
    ins = cur.execute(f"INSERT OR REPLACE INTO szovegek (id, values_of_hogyesz, info_of_hogyesz, kikapcsolodas_motor) values ('1', 'Hőgyész a Tolnai- Hegyhát déli részén a Kapos- folyó mellett húzódó Donát - patak völgyében, szép természeti. környezetben fekszik.', 'Hőgyész a Tolnai- Hegyhát déli részén a Kapos- folyó mellett húzódó Donát - patak völgyében, szép természeti. környezetben fekszik. Wosinsky Mór, az ősi élet kiváló kutatója által feltárt régészeti leletek bizonyítják, hogy a terület a kőkorszakban meg a bronzkorban is lakott volt. A X. szd-ban Tevel hercegnek , aki Árpád fejedelem unokája volt , a jelenlegi Tevel község területén birtokolt , elődeink hermelin prémmel adóztak neki. A hölgymenyétet vadászókat hölgyészeknek nevezték, ebből alakult ki a község neve : HŐGYÉSZ. Az újkori Hőgyész alapítója : gr. Claudius Florimudus Mercy, a török kiűzésénél játszott szerepet. A Mercyek három generációja 50 évig élt a településen és a németek betelepítésénél nagy szerepük volt. Idejükben épült a kastély és az uradalmi épületek nagy része és a csicsói kápolna is akkor épült. Mezővárossá tették Hőgyészt, a Linnia-Fabrika létrehozása országos hírű volt. 1773-ban a Mercy család eladta az uradalmat az Apponyiaknak, akiknek 6 generációja 150 évig birtokolta a területet. A felvilágosult család iskolákat / elemi isk., latin isk., zene isk. / működtetett, kórházaz építtetett, templomot adott a falunak. A településen négy népcsoport / magyarok, németek, székelyek, cigányok/ együtt és közösen őrzik hagyományaikat. A település kisvárosi jellegét a grófok építette épületek és terek adják , melyeket kiváló művészek alkotásai díszítenek. A szép környezet, a természeti és épített látnivalók komoly turisztikai vonzerőt jelentenek. A csicsói zarándoklat mellett túraútvonalak nyújtanak barEnglishási lehetőséget. Négy napraforgós szálláshelyek gondtalan pihenést kínálnak.', 'Itt Hőgyészen és környékén minden motoros megtalálhatja a motorozásához szükséges környezetet. Pl: a crossosok el tudnak menni a zombai mxTrack-re. Az utcai motorosok felfedezhetik Hőgyész környékét . Az endurosok egyből a vendégház mellett kezdhetik a motorozást mivel a vendégház az utca legvégén található, onnan tovább földesút vezet.')")
    con.commit()
except:
    pass



app = Flask(__name__)
app.secret_key = "szupertitkoskulcs"  # Ezt cseréld le egy erősebb kulcsra!



# Előre meghatározott felhasználónév és jelszó


# Főoldal (index)
cur.execute(f"SELECT values_of_hogyesz FROM szovegek WHERE id = 1")
hogyesz_ertekei = cur.fetchall()
hogyesz_ertekei = hogyesz_ertekei[0][0]
hogyesz_ertekei_is_on = False



@app.route("/add_to_db", methods=["POST"])
def add_to_db():
    con = sqlite3.connect("db/login.db")
    cur = con.cursor()
    title_in_html = request.form['title']
    description_in_html = request.form['description']
    if title_in_html == "" or description_in_html == "":
        error_message = "A mezők kitöltése kötelező!"
        return redirect(url_for("dashboard", error_message=error_message))
    nowdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    people = session["user"]
    ins = cur.execute(f"INSERT OR REPLACE INTO esemenyek (id, title, description, date, people) values ('1', '{title_in_html}', '{description_in_html}', '{nowdate}', '{people}')")
    con.commit()
    try:
        user = session["user"]
    except:
        return redirect(url_for("index"))
    cur.execute(f"SELECT perm FROM login WHERE name='{user}'")
    user_with_rang = cur.fetchall()
    if user_with_rang[0][0] == "alap":
        return redirect(url_for("alap_dashboard"))
    elif user_with_rang[0][0] == "admin":
        return redirect(url_for("dashboard"))


@app.route("/value_of_hogyesz", methods=["POST"])
def value_of_hogyesz():
    con = sqlite3.connect("db/login.db")
    cur = con.cursor()
    value_of_hogyesz_in_html = request.form['hogyesz_erteke']
    cur.execute(f"SELECT info_of_hogyesz FROM szovegek WHERE id = 1")
    info_of_hogyesz = cur.fetchall()
    info_of_hogyesz = info_of_hogyesz[0][0]
    cur.execute(f"SELECT kikapcsolodas_motor FROM szovegek WHERE id = 1")
    kikapcsolodas_motor = cur.fetchall()
    kikapcsolodas_motor = kikapcsolodas_motor[0][0]
    if value_of_hogyesz_in_html == "":
        error_message = "A mezők kitöltése kötelező!"
        return redirect(url_for("dashboard", error_message=error_message))

    ins = cur.execute(f"INSERT OR REPLACE INTO szovegek (id, values_of_hogyesz, info_of_hogyesz, kikapcsolodas_motor) values ('1', '{value_of_hogyesz_in_html}', '{info_of_hogyesz}', '{kikapcsolodas_motor}')")
    con.commit()
    try:
        user = session["user"]
    except:
        return redirect(url_for("index"))
    cur.execute(f"SELECT perm FROM login WHERE name='{user}'")
    user_with_rang = cur.fetchall()
    if user_with_rang[0][0] == "alap":
        return redirect(url_for("alap_dashboard"))
    elif user_with_rang[0][0] == "admin":
        return redirect(url_for("dashboard"))

#=========EDIT TEXT===============================
@app.route("/value_of_hogyesz_insert_text", methods=["POST"])
def value_of_hogyesz_insert_text():
    con = sqlite3.connect("db/login.db")
    cur = con.cursor()
    cur.execute(f"SELECT info_of_hogyesz FROM szovegek WHERE id = 1")
    info_of_hogyesz = cur.fetchall()
    info_of_hogyesz = info_of_hogyesz[0][0]
    cur.execute(f"SELECT kikapcsolodas_motor FROM szovegek WHERE id = 1")
    kikapcsolodas_motor = cur.fetchall()
    kikapcsolodas_motor = kikapcsolodas_motor[0][0]
    ins = cur.execute(f"INSERT OR REPLACE INTO szovegek (id, values_of_hogyesz, info_of_hogyesz, kikapcsolodas_motor) values ('1', 'Hőgyész a Tolnai- Hegyhát déli részén a Kapos- folyó mellett húzódó Donát - patak völgyében, szép természeti. környezetben fekszik.', '{info_of_hogyesz}', '{kikapcsolodas_motor}')")
    con.commit()
    try:
        user = session["user"]
    except:
        return redirect(url_for("index"))
    cur.execute(f"SELECT perm FROM login WHERE name='{user}'")
    user_with_rang = cur.fetchall()
    if user_with_rang[0][0] == "alap":
        
        return redirect(url_for("alap_dashboard"))
    elif user_with_rang[0][0] == "admin":
        
        return redirect(url_for("dashboard"))




@app.route("/kikapcs_motor", methods=["POST"])
def kikapcs_motor():
    con = sqlite3.connect("db/login.db")
    cur = con.cursor()
    kikapcsolodas_motor_html = request.form['kikapcsolodas_motor']
    cur.execute(f"SELECT values_of_hogyesz  FROM szovegek WHERE id = 1")
    values_of_hogyesz  = cur.fetchall()
    values_of_hogyesz  = values_of_hogyesz[0][0]
    
    kikapcs_motor_html = request.form['kikapcsolodas_motor']
    
    cur.execute(f"SELECT info_of_hogyesz FROM szovegek WHERE id = 1")
    info_of_hogyesz = cur.fetchall()
    info_of_hogyesz = info_of_hogyesz[0][0]
    if kikapcs_motor_html == "":
        error_message = "A mezők kitöltése kötelező!"
        return redirect(url_for("dashboard", error_message=error_message))

    ins = cur.execute(f"INSERT OR REPLACE INTO szovegek (id, values_of_hogyesz, info_of_hogyesz, kikapcsolodas_motor) values ('1', '{values_of_hogyesz }', '{info_of_hogyesz}', '{kikapcsolodas_motor_html}')")
    con.commit()
    try:
        user = session["user"]
    except:
        return redirect(url_for("index"))
    cur.execute(f"SELECT perm FROM login WHERE name='{user}'")
    user_with_rang = cur.fetchall()
    if user_with_rang[0][0] == "alap":
        return redirect(url_for("moto_alap"))
    elif user_with_rang[0][0] == "admin":
        return redirect(url_for("admin_motor"))



@app.route("/kikapcs_motor_insert", methods=["POST"])
def kikapcs_motor_insert():
    con = sqlite3.connect("db/login.db")
    cur = con.cursor()
    cur.execute(f"SELECT info_of_hogyesz FROM szovegek WHERE id = 1")
    info_of_hogyesz = cur.fetchall()
    info_of_hogyesz = info_of_hogyesz[0][0]
    cur.execute(f"SELECT values_of_hogyesz FROM szovegek WHERE id = 1")
    values_of_hogyesz = cur.fetchall()
    values_of_hogyesz = values_of_hogyesz[0][0]
    ins = cur.execute(f"INSERT OR REPLACE INTO szovegek (id, values_of_hogyesz, info_of_hogyesz, kikapcsolodas_motor) values ('1', '{values_of_hogyesz}', '{info_of_hogyesz}', 'Itt Hőgyészen és környékén minden motoros megtalálhatja a motorozásához szükséges környezetet. Pl: a crossosok el tudnak menni a zombai mxTrack-re. Az utcai motorosok felfedezhetik Hőgyész környékét . Az endurosok egyből a vendégház mellett kezdhetik a motorozást mivel a vendégház az utca legvégén található, onnan tovább földesút vezet.')")
    con.commit()
    try:
        user = session["user"]
    except:
        return redirect(url_for("index"))
    cur.execute(f"SELECT perm FROM login WHERE name='{user}'")
    user_with_rang = cur.fetchall()
    if user_with_rang[0][0] == "alap":
        return redirect(url_for("moto_alap"))
    elif user_with_rang[0][0] == "admin":
        return redirect(url_for("admin_motor")) 





@app.route("/hogyesz_info", methods=["POST"])
def hogyesz_info():
    con = sqlite3.connect("db/login.db")
    cur = con.cursor()
    info_hogyesz_html = request.form['info_hogyesz']
    cur.execute(f"SELECT values_of_hogyesz  FROM szovegek WHERE id = 1")
    values_of_hogyesz  = cur.fetchall()
    values_of_hogyesz  = values_of_hogyesz[0][0]
    cur.execute(f"SELECT kikapcsolodas_motor FROM szovegek WHERE id = 1")
    kikapcsolodas_motor = cur.fetchall()
    kikapcsolodas_motor = kikapcsolodas_motor[0][0]
    if info_hogyesz_html == "":
        error_message = "A mezők kitöltése kötelező!"
        return redirect(url_for("dashboard", error_message=error_message))

    ins = cur.execute(f"INSERT OR REPLACE INTO szovegek (id, values_of_hogyesz, info_of_hogyesz, kikapcsolodas_motor) values ('1', '{values_of_hogyesz }', '{info_hogyesz_html}', '{kikapcsolodas_motor}')")
    con.commit()
    try:
        user = session["user"]
    except:
        return redirect(url_for("index"))
    cur.execute(f"SELECT perm FROM login WHERE name='{user}'")
    user_with_rang = cur.fetchall()
    if user_with_rang[0][0] == "alap":
        return redirect(url_for("info_alap"))
    elif user_with_rang[0][0] == "admin":
        return redirect(url_for("admin_info"))

@app.route("/hogyesz_info_insert", methods=["POST"])
def hogyesz_info_insert():
    con = sqlite3.connect("db/login.db")
    cur = con.cursor()
    cur.execute(f"SELECT values_of_hogyesz  FROM szovegek WHERE id = 1")
    values_of_hogyesz  = cur.fetchall()
    values_of_hogyesz  = values_of_hogyesz[0][0]
    cur.execute(f"SELECT kikapcsolodas_motor FROM szovegek WHERE id = 1")
    kikapcsolodas_motor = cur.fetchall()
    kikapcsolodas_motor = kikapcsolodas_motor[0][0]
    ins = cur.execute(f"INSERT OR REPLACE INTO szovegek (id, values_of_hogyesz, info_of_hogyesz, kikapcsolodas_motor) values ('1', '{values_of_hogyesz}', 'Hőgyész a Tolnai- Hegyhát déli részén a Kapos- folyó mellett húzódó Donát - patak völgyében, szép természeti. környezetben fekszik. Wosinsky Mór, az ősi élet kiváló kutatója által feltárt régészeti leletek bizonyítják, hogy a terület a kőkorszakban meg a bronzkorban is lakott volt. A X. szd-ban Tevel hercegnek , aki Árpád fejedelem unokája volt , a jelenlegi Tevel község területén birtokolt , elődeink hermelin prémmel adóztak neki. A hölgymenyétet vadászókat hölgyészeknek nevezték, ebből alakult ki a község neve : HŐGYÉSZ. Az újkori Hőgyész alapítója : gr. Claudius Florimudus Mercy, a török kiűzésénél játszott szerepet. A Mercyek három generációja 50 évig élt a településen és a németek betelepítésénél nagy szerepük volt. Idejükben épült a kastély és az uradalmi épületek nagy része és a csicsói kápolna is akkor épült. Mezővárossá tették Hőgyészt, a Linnia-Fabrika létrehozása országos hírű volt. 1773-ban a Mercy család eladta az uradalmat az Apponyiaknak, akiknek 6 generációja 150 évig birtokolta a területet. A felvilágosult család iskolákat / elemi isk., latin isk., zene isk. / működtetett, kórházaz építtetett, templomot adott a falunak. A településen négy népcsoport / magyarok, németek, székelyek, cigányok/ együtt és közösen őrzik hagyományaikat. A település kisvárosi jellegét a grófok építette épületek és terek adják , melyeket kiváló művészek alkotásai díszítenek. A szép környezet, a természeti és épített látnivalók komoly turisztikai vonzerőt jelentenek. A csicsói zarándoklat mellett túraútvonalak nyújtanak barEnglishási lehetőséget. Négy napraforgós szálláshelyek gondtalan pihenést kínálnak.', '{kikapcsolodas_motor}')")
    con.commit()
    try:
        user = session["user"]
    except:
        return redirect(url_for("index"))
    cur.execute(f"SELECT perm FROM login WHERE name='{user}'")
    user_with_rang = cur.fetchall()
    if user_with_rang[0][0] == "alap":
        return redirect(url_for("info_alap"))

    elif user_with_rang[0][0] == "admin":
        return redirect(url_for("admin_info"))

#============================end=========================================



@app.route("/change_datas", methods=["POST"])
def change_password():
    con = sqlite3.connect("db/login.db")
    cur = con.cursor()
    cur.execute(f"SELECT password FROM login WHERE name = '{session['user']}'")
    password_in_db = cur.fetchall()
    old_name = session["user"]
    new_password = request.form['new_password']
    old_password = request.form['old_password']
    old_password_in_hash = normal_to_hash(old_password, "UTF-8")
    password_in_db = password_in_db[0][0]
    if password_in_db == old_password_in_hash:
        new_password_in_hash = normal_to_hash(new_password, "UTF-8")
        ins = cur.execute(f"UPDATE login SET password = '{new_password_in_hash}' WHERE name = '{old_name}'")
        con.commit()
        session.pop("user", None)
        flash("Sikeres kijelentkezés.", "success")
        return redirect(url_for("login_page"))
    else:
        flash("Helytelen jelszó.", "error")
        error_message = "Helytelen jelszó."
        return redirect(url_for("change_data", error_message=error_message))

@app.route("/change_datas_alap", methods=["POST"])
def change_password_alap():
    con = sqlite3.connect("db/login.db")
    cur = con.cursor()
    cur.execute(f"SELECT password FROM user WHERE name = '{session['user_p']}'")
    password_in_db = cur.fetchall()
    old_name = session["user_p"]
    new_password = request.form['new_password']
    old_password = request.form['old_password']
    old_password_in_hash = normal_to_hash(old_password, "UTF-8")
    print(password_in_db)
    password_in_db = password_in_db[0][0]
    if password_in_db == old_password_in_hash:
        new_password_in_hash = normal_to_hash(new_password, "UTF-8")
        ins = cur.execute(f"UPDATE user SET password = '{new_password_in_hash}' WHERE name = '{old_name}'")
        con.commit()
        session.pop("user", None)
        flash("Sikeres kijelentkezés.", "success")
        return redirect(url_for("login_all"))
    else:
        flash("Helytelen jelszó.", "error")
        error_message = "Helytelen jelszó."
        return redirect(url_for("change_data", error_message=error_message))
    
    
    

@app.route("/login_all")
def login_all():
    return render_template("aloldalak/all_login.html")


@app.route("/changedata")
def change_data():
    if "user" not in session:
        flash("Először jelentkezz be!", "error")
    return render_template("aloldalak/admin/change_data.html", user=session["user"])

#Név változtatás
@app.route("/change_name", methods=["POST"])
def change_name():
    con = sqlite3.connect("db/login.db")
    cur = con.cursor()
    old_name = session["user"]
    new_name = request.form['new_name']


    ins = cur.execute(f"UPDATE login SET name = '{new_name}' WHERE name = '{old_name}'")
    con.commit()
    session.pop("user", None)
    flash("Sikeres kijelentkezés.", "success")
    return redirect(url_for("login_page"))

@app.route("/change_name_alap", methods=["POST"])
def change_name_alap():
    con = sqlite3.connect("db/login.db")
    cur = con.cursor()
    old_name = session["user_p"]
    new_name = request.form['new_name']


    ins = cur.execute(f"UPDATE user SET name = '{new_name}' WHERE name = '{old_name}'")
    con.commit()
    session.pop("user", None)
    flash("Sikeres kijelentkezés.", "success")
    return redirect(url_for("login_all"))

logged_in_username = ""
# Bejelentkezés
@app.route("/login", methods=["POST"])
def login():
    con = sqlite3.connect("db/login.db")
    cur = con.cursor()
    username_in_html = request.form['username']
    logged_in_username = username_in_html
    password_in_html = request.form['password']
    password_hash = hashlib.sha256(password_in_html.encode("UTF-8")).hexdigest()
    username_in_html_felesleggel = f"('{username_in_html}',)"
    password_hash_felesleggel = f"('{password_in_html}',)"
    # Hitelesítés az előre megadott adatokkal
    
    
    
    
    cur.execute(f"SELECT name, password FROM login WHERE name = \"{username_in_html}\"")
    login_in_db = cur.fetchall()
    
    if len(login_in_db) == 0:
        flash("Helytelen felhasználónév vagy jelszó.", "error")  
        return redirect(url_for("login_page"))
    if login_in_db[0][1] != password_hash:
        flash("Helytelen felhasználónév vagy jelszó.", "error")
        return redirect(url_for("login_page"))
    session["user"] = username_in_html
    flash("Sikeres bejelentkezés!", "success")

    try:
        user = session["user"]
    except:
        return redirect(url_for("index"))
    cur.execute(f"SELECT perm FROM login WHERE name='{user}'")
    user_with_rang = cur.fetchall()
    if user_with_rang[0][0] == "alap":
        return redirect(url_for("alap_dashboard"))
    elif user_with_rang[0][0] == "admin":
        return redirect(url_for("dashboard"))
    

#Alap rang felület

@app.route("/alap/dashboard")
def alap_dashboard():
    con = sqlite3.connect("db/login.db")
    cur = con.cursor()
    cur.execute(f"SELECT values_of_hogyesz FROM szovegek WHERE id = 1")
    hogyesz_ertekei = cur.fetchall()
    hogyesz_ertekei = hogyesz_ertekei[0][0]
    if "user" not in session:
        flash("Először jelentkezz be!", "error")
        return redirect(url_for("index"))
    return render_template("aloldalak/admin/alap_rang/dashboard.html", user=session["user"], hogyesz_ertekei=hogyesz_ertekei)

@app.route("/alap/change_data")
def change_data_alap():
    if "user" not in session:
        flash("Először jelentkezz be!", "error")
        return redirect(url_for("index"))
    return render_template("aloldalak/admin/alap_rang/change_data.html", user=session["user"])


@app.route("/user/change_data")
def change_data_user():
    if "user_p" not in session:
        flash("Először jelentkezz be!", "error")
        return redirect(url_for("index"))
    return render_template("aloldalak/user/change_data.html", user=session["user_p"])


@app.route("/alap/info")
def info_alap():
    con = sqlite3.connect("db/login.db")
    cur = con.cursor()
    cur.execute(f"SELECT info_of_hogyesz FROM szovegek WHERE id = 1")
    info_hogyesz = cur.fetchall()
    info_hogyesz = info_hogyesz[0][0]
    if "user" not in session:
        flash("Először jelentkezz be!", "error")
        return redirect(url_for("index"))
    return render_template("aloldalak/admin/alap_rang/info.html", user=session["user"], info_hogyesz=info_hogyesz)

@app.route("/alap/moto")
def moto_alap():
    con = sqlite3.connect("db/login.db")
    cur = con.cursor()
    cur.execute(f"SELECT kikapcsolodas_motor FROM szovegek WHERE id = 1")
    kikapcsolodas_motor = cur.fetchall()
    kikapcsolodas_motor = kikapcsolodas_motor[0][0]
    if "user" not in session:
        flash("Először jelentkezz be!", "error")
        return redirect(url_for("index"))
    return render_template("aloldalak/admin/alap_rang/moto.html", user=session["user"], kikapcsolodas_motor=kikapcsolodas_motor)
    

go_to_chat = True

# Dashboard (csak bejelentkezett felhasználóknak)

utotag = ""
if go_to_chat == False:
    utotag = ""
elif go_to_chat == True:
    utotag = "#chat-box"
print(utotag)

@app.route(f"/dashboard")
def dashboard():
    global go_to_chat
    con = sqlite3.connect("db/login.db")
    cur = con.cursor()
    cur.execute(f"SELECT values_of_hogyesz FROM szovegek WHERE id = 1")
    hogyesz_ertekei = cur.fetchall()
    hogyesz_ertekei = hogyesz_ertekei[0][0]
    try:
        user = session["user"]
    except:
        return redirect(url_for("index"))
    cur.execute(f"SELECT perm FROM login WHERE name='{user}'")
    user_with_rang = cur.fetchall()
    cur.execute(f"SELECT name, message, date FROM messages")
    messages_db = cur.fetchall()
    cur.execute(f"SELECT in_one FROM messages")
    in_one = cur.fetchall()
    print(messages_db)
    if "user" not in session:
        flash("Először jelentkezz be!", "error")
        return redirect(url_for("index"))
    if user_with_rang[0][0] == "alap":
        return redirect(url_for("alap_dashboard"))
    else:
        return render_template("aloldalak/admin/dashboard.html", user=session["user"], hogyesz_ertekei=hogyesz_ertekei, messages_db=messages_db, in_one=in_one)






@app.route("/edit_messages" , methods=["POST"])
def edit_messages():
    con = sqlite3.connect("db/login.db")
    cur = con.cursor()
    message = request.form["selected_message"]
    
    return redirect(url_for("dashboard"))
    














            

@app.route("/admin/motor")
def admin_motor():
    con = sqlite3.connect("db/login.db")
    cur = con.cursor()
    cur.execute(f"SELECT kikapcsolodas_motor FROM szovegek WHERE id = 1")
    kikapcsolodas_motor = cur.fetchall()
    kikapcsolodas_motor = kikapcsolodas_motor[0][0]
    try:
        user = session["user"]
    except:
        return redirect(url_for("index"))
    cur.execute(f"SELECT perm FROM login WHERE name='{user}'")
    user_with_rang = cur.fetchall()
    if "user" not in session:
        flash("Először jelentkezz be!", "error")
        return redirect(url_for("index"))
    if user_with_rang[0][0] == "alap":
        return redirect(url_for("alap_dashboard"))
    else:
        return render_template("aloldalak/admin/moto.html", user=session["user"], kikapcsolodas_motor=kikapcsolodas_motor)

@app.route("/admin_info")
def admin_info():
    con = sqlite3.connect("db/login.db")
    cur = con.cursor()
    cur.execute(f"SELECT info_of_hogyesz FROM szovegek WHERE id = 1")
    info_hogyesz = cur.fetchall()
    info_hogyesz = info_hogyesz[0][0]
    if "user" not in session:
        flash("Először jelentkezz be!", "error")
        return redirect(url_for("index"))
    try:
        user = session["user"]
    except:
        return redirect(url_for("index"))
    cur.execute(f"SELECT perm FROM login WHERE name='{user}'")
    user_with_rang = cur.fetchall()
    if user_with_rang[0][0] == "alap":
        return redirect(url_for("alap_dashboard"))
    else:
        return render_template("aloldalak/admin/info.html", user=session["user"], info_hogyesz=info_hogyesz)






@app.route("/add_people", methods=["POST"])
def add_people():
    if "user" not in session:
        flash("Először jelentkezz be!", "error")
        return redirect(url_for("index"))
    con = sqlite3.connect("db/login.db")
    cur = con.cursor()
    cur.execute(f"SELECT name FROM login WHERE id=1")
    id1 = cur.fetchall()
    cur.execute(f"SELECT name FROM login WHERE id=2")
    id2 = cur.fetchall()
    cur.execute(f"SELECT name FROM login WHERE id=3")
    id3 = cur.fetchall()
    cur.execute(f"SELECT perm FROM login")
    rang_db = cur.fetchall()

    username_in_html = request.form["new_name"]
    password_in_html = request.form["new_password"]
    rang = request.form["rang"]
    password_hash = hashlib.sha256(password_in_html.encode("UTF-8")).hexdigest()
    try:
        user = session["user"]
    except:
        return redirect(url_for("index"))
    cur.execute(f"SELECT perm FROM login WHERE name='{user}'")
    user_with_rang = cur.fetchall()


    if user_with_rang[0][0] == "admin":
        
        cur.execute(f"INSERT into login (name, password, perm) values ('{username_in_html}', '{password_hash}', '{rang}')")
        con.commit()
    elif user_with_rang[0][0] == "alap":
        print("Nincs jogod ehhez a művelethez!")
    else:
        print('nem eggyezik')

    try:
        user = session["user"]
    except:
        return redirect(url_for("index"))
    cur.execute(f"SELECT perm FROM login WHERE name='{user}'")
    user_with_rang = cur.fetchall()
    if user_with_rang[0][0] == "alap":
        return redirect(url_for("alap_dashboard"))
    else:
        return redirect(url_for("guest_page"))


@app.route("/admin/delete_people")
def delete_people():
    if "user" not in session:
        flash("Először jelentkezz be!", "error")
        return redirect(url_for("index"))
    con = sqlite3.connect("db/login.db")
    cur = con.cursor()
    
    
    try:
        user = session["user"]
    except:
        return redirect(url_for("index"))
    cur.execute(f"SELECT perm FROM login WHERE name='{user}'")
    user_with_rang = cur.fetchall()
    cur.execute(f"SELECT name FROM user")
    name_in_user_tb = cur.fetchall()
    names_str = ""
    for names in name_in_user_tb:
        names_str += f"{names[0]}, "
    names_str = names_str[:-2]
    if user_with_rang[0][0] == "alap":
        return redirect(url_for("alap_dashboard"))
    else:
        return render_template("aloldalak/admin/delete.html", user=session["user"], names_str=names_str, name_in_user_tb=name_in_user_tb)

@app.route("/del_people", methods=["POST"])
def del_people():
    if "user" not in session:
        flash("Először jelentkezz be!", "error")
        return redirect(url_for("index"))
    con = sqlite3.connect("db/login.db")
    cur = con.cursor()
    
    cur.execute(f"SELECT name FROM login WHERE id=1")
    id1 = cur.fetchall()
    cur.execute(f"SELECT name FROM login WHERE id=2")
    id2 = cur.fetchall()
    cur.execute(f"SELECT name FROM login WHERE id=3")
    id3 = cur.fetchall()
    
    user_to_del = request.form["del_name"]
    if user_to_del == id1[0][0] or user_to_del == id2[0][0] or user_to_del == id3[0][0]:
        flash("Ezeket a felhasználókat nem törölheti.")
        return redirect(url_for("guest_page"))
    
    ins = cur.execute(f"DELETE FROM login WHERE name='{user_to_del}'")
    con.commit()

    
    
    try:
        user = session["user"]
    except:
        return redirect(url_for("index"))
    cur.execute(f"SELECT perm FROM login WHERE name='{user}'")
    user_with_rang = cur.fetchall()
    if user_with_rang[0][0] == "alap":
        return redirect(url_for("alap_dashboard"))
    else:
        return redirect(url_for("guest_page"))
    
    


@app.route("/del_user_people", methods=["POST"])
def del_user_people():
    if "user" not in session:
        flash("Először jelentkezz be!", "error")
        return redirect(url_for("index"))
    con = sqlite3.connect("db/login.db")
    cur = con.cursor()

    
    user_to_del = request.form["del_name"]
    
    ins = cur.execute(f"DELETE FROM user WHERE name='{user_to_del}'")
    con.commit()
    
    
    try:
        user = session["user"]
    except:
        return redirect(url_for("index"))
    cur.execute(f"SELECT perm FROM login WHERE name='{user}'")
    user_with_rang = cur.fetchall()
    if user_with_rang[0][0] == "alap":
        return redirect(url_for("alap_dashboard"))
    else:
        return redirect(url_for("guest_page"))


@app.route("/admin/add_people")
def add_people_web():
    con = sqlite3.connect("db/login.db")
    cur = con.cursor()
    
    
    if "user" not in session:
        flash("Először jelentkezz be!", "error")
        return redirect(url_for("index"))
    
    try:
        user = session["user"]
    except:
        return redirect(url_for("index"))
    cur.execute(f"SELECT perm FROM login WHERE name='{user}'")
    user_with_rang = cur.fetchall()
    if user_with_rang[0][0] == "alap":
        return redirect(url_for("alap_dashboard"))
    else:
        return render_template("aloldalak/admin/add_people.html", user=session["user"])
    


    



@app.route("/user/changedata")
def user_change_data():
    con = sqlite3.connect("db/login.db")
    cur = con.cursor()
    if "user_p" not in session:
        flash("Először jelentkezz be!", "error")
        print("először jelentkezz be")
        return redirect(url_for("index"))
    
    user = session["user_p"]
    cur.execute(f"SELECT perm FROM login WHERE name='{user}'")
    user_with_rang = cur.fetchall()
    return render_template("aloldalak/user/change_data.html", user=session["user_p"])






    
@app.route("/add_stat", methods=["POST"])
def add_stat():
    con = sqlite3.connect("db/login.db")
    cur = con.cursor()
    if "user" not in session:
        flash("Először jelentkezz be!", "error")
        return redirect(url_for("index"))
    username_in_html = request.form["username"]
    try:
        day_in_html = int(request.form["days"])
    except:
        flash("Számot adj meg!")
    date_in_html = request.form["date"]


    cur.execute(f"SELECT days FROM user WHERE name='{username_in_html}'")
    days = cur.fetchall()
    try:
        days = int(days[0][0])
        day = days + day_in_html
        ins = cur.execute(f"UPDATE user SET days = '{day}' WHERE name='{username_in_html}'")
        con.commit()
        ins = cur.execute(f"UPDATE user SET date = '{date_in_html}' WHERE name='{username_in_html}'")
        con.commit()
    except:
        flash("Nincs ilyen felhasználónévvel ember")
    
    
    
    return redirect(url_for("guest_page"))
    

@app.route("/send_message", methods=["POST"])
def send_message():
    con = sqlite3.connect("db/login.db")
    cur = con.cursor()
    message_in_html = request.form["message"]
    user = session["user_p"]
    date = now.strftime("%Y.%m.%d, %H:%M:%S")
    in_one = f"{user}: {message_in_html} | {date}"
    cur.execute(f"INSERT INTO messages (name, message, date, in_one) values ('{user}', '{message_in_html}', '{date}', '{in_one}')")
    con.commit()
    return redirect(url_for("user_dashboard"))



@app.route("/send_admin_message", methods=["POST"])
def send_admin_message():
    con = sqlite3.connect("db/login.db")
    cur = con.cursor()
    message_in_html = request.form["message"]
    user = session["user"]
    date = now.strftime("%Y.%m.%d, %H:%M:%S")
    in_one = f"{user}(admin): {message_in_html} | {date}"
    cur.execute(f"INSERT INTO messages (name, message, date, in_one) values ('{user}', '{message_in_html}', '{date}', '{in_one}')")
    con.commit()
    return redirect(url_for("dashboard"))



"""
@app.route('/get_messages', methods=['GET'])
def get_messages():
    con = sqlite3.connect("db/login.db")
    cur = con.cursor()
    # Return the chat messages as HTML
    cur.execute(f"SELECT in_one FROM messages")
    in_one = cur.fetchall()
    

    return jsonify('<br>'.join(in_one))
"""




@app.route("/delete_messages", methods=["POST"])
def delete_message():
    con = sqlite3.connect("db/login.db")
    cur = con.cursor()
    print("s")
    del_message_html = request.form["delete_message"]
    print(del_message_html)
    ins = cur.execute(f"DELETE FROM messages WHERE in_one='{del_message_html}'")
    con.commit()
    global go_to_chat
    go_to_chat = True
    return redirect(url_for("dashboard"))











@app.route("/vendeg")
def guest_page():
    if "user" not in session:
        flash("Először jelentkezz be!", "error")
        return redirect(url_for("index"))

    con = sqlite3.connect("db/login.db")
    cur = con.cursor()
    cur.execute(f"SELECT name FROM user")
    names = cur.fetchall()
    b_name = ""
    for name in names:
        b_name += f"{name[0]}, "
    b_name = b_name[:-2]
    cur.execute(f"SELECT name FROM user")
    name_in_user_tb = cur.fetchall()
    cur.execute(f"SELECT name FROM login")
    name_in_login_tb = cur.fetchall()
    
    try:
        user = session["user"]
    except:
        return redirect(url_for("index"))
    cur.execute(f"SELECT perm FROM login WHERE name='{user}'")
    user_with_rang = cur.fetchall()
    if user_with_rang[0][0] == "alap":
        return redirect(url_for("alap_dashboard"))
    else:
        return render_template("aloldalak/admin/guest.html", name=b_name, name_in_user_tb=name_in_user_tb, name_in_login_tb=name_in_login_tb, user=user)
    
    


























@app.route("/login_page")
def login_page():
    return render_template("aloldalak/admin/login.html")

#Saját felhasználói profil
refresh = 0

@app.route("/user_dashboard")
def user_dashboard():
    con = sqlite3.connect("db/login.db")
    cur = con.cursor()
    alap_user = session["user_p"]
    if "user_p" not in session:
        flash("Először jelentkezz be!", "error")
        return redirect(url_for("index"))
    cur.execute(f"SELECT days FROM user WHERE name='{alap_user}'")
    days = cur.fetchall()
    cur.execute(f"SELECT date FROM user WHERE name='{alap_user}'")
    date = cur.fetchall()
    cur.execute(f"SELECT in_one FROM messages")
    in_one = cur.fetchall()
    print(in_one)
    

    return render_template("aloldalak/user/dashboard.html", days=days, date=date, user=alap_user, in_one=in_one, refresh=refresh)

@app.route("/user_page")
def user_page():
    return render_template("aloldalak/user_page.html")

@app.route("/user_login", methods=["POST"])
def user_login():
    global refresh
    con = sqlite3.connect("db/login.db")
    cur = con.cursor()
    username_in_html = request.form['username']
    logged_in_username = username_in_html
    password_in_html = request.form['password']
    password_hash = hashlib.sha256(password_in_html.encode("UTF-8")).hexdigest()
    username_in_html_felesleggel = f"('{username_in_html}',)"
    password_hash_felesleggel = f"('{password_in_html}',)"
    cur.execute(f"SELECT name, password FROM user WHERE name = \"{username_in_html}\"")
    login_in_db = cur.fetchall()
    
    if len(login_in_db) == 0:
        flash("Helytelen felhasználónév vagy jelszó.", "error")  
        return redirect(url_for("user_page"))
    if login_in_db[0][1] != password_hash:
        flash("Helytelen felhasználónév vagy jelszó.", "error")
        return redirect(url_for("user_page"))
    session["user_p"] = username_in_html
    flash("Sikeres bejelentkezés!", "success")
    refresh = 1
    return redirect(url_for("user_dashboard"))

    

@app.route("/user_register", methods=["POST"])
def user_register():
    con = sqlite3.connect("db/login.db")
    cur = con.cursor()
    cur.execute(f"SELECT name FROM login WHERE id=1")
    id1 = cur.fetchall()
    cur.execute(f"SELECT name FROM login WHERE id=2")
    id2 = cur.fetchall()
    cur.execute(f"SELECT name FROM login WHERE id=3")
    id3 = cur.fetchall()
    cur.execute(f"SELECT perm FROM login")
    rang_db = cur.fetchall()

    username_in_html = request.form["username"]
    password_in_html = request.form["password"]
    password_hash = hashlib.sha256(password_in_html.encode("UTF-8")).hexdigest()
    cur.execute(f"INSERT into user (name, password, days) values ('{username_in_html}', '{password_hash}', '0')")
    con.commit()
    session["user_p"] = username_in_html
    return redirect(url_for("user_dashboard"))













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
    con = sqlite3.connect("db/login.db")
    cur = con.cursor()
    cur.execute(f"SELECT title FROM esemenyek")
    title = cur.fetchall()
    title = title[0][0]
    cur.execute(f"SELECT description FROM esemenyek")
    description = cur.fetchall()
    description = description[0][0]
    cur.execute(f"SELECT date FROM esemenyek")
    date = cur.fetchall()
    date = date[0][0]
    cur.execute(f"SELECT people FROM esemenyek")
    people = cur.fetchall()
    people = people[0][0]
    cur.execute(f"SELECT values_of_hogyesz FROM szovegek WHERE id = 1")
    hogyesz_ertekei = cur.fetchall()
    hogyesz_ertekei = hogyesz_ertekei[0][0]
    return render_template('index.html', title=title, description=description, date=date, people=people, hogyesz_ertekei=hogyesz_ertekei)

@app.route('/informacio')
def info():
    con = sqlite3.connect("db/login.db")
    cur = con.cursor()
    cur.execute(f"SELECT info_of_hogyesz FROM szovegek WHERE id = 1")
    hogyesz_info = cur.fetchall()
    hogyesz_info = hogyesz_info[0][0]
    return render_template('aloldalak/info.html', hogyesz_info=hogyesz_info)


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
    con = sqlite3.connect("db/login.db")
    cur = con.cursor()
    cur.execute(f"SELECT kikapcsolodas_motor FROM szovegek WHERE id = 1")
    kikapcsolodas_motor = cur.fetchall()
    kikapcsolodas_motor = kikapcsolodas_motor[0][0]
    return render_template('aloldalak/moto.html', kikapcsolodas_motor=kikapcsolodas_motor)

@app.route('/sport')
def sport():
    return render_template('aloldalak/sport.html')



@app.route('/short')
def short():
    return render_template('linkshorter/index.html')


if __name__ == '__main__':
    app.run(debug=True)


#discord: ciganytanoda