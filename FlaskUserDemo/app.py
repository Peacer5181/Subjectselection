import pymysql, uuid, os, hashlib, random
from flask import Flask, render_template, request, redirect, url_for, session, abort, flash, jsonify
app = Flask(__name__)

# Register the setup page and import create_connection()
from utils import create_connection, setup
app.register_blueprint(setup)

def create_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='Khangcanthi18105',
        db='xuanguyen_subjectselection',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
@app.before_request
def restrict():
    restricted_pages = [
        'list_users',
        'add_user',
        'update_user',
        'add_subject',
        'update_subject',
        'delete_user',
        'delete_subject',
        'choose',
        'unchoose',
        'subject_chosen'
    ]
    if 'logged_in' not in session and request.endpoint in restricted_pages:
        return redirect('/login')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        password = request.form['password']
        encrypted_password = hashlib.sha256(password.encode()).hexdigest()
        with create_connection() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM students WHERE email=%s AND password=%s"
                values = (
                    request.form['email'],
                    encrypted_password
                )
                cursor.execute(sql, values)
                result = cursor.fetchone()
        if result:
            session['logged_in'] = True
            session['first_name'] = result['First_name']
            session['role']=result['Role']
            session['id'] = result['id']
            return redirect("/")
        else:
            error_message=('invalid username or password','hello','hey look')
            flash(error_message[random.randint(0,2)])
            return redirect("/login")
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# TODO: Add a '/register' (add_user) route that uses INSERT
@app.route('/add_user', methods=['GET','POST'])
def add_user():
    if request.method == 'POST' :
        password = request.form['password']
        encrypted_password = hashlib.sha256(password.encode()).hexdigest()
        with create_connection() as connection:
            with connection.cursor() as cursor:
                try :
                    cursor.execute("INSERT INTO students (First_name, Last_name, Date_of_birth, Year_level, Email, Password ) VALUES (%s,%s,%s,%s,%s,%s)",
                                   (request.form['first_name'],
                                    request.form['last_name'],
                                    request.form['date_of_birth'],
                                    request.form['year_level'],
                                    request.form['email'],
                                    encrypted_password))                                       
                    connection.commit()
                except pymysql.err.IntegrityError:
                    flash('Email already exist')
                    return redirect('/add_user')
                sql = "SELECT * FROM students WHERE Email=%s AND Password=%s"
                values = (
                    request.form['email'],
                    encrypted_password
                )               
                cursor.execute(sql, values)
                result = cursor.fetchone()               
        if result:
            session['logged_in'] = True
            session['first_name'] = result['First_name']
            session['role']=result['Role']
            session['id'] = result['id']
        return redirect('/')
    else :
        return render_template('add_user.html')

@app.route('/add_subject', methods=['GET','POST'])
def add_subject():
    if request.method == 'POST' :
        with create_connection() as connection:
            with connection.cursor() as cursor:
                try :
                    cursor.execute("INSERT INTO subjects ( Subject, Description) VALUES (%s,%s)",
                                    (request.form['subject'],
                                    request.form['description'],
                                    ))                                       
                    connection.commit()
                except pymysql.err.IntegrityError:
                    flash('Subject already exist')
                    return redirect('/add_subject')
        return redirect('/')
    else :
        return render_template('add_subject.html')

# TODO: Add a '/dashboard' (list_users) route that uses SELECT
@app.route('/list_users')
def list_users():
    with create_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM students" )
            result = cursor.fetchall()
    return render_template('list_users.html',data=result)

## TODO: Add a '/profile' (view_user) route that uses SELECT
#@app.route('/view')
#def view_user():
#    with create_connection() as connection:
#        with connection.cursor() as cursor:
#            cursor.execute("SELECT * FROM users WHERE id=%s", request.args['id'])
#            result = cursor.fetchone()
#    return render_template('users_view.html', result=result)

# TODO: Add a '/delete_user' route that uses DELETE
@app.route('/delete_user')
def delete_user():
    #if session['role'] != 'admin':
    #    error_message=("You don't have the power",'cmon',"you wouldn't dare")
    #    flash(error_message[random.randint(0,2)])
    #    return redirect('/')
    with create_connection() as connection:
        with connection.cursor() as cursor:
            sql = """DELETE FROM students WHERE id = %s"""
            values = (request.args['id'])
            cursor.execute(sql, values)
            connection.commit()
    return redirect('/list_users')

# TODO: Add a '/delete_subject' route that uses DELETE
@app.route('/delete_subject')
def delete_subject():
    with create_connection() as connection:
        with connection.cursor() as cursor:
            sql = """DELETE FROM subjects WHERE id = %s"""
            values = (request.args['id'])
            cursor.execute(sql, values)
            connection.commit()
    return redirect('/list_subjects')
