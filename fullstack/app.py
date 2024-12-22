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

if __name__ == '__main__':
    app.run(debug=True)