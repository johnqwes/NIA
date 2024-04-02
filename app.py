from flask import Flask, render_template, request, redirect, abort, session, url_for, flash
from models import db, ProjectModel
from sqlalchemy import or_
import pyrebase
from firebase_admin import auth
from werkzeug.urls import quote


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

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Set the secret key to use sessions in Flask
app.secret_key = "123123"


firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

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
    if 'user' in session:
        session.pop('user', None)
    return redirect(url_for('index'))


    # @app.before_first_request
def create_table():
        db.create_all()

@app.before_first_request
def initialize():
        create_table()

@app.route('/create', methods=['GET', 'POST'])
def create():
        if request.method == 'GET':
            return render_template('create.html')
        
        if request.method == 'POST':
            name_of_cis = request.form['name_of_cis']
            location = request.form['location']
            source_of_water = request.form['source_of_water']
            scheme_of_irrigation = request.form['scheme_of_irrigation']
            service_area = request.form['service_area']
            firmed_up_service_area = request.form['firmed_up_service_area']
            operational_area = request.form['operational_area']
            num_farmer_beneficiaries = request.form['num_farmer_beneficiaries']
            name_of_ia = request.form['name_of_ia']
            main_canals = request.form['main_canals']
            laterals = request.form['laterals']


            data = ProjectModel(
                name_of_cis = name_of_cis,
                location=location,
                source_of_water=source_of_water,
                scheme_of_irrigation=scheme_of_irrigation,
                firmed_up_service_area=firmed_up_service_area,
                service_area=service_area,
                operational_area=operational_area,
                num_farmer_beneficiaries=num_farmer_beneficiaries,
                name_of_ia=name_of_ia,
                main_canals=main_canals,
                laterals=laterals
            )
            db.session.add(data)
            db.session.commit()
            return redirect('/')   


@app.route('/', methods=['GET'])
def RetrieveList():
    data = ProjectModel.query.all()
    return render_template('index.html', data=data)


@app.route('/<int:id>/edit', methods=['GET', 'POST'])
def update(id):
        data = ProjectModel.query.get(id)

        if request.method == 'POST':
            if data:
                data.name_of_cis = request.form['name_of_cis']
                data.location = request.form['location']
                data.source_of_water = request.form['source_of_water']
                data.scheme_of_irrigation = request.form['scheme_of_irrigation']
                data.firmed_up_service_area = request.form['firmed_up_service_area']
                data.service_area = request.form['service_area']
                data.operational_area = request.form['operational_area']
                data.num_farmer_beneficiaries = request.form['num_farmer_beneficiaries']
                data.name_of_ia = request.form['name_of_ia']
                data.main_canals = request.form['main_canals']
                data.laterals = request.form['laterals']

                db.session.commit()
                return redirect('/')
            else:
                return f"data with id = {id} does not exist"    

        return render_template('update.html', data=data)



@app.route('/<int:id>/delete', methods=['GET','POST'])
def delete(id):
        data = ProjectModel.query.filter_by(id=id).first()
        if request.method == 'POST':
            if data:
                db.session.delete(data)
                db.session.commit()
                return redirect('/')
            abort(404)
        #return redirect('/')
        return render_template('delete.html')    

@app.route('/search', methods=['GET'])
def search():
        query = request.args.get('query')
        if not query:
            return redirect('/')
        else:
            # Perform search using query
            data = ProjectModel.query.filter(or_(
                ProjectModel.name_of_cis.ilike(f'%{query}%'),
                ProjectModel.location.ilike(f'%{query}%'),
                ProjectModel.source_of_water.ilike(f'%{query}%'),
                ProjectModel.scheme_of_irrigation.ilike(f'%{query}%'),
                ProjectModel.service_area.ilike(f'%{query}%'),
                ProjectModel.firmed_up_service_area.ilike(f'%{query}%'),
                ProjectModel.operational_area.ilike(f'%{query}%'),
                ProjectModel.num_farmer_beneficiaries.ilike(f'%{query}%'),
                ProjectModel.name_of_ia.ilike(f'%{query}%'),
                ProjectModel.main_canals.ilike(f'%{query}%'),
                ProjectModel.laterals.ilike(f'%{query}%')
            )).all()

            return render_template('index.html', data=data)
        


if __name__ == "__main__":
        app.run(host='localhost', port=5000)
