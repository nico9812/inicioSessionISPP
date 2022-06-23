
from re import U
from .entidad.user import User
class modeluser():

    @classmethod
    def login(self, mysql, user):
        try:
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM usuarios WHERE usuario = \'{}\''.format(user.usuario))
            row = cur.fetchone()
            if row != None:
                temp=row[4]
                if temp != None:
                    temp = User.checkpassword(temp, user.contraseña)
                else:
                    temp = False
                user = User(row[0],row[1],User.checkpassword(row[2],user.contraseña),row[3], temp)
                return user
            else:
                return None

        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def comprobaremail(self, mysql, user):
        
        try:
            cur = mysql.connection.cursor()
            cur.execute('SELECT email, idusuario FROM usuarios WHERE email = \'{}\''.format(str(user.email)))
            row=cur.fetchone()
            ema=str(row[0])
            id=int(row[1])
            if user.email == ema:
                
                cur.execute('UPDATE usuarios SET contraseñatemp = %s WHERE idusuario = %s',(str(User.generarhash(user.contraseñatemp)), id))
                mysql.connection.commit()

        except Exception as ex:
            raise Exception(ex)
    

    @classmethod
    def getbyid(self, mysql, id):
        try:
            cur = mysql.connection.cursor()
            sql = 'SELECT idusuario, usuario, email FROM usuarios WHERE idusuario = {}'.format(id)
            cur.execute(sql)
            row = cur.fetchone()
            if row != None:
                return User(row[0],row[1],row[2],None)
            else:
                return None
     
        except Exception as ex:
            raise Exception(ex)
        