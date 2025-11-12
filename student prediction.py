
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from joblib import dump, load
import os
import tkinter as tk
from tkinter import messagebox


MODEL_FILE = "student_model.joblib"

if not os.path.exists(MODEL_FILE):
    print("🔧 Training new model...")

    data = {
        'Hours_Studied': [2, 3, 4, 5, 6, 1, 7, 8, 9, 10, 3, 6, 8, 4, 9],
        'Attendance': [70, 75, 80, 85, 90, 60, 95, 96, 98, 99, 78, 82, 91, 79, 97],
        'Previous_Score': [50, 55, 60, 65, 70, 40, 75, 80, 85, 90, 58, 68, 78, 62, 88],
        'Extracurricular': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        'Final_Score': [52, 58, 64, 70, 75, 45, 80, 85, 90, 95, 60, 72, 82, 66, 92]
    }

    df = pd.DataFrame(data)
    X = df[['Hours_Studied', 'Attendance', 'Previous_Score', 'Extracurricular']]
    y = df['Final_Score']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)

    dump(model, MODEL_FILE)
    print("✅ Model trained and saved as 'student_model.joblib'")
else:
    print("✅ Existing model loaded.")

model = load(MODEL_FILE)


root = tk.Tk()
root.title("🎓 Student Performance Predictor")
root.geometry("420x380")
root.configure(bg="#e6f2ff")

title_label = tk.Label(root, text="Student Performance Predictor",
                       font=("Arial", 14, "bold"), bg="#e6f2ff", fg="#003366")
title_label.pack(pady=15)


def create_label_entry(text):
    tk.Label(root, text=text, bg="#e6f2ff", font=("Arial", 11)).pack()
    entry = tk.Entry(root, font=("Arial", 11))
    entry.pack(pady=3)
    return entry

entry_hours = create_label_entry("📘 Hours Studied:")
entry_attendance = create_label_entry("📊 Attendance (%):")
entry_previous = create_label_entry("📚 Previous Score:")
entry_extra = create_label_entry("🎭 Extracurricular (1=Yes, 0=No):")


def predict_performance():
    try:
        h = float(entry_hours.get())
        a = float(entry_attendance.get())
        p = float(entry_previous.get())
        e = int(entry_extra.get())

        pred = model.predict([[h, a, p, e]])[0]

        # Classify performance level
        if pred < 60:
            level = "Beginner 🤓"
        elif pred < 80:
            level = "Intermediate 💪"
        else:
            level = "Advanced 🚀"

        messagebox.showinfo("Prediction Result",
                            f"🎯 Predicted Final Score: {pred:.2f}\n📊 Performance Level: {level}")
    except Exception as ex:
        messagebox.showerror("Error", f"⚠️ Invalid Input!\n\n{ex}")


predict_btn = tk.Button(root, text="Predict Performance", command=predict_performance,
                        bg="#66cc66", fg="black", font=("Arial", 12, "bold"),
                        relief="raised", padx=10, pady=5)
predict_btn.pack(pady=20)

footer = tk.Label(root, text="Developed by Vishal kr 💡", bg="#e6f2ff", fg="#555",
                  font=("Arial", 10, "italic"))
footer.pack(side="bottom", pady=10)

root.mainloop()
