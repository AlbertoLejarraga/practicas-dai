from flask import Flask, render_template
app = Flask(__name__)
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/user/')
@app.route('/user/<user>')
def helloVariables(user = None):
    return render_template('index.html', logado = True, usuario_actual=user)
