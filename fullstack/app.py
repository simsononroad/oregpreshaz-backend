from flask import *

app = Flask(__name__)
app.template_folder = 'templates'
app.static_folder = 'static'


@app.route('/')
def index():
    return render_template('index.html')

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


if __name__ == '__main__':
    app.run(debug=True)