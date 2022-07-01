# Importación Modular
from .. import mysql
from ..models.entidad.EntidadUsuario import User
from ..models.ModeloUsuario import modeloUsuario
from random import choice
from ..funcionalidades.enviarEmail import email

# Importación de Flask
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask_wtf.csrf import CSRFProtect

# Desarrollo de la vista Login

auth = Blueprint('auth', __name__)

# Creación de la ruta login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('Lcorreo')
        contrasenia = request.form.get('Lpassword')
        user = User(usuario=usuario, contraseña=contrasenia, email=usuario)
        RetornoUsuario = modeloUsuario.logearUsuario(mysql, user)
        print(RetornoUsuario)
        if RetornoUsuario != None:
            if RetornoUsuario.contraseña or RetornoUsuario.contraseñatemp:
                cur = mysql.connection.cursor()
                cur.execute('UPDATE usuarios SET contraseñatemp = NULL WHERE idusuario = %s', (str(RetornoUsuario.id)))
                mysql.connection.commit()
                login_user(RetornoUsuario)
                if RetornoUsuario.contraseñatemp:
                    return redirect(url_for('auth.cambiarcontraseña'))
                return redirect(url_for('views.home'))
            else:
                flash('Contraseña Incorrecta', category='error')
        else:
            flash('Usuario Inexistente', category='error')

    return render_template("log_in.html", user=current_user)

@auth.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        usuario = request.form.get("Rusuario")
        correo = request.form.get("Rcorreo")
        password1 = request.form.get("Rpassword1")
        password2 = request.form.get("Rpassword2")

        user = User(id=None, usuario=usuario, contraseña=password1, email=correo)
        
        correo_existe = modeloUsuario.filtrarEmail(mysql, user)
        usuario_existe = modeloUsuario.filtrarUsuario(mysql, user)

        if correo_existe:
            flash('El correo ya esta en uso', category='error')
        elif usuario_existe:
            flash('El nombre de usuario ya esta en uso', category='error')
        elif (password1 != password2):
            flash('Las contraseñas no son iguales', category='error')
        elif len(usuario) <= 5:
            flash('Tu nombre de usuario es menor a 5 letras', category='error')
        elif len(password1) <= 6:
            flash('Las contraseña es muy corta', category='error')
        elif len(correo) < 4:
            flash('El correo es invalido', category='error')
        else:
            modeloUsuario.crearUsuario(mysql, user)
            usuario_nuevo = modeloUsuario.filtrarUsuario(mysql, user)
            return redirect(url_for('views.index'))

    return render_template("log_in.html", user=current_user)


# Creación de la ruta logout
@auth.route("/log-out")
@login_required
def logout():
    logout_user()
    flash('El usuario ha cerrado la sesión correctamente')
    return redirect(url_for("views.index"))

@auth.route('/recuperarcontrasenia', methods = ['GET', 'POST'])
def recuperarcontraseña():
        #genreacion y envio de contraseña temporal
        if request.method == 'POST':
            longitud = 10
            valores = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ=@#%&+"
            p=''
            p = p.join([choice(valores) for i in range(longitud)])

            mail = request.form.get('email')
            user = User(email=mail,contraseñatemp=p)
            
            try:
                modeloUsuario.comprobarEmail(mysql, user)
            except Exception as e:
                flash('Error a la hora de enviar el email')
                return redirect(url_for('auth.recuperarcontraseña'))
            
            Email = email(mail, p)
            Enviacion = email.enviarCorreo(Email)
            print(Enviacion)
            if Enviacion:
                flash('Email enviado')
                return redirect(url_for('views.index'))
            else:
                flash('El Email es Invalido')
        else:
            print("calderon gay")
        return render_template('recuperar_contraseña.html')
    

@auth.route('/cambiarcontraseña',methods = ['POST','GET'])
def cambiarcontraseña():
    #confirma si la nueva clave es correcta y la guarda
    if request.method == 'POST':
        id = request.form.get('id')
        contraseña1 = request.form.get('password')
        contraseña2 = request.form.get('passwordconfirm')
        if contraseña1 == contraseña2:
            try: 
                cur = mysql.connection.cursor()
                consulta = ('UPDATE usuarios SET contraseña = %s WHERE idusuario = %s')
                cur.execute(consulta,[User.generarhash(contraseña1), id])
                mysql.connection.commit()
                flash('Contraseña cambiada correctamente')
                return redirect(url_for('views.index'))
            except Exception as ex:
                flash('No se pudo realizar la consulta SQL', ex)
                print(ex)
                return render_template('cambiarcontraseña.html', id=id)
        else:
            flash('Las contraseñas no coinciden')
            return render_template('cambiarcontraseña.html', id=id)
    else:
        id = current_user.id
        logout_user()
        
    return render_template('cambiarcontraseña.html', id=id)
    
