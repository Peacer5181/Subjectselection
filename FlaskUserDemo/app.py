import pymysql, uuid, os, hashlib, random
from flask import Flask, render_template, request, redirect, url_for, session, abort, flash, jsonify
app = Flask(__name__)

# Register the setup page and import create_connection()
from utils import create_connection, setup
app.register_blueprint(setup)

def create_connection():
    return pymysql.connect(
        host='10.0.0.17',
        user='xuanguyen',
        password='ARPAS',
        db='xuanguyen_subjectselection',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
#@app.before_request
#def restrict():
#    restricted_pages = [
#        'list_users',
#        'view_user',
#        'edit',
#        'delete',
#        'watch'
#    ]
#    if 'logged_in' not in session and request.endpoint in restricted_pages:
#        return redirect('/login')

@app.route('/')
def home():
    return render_template('home.html')

#@app.route('/login', methods=['GET', 'POST'])
#def login():
#    if request.method == 'POST':

#        password = request.form['password']
#        encrypted_password = hashlib.sha256(password.encode()).hexdigest()
#        with create_connection() as connection:
#            with connection.cursor() as cursor:
#                sql = "SELECT * FROM users WHERE email=%s AND password=%s"
#                values = (
#                    request.form['email'],
#                    encrypted_password
#                )
#                cursor.execute(sql, values)
#                result = cursor.fetchone()
#        if result:
#            session['logged_in'] = True
#            session['first_name'] = result['first_name']
#            session['role']=result['role']
#            session['id'] = result['id']
#            return redirect("/")
#        else:
#            error_message=('invalid username or password','hello','hey look')
#            flash(error_message[random.randint(0,2)])
#            return redirect("/login")
#    else:
#        return render_template('login.html')

#@app.route('/logout')
#def logout():
#    session.clear()
#    return redirect('/')

## TODO: Add a '/register' (add_user) route that uses INSERT
#@app.route('/register', methods=['GET','POST'])
#def register():
#    if request.method == 'POST' :
#        password = request.form['password']
#        encrypted_password = hashlib.sha256(password.encode()).hexdigest()
#        if request.files['avatar'].filename:
#            avatar_image = request.files["avatar"]
#            ext = os.path.splitext(avatar_image.filename)[1]
#            avatar_filename= str(uuid.uuid4())[:8] + ext
#            avatar_image.save("static/images/"+avatar_filename)
#        else:
#            avatar_filename = None
#        with create_connection() as connection:
#            with connection.cursor() as cursor:
#                try :
#                    cursor.execute("INSERT INTO users (first_name, last_name, email, password, avatar) VALUES (%s,%s,%s,%s,%s)",
#                                   (request.form['first_name'],
#                                    request.form['last_name'],
#                                    request.form['email'],
#                                    encrypted_password,
#                                    avatar_filename))   
#                    connection.commit()
#                except pymysql.err.IntegrityError:
#                    flash('Email already exist')
#                    return redirect('/register')
#                sql = "SELECT * FROM users WHERE email=%s AND password=%s"
#                values = (
#                    request.form['email'],
#                    encrypted_password
#                )               
#                cursor.execute(sql, values)
#                result = cursor.fetchone()               
#        if result:
#            session['logged_in'] = True
#            session['first_name'] = result['first_name']
#            session['role']=result['role']
#            session['id'] = result['id']
#        return redirect('/')
#    else :
#        return render_template('register.html')


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

## TODO: Add a '/delete_user' route that uses DELETE
#@app.route('/delete')
#def delete():
#    if session['role'] != 'admin':
#        error_message=("You don't have the power",'cmon',"you wouldn't dare")
#        flash(error_message[random.randint(0,2)])
#        return redirect('/')
#    with create_connection() as connection:
#        with connection.cursor() as cursor:
#            sql = """DELETE FROM users WHERE id = %s"""
#            values = (request.args['id'])
#            cursor.execute(sql, values)
#            connection.commit()
#    return redirect('/dashboard')
#@app.route('/unwatch')
#def unwatch():        
#    with create_connection() as connection:
#        with connection.cursor() as cursor:
#            sql = """DELETE FROM user_movie WHERE id = %s"""
#            values = (request.args['id'])
#            cursor.execute(sql, values)
#            connection.commit()
#    return redirect('/')
#@app.route('/movie_watched')
#def movie_watched():
#    with create_connection() as connection:
#        with connection.cursor() as cursor:
#            sql = """Select *,GROUP_CONCAT(genre.Genre_name) FROM users 
#                    JOIN user_movie ON user_movie.user_id = users.id
#                    JOIN movies ON movies.id = user_movie.movie_id
#                    JOIN movie_genre ON  movie_genre.movie_id = movies.id 
#                    JOIN genre ON genre.genre_id = movie_genre.genre_id
#                    WHERE users.id = %s
#                    GROUP by movies.id"""
#            if session['role'] != 'admin':
#                values = session['id']
#            else :
#                if 'id' in request.args:
#                    values = request.args['id']
#                else:
#                    values = session['id']
#            cursor.execute(sql,values)
#            result = cursor.fetchall()
#            print(result)
#    return render_template('movie_watched.html', result=result)
## TODO: Add an '/edit_user' route that uses UPDATE
#@app.route('/edit', methods=['GET', 'POST'])
#def edit():
#    if session['role'] != 'admin' and str(session['id']) != request.args['id']:
#        flash("you don't have the permission to edit this user")
#        return redirect('/view?id=' + request.args['id'])
#    if request.method == 'POST':
        
#        if request.files['avatar'].filename:
#            avatar_image = request.files["avatar"]
#            ext = os.path.splitext(avatar_image.filename)[1]
#            avatar_filename = str(uuid.uuid4())[:8] + ext
#            avatar_image.save("static/images/" + avatar_filename)
#            if request.form['old_avatar'] != 'None' and os.path.exists("static/iamges/" + request.form['old_avatar']):
#                os.remove("static/images/" + request.form['old_avatar'])
#        elif request.form['old_avatar'] != 'None' :
#            avatar_filename = request.form['old_avatar']
#        else:
#            avatar_filename = None

#        with create_connection() as connection:
#            with connection.cursor() as cursor:
#                if request.form['password']:
#                    password = request.form['password']
#                    encrypted_password = hashlib.sha256(password.encode()).hexdigest()               
#                    sql = """UPDATE users SET
#                        first_name = %s,
#                        last_name = %s,
#                        email = %s,
#                        password = %s,
#                        avatar = %s
#                        WHERE id = %s"""
#                    values = (
#                        request.form['first_name'],
#                        request.form['last_name'],
#                        request.form['email'],
#                        encrypted_password,
#                        avatar_filename,
#                        request.form['id']
#                    )
#                else:
#                    sql = """UPDATE users SET
#                        first_name = %s,
#                        last_name = %s,
#                        email = %s,
#                        avatar = %s
#                        WHERE id = %s"""
#                    values = (
#                        request.form['first_name'],
#                        request.form['last_name'],
#                        request.form['email'],
#                        avatar_filename,
#                        request.form['id'])
#                cursor.execute(sql, values)
#                connection.commit()
#        return redirect('/view?id=' + request.form['id'])
#    else:
#        with create_connection() as connection:
#            with connection.cursor() as cursor:
#                cursor.execute("SELECT * FROM users WHERE id = %s", request.args['id'])
#                result = cursor.fetchone()
#        return render_template('edit.html', result=result)
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
#@app.route('/checkemail')
#def check_email():
#    with create_connection() as connection:
#        with connection.cursor() as cursor:
#            sql = "SELECT * FROM users WHERE email=%s "
#            values = (
#                request.args['email']
#            )
#            cursor.execute(sql, values)
#            result = cursor.fetchone()
#    if result:
#        return jsonify({ 'status': 'Error'})
#    else :
#        return jsonify({ 'status': 'OK'})
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
