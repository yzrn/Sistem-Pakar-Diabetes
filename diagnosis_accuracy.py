def expert_diagnosis(symptoms):
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

test_data = [
    # Format: ([symptoms], expected_result)
    ([1,1,0,0,0,1,0,1,0,0,0], "Berisiko diabetes."),    
    ([0,1,0,0,0,0,0,0,0,0,0], "Tidak berisiko diabetes."),    
    ([0,0,0,1,1,1,1,1,0,0,0], "Berisiko diabetes."),    
    ([1,0,0,0,0,0,0,0,0,0,0], "Tidak berisiko diabetes."),
    ([1,0,0,0,0,0,1,1,1,0,0], "Tidak berisiko diabetes."),
    ([1,0,1,1,0,1,0,0,0,0,0], "Berisiko diabetes."),    
    ([0,1,1,1,1,1,1,0,0,0,0], "Berisiko diabetes."),
    ([0,0,0,1,0,0,0,0,0,0,0], "Tidak berisiko diabetes."),
    ([1,0,1,0,0,0,0,0,0,0,0], "Berisiko diabetes."),
    ([1,0,0,0,0,0,0,0,0,0,0], "Tidak berisiko diabetes."),
    ([0,0,0,0,0,0,0,0,1,1,1], "Tidak berisiko diabetes."),
    ([1,0,0,0,0,0,0,0,0,0,1], "Tidak berisiko diabetes."),
    ([0,0,0,1,1,0,0,0,0,0,1], "Tidak berisiko diabetes."),
    ([1,1,0,0,0,0,0,1,1,0,0], "Tidak berisiko diabetes."),
    ([1,1,1,0,0,0,0,1,1,0,0], "Berisiko diabetes."),    
    ([0,0,1,0,0,1,0,0,0,0,1], "Tidak berisiko diabetes."),    
    ([0,0,1,1,0,0,0,0,0,0,0], "Tidak berisiko diabetes."),    
    ([1,1,0,0,0,0,1,1,0,0,0], "Tidak berisiko diabetes."),    
    ([1,1,0,1,0,0,0,1,0,0,0], "Berisiko diabetes."),    
    ([1,1,0,1,0,0,0,1,0,0,0], "Berisiko diabetes."),
    ([1,1,0,1,0,0,0,1,0,0,0], "Berisiko diabetes."),
    ([1,1,1,1,0,0,0,0,0,0,0], "Berisiko diabetes."),    
    ([1,0,0,0,0,0,0,0,0,0,0], "Tidak berisiko diabetes."),
    ([0,1,1,0,0,0,0,0,0,0,0], "Tidak berisiko diabetes."),    
    ([1,1,1,1,0,0,0,0,0,0,0], "Berisiko diabetes."),
    ([0,1,0,0,0,0,0,0,0,0,0], "Tidak berisiko diabetes."),
    ([1,1,0,0,0,0,0,0,0,0,0], "Tidak berisiko diabetes."),
    ([1,1,1,0,0,0,0,0,0,0,0], "Berisiko diabetes."),    
    ([1,1,1,1,0,0,0,0,0,0,0], "Berisiko diabetes."),    
    ([1,0,0,1,0,0,0,0,0,0,0], "Tidak berisiko diabetes."),
    ([1,1,1,0,0,0,0,0,0,0,0], "Berisiko diabetes."),
    ([0,1,1,0,0,0,0,0,0,0,0], "Tidak berisiko diabetes."),
    ([1,1,0,0,0,0,0,0,0,0,0], "Tidak berisiko diabetes."),
    ([1,1,0,0,0,0,0,0,0,0,0], "Tidak berisiko diabetes."),    
    ([0,1,1,1,0,0,0,0,0,0,0], "Tidak berisiko diabetes."),
    ([1,1,1,0,0,0,0,0,0,0,0], "Berisiko diabetes."),    
    ([0,1,1,0,0,0,0,1,0,0,0], "Tidak berisiko diabetes."),    
    ([0,1,1,1,0,0,0,0,0,0,0], "Tidak berisiko diabetes."),
    ([0,1,1,1,1,1,0,0,0,0,0], "Berisiko diabetes."),    
    ([1,1,1,0,0,0,0,0,0,0,0], "Berisiko diabetes."),    
    ([1,0,0,0,0,0,0,0,0,0,0], "Tidak berisiko diabetes."),
    ([0,1,0,1,0,1,1,0,0,1,0], "Berisiko diabetes."),	
    ([0,1,1,1,1,0,0,0,0,0,0], "Berisiko diabetes."),	
    ([1,1,1,0,1,0,0,0,0,0,0], "Berisiko diabetes."),	
    ([1,0,0,0,1,1,0,0,0,1,1], "Tidak berisiko diabetes."),
    ([1,0,1,1,0,0,0,0,0,0,0], "Berisiko diabetes."),
    ([1,1,1,1,0,0,0,0,0,0,0], "Berisiko diabetes."),
    ([1,1,1,1,0,0,0,0,0,0,0], "Berisiko diabetes"),
    ([0,1,0,1,1,0,0,0,0,0,0], "Tidak berisiko diabetes."),
    ([0,0,1,1,0,1,1,0,0,0,0], "Tidak berisiko diabetes."),
    ([1,0,0,0,0,0,1,1,1,1,0], "Tidak berisiko diabetes."),
    ([0,0,0,1,1,1,1,1,0,0,0], "Tidak berisiko diabetes."),
    
]

# Inisialisasi variabel untuk menghitung akurasi
correct_predictions = 0

# Loop untuk menguji semua data
for symptoms, expected_result in test_data:
    prediction = expert_diagnosis(symptoms)
    if prediction == expected_result:
        correct_predictions += 1

# Hitung akurasi
accuracy = (correct_predictions / len(test_data)) * 100
print(f"Akurasi: {accuracy}%")
