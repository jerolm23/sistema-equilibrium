from flask import Flask, render_template,   request, jsonify
import MySQLdb
from flask_cors import CORS
import smtplib 
from email.message import EmailMessage 
from flask_mail import Mail, Message

app=Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'  
app.config['MAIL_PORT'] = 587  
app.config['MAIL_USE_TLS'] = True  
app.config['MAIL_USERNAME'] = 'equilibriumlifeparati@gmail.com'  
app.config['MAIL_PASSWORD'] = 'x r y e s h y d i p c a u z a n'             

CORS(app)

mail = Mail(app)

@app.route("/registro", methods=['POST'])
def insertar():

    cuerpo=request.get_json()

    conexion=MySQLdb.connect("localhost", "root", "admin", "proyecto")

    cursor=conexion.cursor()

    print(request.get_json())
    print(request.get_json().get("nombre"))

    cursor.execute(f"INSERT INTO usuario(id,nombre,correo,contrasena) VALUES (0,'{cuerpo.get("nombre")}', '{cuerpo.get("email")}', '{cuerpo.get("contrasena")}')")


    conexion.commit()

    return "Usuario registrado exitosamente!"

@app.route("/login/<email>/<contrasena>")
def login(email,contrasena):

    conexion=MySQLdb.connect("localhost", "root", "admin", "proyecto")

    cursor=conexion.cursor()

    ejecucion=cursor.execute(f"SELECT * FROM usuario WHERE correo='{email}' and contrasena='{contrasena}'")

    if(ejecucion==0):
        return jsonify({"estado":"no"})
    else:
        registros=cursor.fetchall()
        print(registros)
        return jsonify({"estado":"si", "id":registros[0][0]})

@app.route("/obtenerUsuario/<id>")
def obt(id):

    conexion=MySQLdb.connect("localhost", "root", "admin", "proyecto")

    cursor=conexion.cursor()

    cursor.execute(f"SELECT * FROM USUARIO WHERE id={id}")

    registro=cursor.fetchall()

    datos={"nombre":registro[0][1], "correo":registro[0][2],"contra":registro[0][3]}

    return jsonify(datos)


@app.route("/actualizar", methods=['POST'])
def udate():

    body=request.get_json()
    

    conexion=MySQLdb.connect("localhost", "root", "admin", "proyecto")

    cursor=conexion.cursor()

    cursor.execute(f"UPDATE USUARIO SET nombre='{body.get("nombre")}', correo='{body.get("correo")}', contrasena='{body.get("contra")}' WHERE id={body.get("id")}")


    conexion.commit()
    
    return "OK"

@app.route("/eliminar/<id>")
def delet(id):
    conexion=MySQLdb.connect("localhost", "root", "admin", "proyecto")

    cursor=conexion.cursor()

    cursor.execute(f"DELETE FROM USUARIO WHERE id={id}")

    conexion.commit()

    return "OK"

@app.route("/enviarMensaje", methods=["POST"])
def sendM():

    body=request.get_json()
    bodyEmail=f"""  
     <h1 style='color:rgb(23,229,23)'>Nombre: <span style='color:black'>{body.get("name")}</span></h1>
     <h1 style='color:rgb(23,229,23)'>Correo: <span style='color:black'>{body.get("to")}</span></h1>  
     <h1 style='color:rgb(23,229,23)'>Telefono: <span style='color:black'>{body.get("tel")}</span></h1>  
     <h1 style='color:rgb(23,229,23)'>Mensaje: <span style='color:black'>{body.get("mss")}</span></h1>  
    """
    enviarEmail(["garciaesneider11@gmail.com"], "Mensaje - PQRS, Usuario", bodyEmail)
    return "ok"

def enviarEmail(to,subject,body):
    msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=to)  
    msg.html=body
    try:
        mail.send(msg) 
    except Exception as e:
        print(e)


if __name__ == '__main__':
    app.run(debug=True)

app.run(debug=True)