from flask import *

app = Flask(__name__)
app.template_folder = 'templates'
app.static_folder = 'static'

class path():
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
path()

if __name__ == '__main__':
    app.run(debug=True)