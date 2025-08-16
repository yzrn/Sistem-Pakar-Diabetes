from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from flask import Flask, jsonify

app = Flask(__name__)
app.secret_key = 'supersecretkey'  

# Konfigurasi basis data SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inisialisasi basis data
db = SQLAlchemy(app)

# Definisikan model User
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Definisikan model History
class History(db.Model):
    __tablename__ = 'history'
    name = db.Column(db.String, primary_key=True)
    ktp = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String)
    symptoms = db.Column(db.Text)
    diagnosis_result = db.Column(db.String)  

    user = db.relationship('User', backref=db.backref('histories', lazy=True))

class Symptom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)


# Load model yang disimpan
model = pickle.load(open('model/diabetes_model.sav', 'rb'))

# Load and fit the scaler
diabetes_dataset = pd.read_csv('diabetes.csv')
X = diabetes_dataset.drop(columns='Outcome', axis=1)
scaler = StandardScaler()
scaler.fit(X)

# Inisialisasi basis data sebelum permintaan pertama
@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

users = {
    'admin': {'password': 'adminpass', 'role': 'admin'},
    'user': {'password': 'userpass', 'role': 'user'}
}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and users[username]['password'] == password:
            session['username'] = username
            session['role'] = users[username]['role']
            
            if users[username]['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            flash('Login failed. Check your username and password.', 'danger')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')
        
        if User.query.filter_by(username=username).first():
            flash('Username sudah ada')
        else:
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registrasi berhasil! Silakan login.')
            return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'role' in session and session['role'] == 'admin':
        return render_template('admin_dashboard.html')
    else:
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('login'))

@app.route('/user_dashboard')
def user_dashboard():
    if 'role' in session and session['role'] == 'user':
        return render_template('user_dashboard.html')
    else:
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('login'))


@app.route('/diagnose', methods=['GET', 'POST'])
def diagnose():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    user_id = session.get('user_id')
    if request.method == 'POST':
        try:
            name = request.form['name']
            ktp = user_id  # Menggunakan ID pengguna saat ini
            age = int(request.form['age'])
            gender = request.form['gender']
            symptoms = [
                int(request.form.get('symptom1', 0)),
                int(request.form.get('symptom2', 0)),
                int(request.form.get('symptom3', 0)),
                int(request.form.get('symptom4', 0)),
                int(request.form.get('symptom5', 0)),
                int(request.form.get('symptom6', 0)),
                int(request.form.get('symptom7', 0)),
                int(request.form.get('symptom8', 0)),
                int(request.form.get('symptom9', 0)),
                int(request.form.get('symptom10', 0)),
                int(request.form.get('symptom11', 0))
            ]
            
            symptoms_str = ','.join(map(str, symptoms))  # Mengubah daftar gejala menjadi string

            # Diagnosa menggunakan aturan pakar
            diagnosis_result = expert_diagnosis(symptoms)

            # Simpan hasil dalam riwayat pengguna
            if user_id:
                new_history = History(
                    name=name,
                    ktp=ktp,
                    age=age,
                    gender=gender,
                    symptoms=symptoms_str,
                    diagnosis_result=diagnosis_result  # Menyimpan hasil diagnosa
                )
                db.session.add(new_history)
                db.session.commit()

            # Simpan hasil dalam flash message
            flash(f'Hasil Diagnosis: {diagnosis_result}')
        except Exception as e:
            flash(f'Error: {str(e)}')

    # Ambil riwayat diagnosis pengguna dari basis data
    if user_id:
        user_history = History.query.filter_by(ktp=user_id).all()
    else:
        user_history = []

    return render_template('diagnose.html', history=user_history)


def expert_diagnosis(symptoms):
    """
    Fungsi ini mendiagnosis risiko diabetes berdasarkan gejala yang diberikan.
    
    :param symptoms: Daftar gejala dalam bentuk 0 (tidak ada) atau 1 (ada).
    :return: String yang menunjukkan diagnosis.
    """
    # Misalkan gejala terdaftar sebagai berikut:
    # [Haus berlebihan, Penurunan berat badan, Kelelahan, Luka lama sembuh, Penglihatan kabur, Sering lapar, Infeksi, Kesemutan, Kulit kering, Mual, Sakit kepala]
    
    # Logika diagnosa
    if symptoms[0] == 1 and symptoms[1] == 1 and symptoms[2] == 1 and symptoms[4] == 1:
        return "Berisiko diabetes."
    elif symptoms[0] == 1 and symptoms[1] == 1 and (symptoms[2] == 1 or symptoms[3] == 1):
        return "Berisiko diabetes."
    elif (symptoms[0] == 1 or symptoms[4] == 1) and symptoms[2] == 1:
        return "Berisiko diabetes."
    elif symptoms[5] == 1 and (symptoms[6] == 1 or symptoms[7] == 1):
        return "Berisiko diabetes."
    elif symptoms[8] == 1 or symptoms[9] == 1 or symptoms[10] == 1:
        return "Tidak berisiko diabetes."
    else:
        return "Tidak berisiko diabetes."

@app.route('/leb')
def leb():
    return render_template('leb.html')

@app.route('/predict', methods=['POST'])
def predict():
    input_data = [float(x) for x in request.form.values()]
    input_data_as_numpy_array = np.array(input_data).reshape(1, -1)
    std_data = scaler.transform(input_data_as_numpy_array)
    prediction = model.predict(std_data)
    
    if prediction[0] == 0:
        result = 'Pasien tidak terkena diabetes'
    else:
        result = 'Pasien terkena diabetes'

    # Save history
    if 'user_id' in session:
        user_id = session['user_id']
        new_history = History(user_id=user_id, diagnosis_result=result)
        db.session.add(new_history)
        db.session.commit()

    return render_template('leb.html', prediction=result)

@app.route('/disease_list')
def disease_list():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    diseases = ["Diabetes"]  # Add more diseases as needed
    return render_template('daftar_gejala.html', diseases=diseases)

@app.route('/Riwayat')
def diagnosis_history():
    if 'username' not in session:
        return redirect(url_for('login'))

    user_id = session.get('user_id')
    if user_id:
        user_history = History.query.filter_by(ktp=user_id).all()
    else:
        user_history = []

    return render_template('history.html', history=user_history)

    
@app.route('/user_guide')
def user_guide():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    return render_template('user_guide.html')

@app.route('/tambah-gejala', methods=['POST'])
def tambah_gejala():
    description = request.json.get('description')
    if description:
        gejala_baru = Symptom(description=description)
        db.session.add(gejala_baru)
        db.session.commit()
        return jsonify({'status': 'success', 'gejala_id': gejala_baru.id}), 200
    return jsonify({'status': 'error'}), 400

@app.route('/hapus-gejala/<int:id>', methods=['DELETE'])
def hapus_gejala(id):
    gejala = Symptom.query.get(id)
    if gejala:
        db.session.delete(gejala)
        db.session.commit()
        return jsonify({'status': 'success'}), 200
    return jsonify({'status': 'error'}), 400

@app.route('/gejala')
def daftar_gejala():
    gejala_list = Symptom.query.all()
    return render_template('daftar_gejala.html', gejala_list=gejala_list)



if __name__ == '__main__':
    app.run(debug=True)

