import numpy as np
from sklearn import svm


# Data ini seharusnya diganti dengan data nyata
# Fitur: umur, jenis kelamin (0: perempuan, 1: laki-laki), dan 11 gejala (0: tidak, 1: ya)
X = np.array([
    [25, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1],
    [30, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0],
    [45, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
    [35, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0],
    # Tambahkan lebih banyak data latih di sini
])

# Label: 0 (tidak ada penyakit), 1 (ada penyakit)
y = np.array([1, 0, 1, 0])

# Buat model SVM
model = svm.SVC(probability=True)
model.fit(X, y)

def predict(age, gender, symptoms):
    # Ubah gender menjadi format numerik
    gender_numeric = 1 if gender == 'male' else 0
    
    # Gabungkan fitur input
    features = [age, gender_numeric] + symptoms
    
    # Prediksi menggunakan model SVM
    prediction = model.predict([features])
    return prediction

if __name__ == "__main__":
    age = 40
    gender = 'male'
    symptoms = [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1]
    result = predict(age, gender, symptoms)
    print("Hasil prediksi SVM:", "Penyakit terdeteksi" if result[0] == 1 else "Tidak ada penyakit")
