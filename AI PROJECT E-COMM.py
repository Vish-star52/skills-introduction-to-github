
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import tkinter as tk
from tkinter import ttk, messagebox


data = pd.DataFrame({
    "product_name": [
        "Apple iPhone 14", "Samsung Galaxy S23", "OnePlus 11",
        "Sony Headphones WH-1000XM5", "Boat Bluetooth Speaker",
        "Apple MacBook Air", "Dell XPS 13 Laptop", "HP Pavilion Laptop",
        "Canon DSLR Camera", "Nikon Mirrorless Camera"
    ],
    "description": [
        "Latest iPhone with A16 Bionic chip and great camera performance",
        "High-end Android smartphone with powerful Snapdragon processor",
        "Flagship killer smartphone with great performance and battery life",
        "Noise cancelling headphones with premium sound quality",
        "Portable wireless Bluetooth speaker with deep bass",
        "M2-powered laptop with slim design and long battery life",
        "Premium ultrabook with InfinityEdge display and sleek design",
        "Reliable laptop for students with i5 processor and 8GB RAM",
        "Professional DSLR camera with 24MP sensor and optical zoom",
        "Mirrorless camera with 4K video and fast autofocus"
    ],
    "category": [
        "Smartphone", "Smartphone", "Smartphone",
        "Audio", "Audio", "Laptop", "Laptop",
        "Laptop", "Camera", "Camera"
    ]
})


data["text"] = data["product_name"] + " " + data["description"] + " " + data["category"]

vectorizer = TfidfVectorizer(stop_words='english')
feature_matrix = vectorizer.fit_transform(data["text"])

similarity = cosine_similarity(feature_matrix)

def recommend(product_name):
    if product_name not in data["product_name"].values:
        return ["⚠️ Product not found!"]
    
    idx = data[data["product_name"] == product_name].index[0]
    scores = list(enumerate(similarity[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    top_5 = scores[1:6]
    recs = [data.iloc[i[0]]["product_name"] for i in top_5]
    return recs


root = tk.Tk()
root.title("🛒 E-Commerce Personalized Recommendation System")
root.geometry("600x450")
root.resizable(False, False)
root.configure(bg="#969496")

# Title Label
title_label = tk.Label(root, text="E-Commerce Personalized Recommendation System",
                       font=("Arial", 14, "bold"), bg="#00ff11", fg="#2c3e50")
title_label.pack(pady=20)

# Product Selection
label = tk.Label(root, text="Select a Product:", font=("Arial", 12), bg="#000000")
label.pack()

selected_product = tk.StringVar()
combo = ttk.Combobox(root, textvariable=selected_product, width=50, font=("Arial", 11))
combo['values'] = list(data["product_name"])
combo.pack(pady=10)

# Output Text Box
output_box = tk.Text(root, width=70, height=10, font=("Arial", 11), wrap="word", bg="#213b4a")
output_box.pack(pady=10)

# Function to display recommendations
def show_recommendations():
    product = selected_product.get().strip()
    if not product:
        messagebox.showwarning("Input Error", "Please select a product first!")
        return
    recs = recommend(product)
    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, f"Top Recommendations for '{product}':\n\n")
    for r in recs:
        output_box.insert(tk.END, f"👉 {r}\n")

# Recommend Button
btn = tk.Button(root, text="🔍 Get Recommendations", command=show_recommendations,
                bg="#00ff00", fg="green", font=("Arial", 15, "bold"), width=30, height=2)
btn.pack(pady=15)

# Exit Button
exit_btn = tk.Button(root, text="❌ Exit", command=root.destroy,
                     bg="#e74c3c", fg="red", font=("Arial", 11, "bold"), width=15)
exit_btn.pack(pady=5)

# Run the GUI Loop
root.mainloop()