#@app.route('/unwatch')
#def unwatch():        
#    with create_connection() as connection:
#        with connection.cursor() as cursor:
#            sql = """DELETE FROM user_movie WHERE id = %s"""
#            values = (request.args['id'])
#            cursor.execute(sql, values)
#            connection.commit()
#    return redirect('/')
@app.route('/subject_chosen')
def subject_chosen():
    with create_connection() as connection:
        with connection.cursor() as cursor:
            sql = """Select * FROM students 
                    JOIN student_subject ON student_subject.student_id = students.id
                    JOIN subjects ON subjects.id = student_subject.subject_id
                    WHERE students.id = %s"""
            #if session['role'] != 'admin':
            #    values = session['id']
            #else :
            #    if 'id' in request.args:
            values = request.args['id']
                #else:
                #    values = session['id']
            cursor.execute(sql,values)
            result = cursor.fetchall()
            print(result)
    return render_template('subject_chosen.html', result=result)

# TODO: Add a '/update_subject' route that uses UPDATE
@app.route('/update_subject', methods=['GET', 'POST'])
def update_subject():
    if request.method == 'POST':
        with create_connection() as connection:
            with connection.cursor() as cursor:
                sql = """UPDATE subjects SET 
                        Subject = %s,
                        Description = %s
                        WHERE id = %s"""
                values = (
                    request.form['subject'],
                    request.form['description'],
                    request.form['id'])
                cursor.execute(sql, values)
                connection.commit()
        return redirect('/list_subjects')
    else:
        with create_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM subjects WHERE id = %s", request.args['id'])
                result = cursor.fetchone()
        return render_template('update_subject.html', result=result)

# TODO: Add an '/edit_user' route that uses UPDATE
@app.route('/update_user', methods=['GET', 'POST'])
def update_user():
    #if session['role'] != 'admin' and str(session['id']) != request.args['id']:
    #    flash("you don't have the permission to edit this user")
    #    return redirect('/view?id=' + request.args['id'])
    if request.method == 'POST':
        
        #if request.files['avatar'].filename:
        #    avatar_image = request.files["avatar"]
        #    ext = os.path.splitext(avatar_image.filename)[1]
        #    avatar_filename = str(uuid.uuid4())[:8] + ext
        #    avatar_image.save("static/images/" + avatar_filename)
        #    if request.form['old_avatar'] != 'None' and os.path.exists("static/iamges/" + request.form['old_avatar']):
        #        os.remove("static/images/" + request.form['old_avatar'])
        #elif request.form['old_avatar'] != 'None' :
        #    avatar_filename = request.form['old_avatar']
        #else:
        #    avatar_filename = None

        with create_connection() as connection:
            with connection.cursor() as cursor:
                if request.form['password']:
                    password = request.form['password']
                    encrypted_password = hashlib.sha256(password.encode()).hexdigest()               
                    sql = """UPDATE students SET
                        First_name = %s,
                        Last_name = %s,             
                        Date_of_birth = %s,
                        Year_level = %s,
                        Email = %s,
                        Password = %s
                        WHERE id = %s"""
                    values = (
                        request.form['first_name'],
                        request.form['last_name'],
                        request.form['date_of_birth'],
                        request.form['year_level'],
                        request.form['email'],
                        encrypted_password,
                        request.form['id'])
                    
                else:
                    sql = """UPDATE students SET
                        First_name = %s,
                        Last_name = %s,
                        Date_of_birth = %s,
                        Year_level = %s,
                        Email = %s
                        WHERE id = %s"""
                    values = (
                        request.form['first_name'],
                        request.form['last_name'],
                        request.form['date_of_birth'],
                        request.form['year_level'],
                        request.form['email'],                       
                        request.form['id'])
                cursor.execute(sql, values)
                connection.commit()
        return redirect('/list_users')
    else:
        with create_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM students WHERE id = %s", request.args['id'])
                result = cursor.fetchone()
        return render_template('update_user.html', result=result)
#@app.route('/watch')
#def watch():
#    with create_connection() as connection:
#        with connection.cursor() as cursor:                
#            cursor.execute("INSERT INTO user_movie (user_id,movie_id) VALUES (%s,%s)",
#                            (session['id'],request.args['id']))   
#            connection.commit()               
#    return redirect('/movie_watched')
@app.route('/list_subjects')
def list_subjects():
    with create_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT * FROM subjects""" )
            result = cursor.fetchall()
    return render_template('list_subjects.html',data=result)
@app.route('/checkemail')
def check_email():
    with create_connection() as connection:
        with connection.cursor() as cursor:
            sql = "select * from users where email=%s "
            values = (
                request.args['email']
            )
            cursor.execute(sql, values)
            result = cursor.fetchone()
    if result:
        return jsonify({ 'status': 'error'})
    else :
        return jsonify({ 'status': 'ok'})
if __name__ == '__main__':
    import os

    # This is required to allow flashing messages. We will cover this later.
    app.secret_key = os.urandom(32)

    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug=True)
