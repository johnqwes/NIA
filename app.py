from flask import Flask, render_template, request, redirect, abort, session, url_for, flash
from models import db, ProjectModel
from sqlalchemy import or_
import pyrebase
from firebase_admin import auth

app = Flask(__name__)

firebaseConfig = {
    'apiKey': "AIzaSyAF25avieiXm9XIZezYaL1JCEAux0-Gl1w",
    'authDomain': "nia-mis.firebaseapp.com",
    'projectId': "nia-mis",
    'storageBucket': "nia-mis.appspot.com",
    'messagingSenderId': "333239771011",
    'appId': "1:333239771011:web:51f1310ff4894b6cc0e0b6",
    'measurementId': "G-SND6D820B7",
    'databaseURL': ''
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Configure Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "123123"

# Initialize SQLAlchemy
db.init_app(app)

# Create database tables before first request
@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = email
            return redirect(url_for('index'))
        except auth.AuthError as e:
            error_message = e.message
            if error_message == 'INVALID_EMAIL':
                flash("Invalid email address", "danger")
            elif error_message == 'INVALID_PASSWORD':
                flash("Incorrect password", "danger")
            elif error_message == 'USER_NOT_FOUND':
                flash("User not found", "danger")
            else:
                flash("Login failed. Please try again later.", "danger")
                flash(str(e), "danger")  # Display the actual error message in the notification
                print("Error:", e)  # Print the actual error for debugging
        return render_template('login.html')
    else:
        if 'user' in session:
            data = ProjectModel.query.all()
            return render_template('index.html', data=data)
        else:
            return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name_of_cis = request.form['name_of_cis']
        location = request.form['location']
        # Add other form fields here...

        data = ProjectModel(
            name_of_cis=name_of_cis,
            location=location,
            # Assign other form values to corresponding model attributes...
        )
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/<int:id>/edit', methods=['GET', 'POST'])
def update(id):
    data = ProjectModel.query.get(id)
    if request.method == 'POST':
        if data:
            data.name_of_cis = request.form['name_of_cis']
            data.location = request.form['location']
            # Update other model attributes...
            db.session.commit()
            return redirect(url_for('index'))
        else:
            return f"Data with id = {id} does not exist"
    return render_template('update.html', data=data)

@app.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete(id):
    data = ProjectModel.query.get(id)
    if request.method == 'POST':
        if data:
            db.session.delete(data)
            db.session.commit()
            return redirect(url_for('index'))
        abort(404)
    return render_template('delete.html', data=data)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if not query:
        return redirect(url_for('index'))
    else:
        data = ProjectModel.query.filter(or_(
            ProjectModel.name_of_cis.ilike(f'%{query}%'),
            ProjectModel.location.ilike(f'%{query}%'),
            # Add other fields for searching...
        )).all()
        return render_template('index.html', data=data)

if __name__ == "__main__":
    app.run(host='localhost', port=5000)