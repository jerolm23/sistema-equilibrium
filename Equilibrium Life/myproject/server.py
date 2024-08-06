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


mail = Mail(app)

@app.route("/contact", methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        nombre = request.form['Name']
        email = request.form['Email']
        telefono = request.form['Phone number']
        mensaje = request.form['Message']


        msg = Message('Nuevo mensaje de contacto',
                    sender=app.config['MAIL_USERNAME'], 
                    recipients=['equilibriumlifeparati@gmail.com'])  
        msg.body = f"Nombre: {nombre}\nEmail: {email}\nTeléfono: {telefono}\nMensaje: {mensaje}"

        try:
            mail.send(msg) 
            return 'Mensaje enviado correctamente.'
        except Exception as e:
            return 'Error al enviar el mensaje: ' + str(e)

    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)

app.run(debug=True)