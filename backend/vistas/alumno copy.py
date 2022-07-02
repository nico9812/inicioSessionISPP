from flask import Blueprint, render_template, flash, request
from flask_login import login_required, current_user

from ..models.entidad.EntidadUsuario import User

from .. import mysql

vistAlumno = Blueprint("vistAlumno", __name__)


@vistAlumno.route("/carrera", methods=["GET", "POST"])
@login_required
def getCarreras():
    cur = mysql.connection.cursor()
    consulta = ('SELECT * FROM carrera order by carreranombre')
    cur.execute(consulta)
    row = cur.fetchall()
    return render_template("mostrarCarrera.html", row=row)


@vistAlumno.route("/carrera/<int:idcar>/plan", methods=["GET", "POST"])
@login_required
def getplan(idcar):    
    cur = mysql.connection.cursor()
    consulta = ('''
SELECT
carpo.plandeestudioid,
plandeestudio.plannombre,
carrera.carreraid,
carrera.carreranombre,
carpoid
FROM
carpo
left JOIN carrera on carpo.CarreraID = carrera.CarreraID
left JOIN plandeestudio on carpo.plandeestudioid = plandeestudio.PlanID
where carrera.carreraid = %s
order by CarreraNombre
''')
    cur.execute(consulta,([idcar]))
    row = cur.fetchall()
    return render_template("mostrarPlanes.html", row=row)

@vistAlumno.route("/carrera/<int:idcar>/plan/<int:idplan>/carpo/<int:idcarpo>/materias")
@login_required
def getMateriasCarreraPlanID(idcar, idplan, idcarpo):
    cur = mysql.connection.cursor()
    consulta = ("SELECT * FROM materia where idcarpo = %s")
    cur.execute(consulta,([idcarpo]))
    row = cur.fetchall()

    año=0
    for mat in row:
        for i in range(4):
            if int(mat[3])>año:
                año=int(mat[3])

    años = [['Primer Año','1'],['Segundo Año','2'],['Tercer Año','3'],['Cuarto Año','4'],['Quinto Año','5']]
    #cur.execute('SELECT carreraId FROM carpo WHERE carpoid = %s',([idcarpo]))
    #carreraId = int(cur.fetchone()[0])
    #cur.execute('SELECT año FROM carrera WHERE carreraid = %s',([carreraId]))
    #año = int(cur.fetchone()[0])
    return render_template("mostrarMateria.html", row=row, años = años, año = año)


@vistAlumno.route("/mostrarCarrerasInscriptas")
@login_required
def getCarrerasInscriptas():
    # Se optiene la ID del Usuario
    iduser = current_user.id
    
    #Primero se pasa por el Perfil del Usuario
    cur = mysql.connection.cursor()
    consulta = ("SELECT idusuarioperfil from usuariosperfiles where idusuario = %s")
    cur.execute(consulta,[(iduser)])
    iduser = cur.fetchone()[0]

    #Segundo se pasa por el Estudiante
    consulta = ("SELECT idestudiante from estudiante where IDusuariosPerfiles = %s")
    cur.execute(consulta,[(iduser)])
    iduser = cur.fetchone()[0]

    #Tercero se pasa por el CarpoEstudiante
    consulta = ("SELECT idCarpo, idCarpoEstudiante from CarpoEstudiante where idestudiante = %s")
    cur.execute(consulta,[(iduser)])
    auxiliar = cur.fetchall()
    Carpo = auxiliar
    idCarpoEstudiante = []
    row=[]
    #Cuarto, se revisa que Carrera es
    for car in Carpo:
        idCarpoEstudiante.append(car[1])
        consulta = ('''SELECT DISTINCT
CarreraNombre as 'Carrera',
PlanNombre as 'Plan',
IFNULL(OrientacionNombre,'Sin Orientación') as 'Orientación',
carpoid
FROM
carpo
left JOIN carrera on carpo.CarreraID = carrera.CarreraID
left JOIN plandeestudio on carpo.PlanDeEstudioID = plandeestudio.PlanID
left join orientacion on carpo.orientacionid = orientacion.orientacionid
where carpoid = %s
order by CarreraNombre;
''')
        cur.execute(consulta,[(car[0])])
        #row=str(cur.fetchone()).replace('(','').replace(')','').replace('\'','').replace(' ','').split(',')
        #print(str(car)+' 1 '+str(row))
        row.append(cur.fetchone())
    print(idCarpoEstudiante)
    idCarpoEstudiante = str(idCarpoEstudiante)    
    #Quinto, se revisa que Materias esta inscripto
    #consulta = ('select idmateria from carpestmateria where idcarpoestudiante = %s')
    #cur.execute(consulta, [(iduser)])
    #listaMateriasObtenidas = cur.fetchall()
    #materias = str(listaMateriasObtenidas)
    #materias = materias.replace('(','').replace(')','').replace('[','').replace(']','').replace(',','')
    return render_template("mostrarCarreraInscripta.html",rowcarpo=row, idCarpoEstudiante=idCarpoEstudiante)



@vistAlumno.route("/mostrarCarrerasInscriptas/Materias/<idCarpoEstudiante>/<idcarpo>")
@login_required
def getMateriasInscriptas():
    idcarpos = request.args.get('idcarpo')
    materias = request.args.get('idCarpoEstudiante')

    consulta = ('select idmateria from carpestmateria where idcarpoestudiante = %s')
    print(idcarpos)
    print(materias)
    # materias= materias.split(' ')
    # listaMaterias = []
    # for materia in materias:
    #     cur = mysql.connection.cursor()
    #     consulta = ('SELECT * from materia where idmateria = %s')
    #     cur.execute(consulta, [(str(materia))])
    #     row = cur.fetchone()
    #     listaMaterias.append(row)
    # año=0
    # for mat in listaMaterias:
    #     for i in range(4):
    #         if int(mat[3])>año:
    #             año=int(mat[3])

    años = [['Primer Año','1'],['Segundo Año','2'],['Tercer Año','3'],['Cuarto Año','4'],['Quinto Año','5']]
    #cur.execute('SELECT carreraId FROM carpo WHERE carpoid = %s',([idcarpo]))
    #carreraId = int(cur.fetchone()[0])
    #cur.execute('SELECT año FROM carrera WHERE carreraid = %s',([carreraId]))
    #año = int(cur.fetchone()[0])
    return render_template("mostrarMateriasInscriptas.html",materias=listaMaterias,años=años,año=año)