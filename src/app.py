from flask import Flask, flash, redirect,render_template, url_for, request, flash
from flask_mysqldb import MySQL
from config import config
from models.entidad.user import User
from models.modelu import modeluser
from flask_login import LoginManager, current_user,login_user,logout_user, login_required
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import check_password_hash,generate_password_hash
from enviaremail import email
from random import choice

app = Flask(__name__)
csrf = CSRFProtect()
mysql = MySQL(app)
login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return modeluser.getbyid(mysql, id)

@app.route('/')
def index():
    #confirma si inicio session
    if not current_user.is_authenticated:
        return render_template('index.html')
    return redirect(url_for('home'))

@app.route('/logout')
@login_required
def logout():
    #cierre de session
    logout_user()
    return redirect(url_for('index'))

@app.route('/home')
@login_required
#paguina al iniciar session
def home():
    return render_template('home.html')

@app.route('/enviarmail', methods=['POST'])
def enviarmail():
    try:
        #genreacion y envio de contraseña temporal
        if request.method == 'POST':
            longitud = 10
            valores = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ=@#%&+"
            p=''
            p = p.join([choice(valores) for i in range(longitud)])

            mail = str(request.form['email'])
            user = User(1,'usuario', 'contraseña', mail, p)
            modeluser.comprobaremail(mysql, user)

            Email = email(mail, p)
            email.enviaremail(Email)
            flash('Email enviado')
            return redirect(url_for('index'))
    except Exception:
        flash('Error al enviar el email')
        return redirect(url_for('recuperarcontraseña'))
    

@app.route('/autentificacion', methods = ['GET', 'POST'])
def autentificacion():
    #autentificacion de inicio de session
    if request.method == 'POST':
        user = User(1,request.form['user'], request.form['password'], )
        logeouser = modeluser.login(mysql,user)
        if logeouser == None:
            flash('usuario no encontrado')
            return redirect(url_for('index'))
        else:
            if logeouser.contraseña or logeouser.contraseñatemp:
                cur = mysql.connection.cursor()
                cur.execute('UPDATE usuarios SET contraseñatemp = NULL WHERE idusuario = %s',(str(logeouser.id)))
                mysql.connection.commit()
                login_user(logeouser)
                print(logeouser.contraseñatemp)
                if logeouser.contraseñatemp:
                    return redirect(url_for('cambiarcontraseña'))
                return redirect(url_for('home'))
            else:
                flash('Contraseña incorrecta')
                return redirect(url_for('index'))

@app.route('/confirmarclave',methods = ['POST'])
def confirmarclave():
    #confirma si la nueva clave es correcta y la guarda
    try:
        if request.method == 'POST':
            id = request.form['id']
            contraseña = request.form['password']
            if contraseña == request.form['passwordconfirm']:
                cur = mysql.connection.cursor()
                cur.execute('UPDATE usuarios SET contraseña = %s WHERE idusuario = %s',(str(User.generarhash(contraseña)), str(id)))
                mysql.connection.commit()
                flash('Contraseña cambiada correctamente')
                return redirect(url_for('index'))
            else:
                flash('Las contraseñas no coinciden')
                return render_template('cambiarcontraseña.html', id = id)
        else:
            return render_template('cambiarcontraseña.html', id = id)
    except Exception as ex:
        print(ex)
        return render_template('cambiarcontraseña.html', id = id)

@app.route('/cambiarcontraseña')
def cambiarcontraseña():
    #cambiar contraseña
    id = current_user.id
    logout_user()
    return render_template('cambiarcontraseña.html', id = id)

@app.route('/recuperarcontraseña')
def recuperarcontraseña():
    #pedido de email de recuperacion
    return render_template('recuperar_contraseña.html')

#tratamiento de errores
def status_401(error):
    return redirect(url_for('index'))
def status_404(error):
    return "<h1>Página no encontrada</h1>", 404

if __name__ == '__main__':
    app.config.from_object(config['desarrollo'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()