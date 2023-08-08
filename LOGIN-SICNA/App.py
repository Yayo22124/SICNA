#ARCHIVO INICIAL DE NUESTRO SERVIDOR  
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

#MYSQL CONECTION
app = Flask(__name__)#CREANDO LA CONEXION A LA BASE DE DATOS MYSQL
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '112020a'
app.config['MYSQL_DB'] = 'bd_sicna_joan'
mysql = MySQL(app)

#INICIO DE SESION
#SETTINGS
app.secret_key = 'mysecretkey' #COMO VA A IR PROTEGIDA NUESTRA SESION

@app.route('/')#inicializado el objeto
#INICIALIZAR EL SERVIDOR
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM tbb_prueba_python')
    data = cur.fetchall()    
    return render_template('index.html', contacts = data) #HACEMOS QUE CUANDO ENTRE LO REDIRECCIONE A UNA PAGINA HTML

@app.route('/add_contact', methods=['POST']) #A;ADIMOS EL ADD CONTACT CON EL METODO POST
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        numero = request.form['numero']
        correo = request.form['correo']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO tbb_prueba_python (Nombre, Telefono, correo) VALUES (%s, %s, %s)',(fullname, numero,correo))  
        mysql.connection.commit()
        flash('CONTACTO AGREDADO SATISFACTORIAMENTE')
        return redirect(url_for('index'))

@app.route('/edit/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM tbb_prueba_python WHERE id = %s',(id))
    data = cur.fetchall()
    return render_template('edit.html', contact = data[0])


@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        telefono = request.form['numero']
        correo = request.form['correo']
        cur = mysql.connection.cursor()
        cur.execute(""" 
            UPDATE tbb_prueba_python
            SET Nombre = %s,
                Telefono = %s,
                correo = %s
            WHERE id = %s            
        """, (fullname,telefono,correo,id))
        mysql.connection.commit()
        flash('CONTACTO ACTUALIZADO SATISFACTORIAMENTE')
        return redirect(url_for('index')) 
        

@app.route('/delete/<id>') #.CADA VEZ QUE RECIBA UNA RUTA DELETE VA A TENER AL LADO UN NUMERO PARA PODER ELIMINARLO
def deletecontact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM tbb_prueba_python WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('CONTACTO REMOVIDO SATISFACTORIAMENTE')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=3000, debug=True) #SI NOS ENCONTRAMOS EN EL MAIN QUE INICIALIZE EL PUERTO

