from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'iglesia'

mysql = MySQL(app)
app.secret_key = 'mysecretkey'
@app.route ('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM miembro')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', contacts = data)
    
@app.route ('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
      nombre = request.form['nombre']
      apellido = request.form['apellido']
      telefono = request.form['telefono']
      comunidad = request.form['comunidad']
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO miembro (nombre, apellido, telefono, comunidad) VALUES (%s, %s, %s, %s)',
    (nombre, apellido, telefono, comunidad))
    mysql.connection.commit()
    flash('Miembro agregado')


    return redirect(url_for('Index'))
@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM miembro WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-contact.html', contact = data[0])


@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        comunidad = request.form['comunidad']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE miembro
            SET nombre = %s,
                apellido = %s,
                telefono = %s,
                comunidad = %s
            WHERE id = %s
        """, (nombre, apellido, telefono,comunidad, id))
        flash('miembro modificado')
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM miembro WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('miembro eliminado')
    return redirect(url_for('Index'))

@app.route ('/comunidad', methods=['POST'])
def add_comunidad():
    if request.method == 'POST':
      nombre = request.form['nombre']
      actividad = request.form['actividad']

    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO comunidad (nombre, actividad) VALUES (%s, %s)',
    (nombre, actividad))
    mysql.connection.commit()
    flash('comunidad agregado')

if __name__ == '__main__':
    app.run(port = 3000, debug = True)

