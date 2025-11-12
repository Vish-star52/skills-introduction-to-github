import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import json
import os

FILE_NAME = "shop_data.json"

# Create data file if not present
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, "w") as f:
        json.dump([], f)

def load_data():
    with open(FILE_NAME, "r") as f:
        return json.load(f)

def save_data(data):
    with open(FILE_NAME, "w") as f:
        json.dump(data, f, indent=4)

# ---------- MAIN WINDOW ----------
root = tk.Tk()
root.title("🏪 Shop Management System")
root.geometry("800x600")
root.config(bg="#f2f2f2")

# ---------- TITLE ----------
title_label = tk.Label(root, text="SHOP MANAGEMENT SYSTEM", font=("Arial", 22, "bold"), bg="#f2f2f2", fg="#2b2b2b")
title_label.pack(pady=10)

# ---------- IMAGE ----------
try:
    img = Image.open("shop.png")  # optional image file
    img = img.resize((120, 120))
    photo = ImageTk.PhotoImage(img)
    img_label = tk.Label(root, image=photo, bg="#f2f2f2")
    img_label.pack(pady=5)
except:
    pass

# ---------- TABLE FRAME ----------
tree_frame = tk.Frame(root)
tree_frame.pack(pady=10)

columns = ("ID", "Name", "Price", "Qty")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)
tree.pack()

def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    data = load_data()
    for p in data:
        tree.insert("", tk.END, values=(p['id'], p['name'], p['price'], p['qty']))

refresh_table()

# ---------- FUNCTIONS ----------
def add_product_window():
    win = tk.Toplevel(root)
    win.title("Add Product")
    win.geometry("400x300")

    tk.Label(win, text="Product ID:").pack()
    pid = tk.Entry(win)
    pid.pack()

    tk.Label(win, text="Name:").pack()
    name = tk.Entry(win)
    name.pack()

    tk.Label(win, text="Price:").pack()
    price = tk.Entry(win)
    price.pack()

    tk.Label(win, text="Quantity:").pack()
    qty = tk.Entry(win)
    qty.pack()

    def save_product():
        data = load_data()
        new_product = {
            "id": pid.get(),
            "name": name.get(),
            "price": float(price.get()),
            "qty": int(qty.get())
        }
        data.append(new_product)
        save_data(data)
        refresh_table()
        messagebox.showinfo("Success", "Product added successfully!")
        win.destroy()

    tk.Button(win, text="Add Product", command=save_product, bg="green", fg="white").pack(pady=10)

def delete_product():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Error", "Select a product to delete!")
        return
    pid = tree.item(selected[0])["values"][0]
    data = load_data()
    data = [p for p in data if p['id'] != pid]
    save_data(data)
    refresh_table()
    messagebox.showinfo("Deleted", "Product deleted successfully!")

def billing_window():
    win = tk.Toplevel(root)
    win.title("Billing System")
    win.geometry("400x400")

    tk.Label(win, text="Enter Product ID:").pack()
    pid = tk.Entry(win)
    pid.pack()

    tk.Label(win, text="Quantity:").pack()
    qty = tk.Entry(win)
    qty.pack()

    bill_area = tk.Text(win, width=45, height=15)
    bill_area.pack(pady=10)

    def add_to_bill():
        data = load_data()
        total = 0
        for product in data:
            if product['id'] == pid.get():
                q = int(qty.get())
                if q <= product['qty']:
                    cost = product['price'] * q
                    product['qty'] -= q
                    save_data(data)
                    refresh_table()
                    bill_area.insert(tk.END, f"{product['name']} x{q} = ₹{cost}\n")
                    total += cost
                else:
                    messagebox.showwarning("Error", "Not enough stock!")
                break
        else:
            messagebox.showerror("Error", "Product not found!")

        bill_area.insert(tk.END, f"Total: ₹{total}\n")

    tk.Button(win, text="Add to Bill", command=add_to_bill, bg="blue", fg="white").pack(pady=5)
    tk.Button(win, text="Close", command=win.destroy, bg="red", fg="white").pack()

# ---------- BUTTONS ----------
btn_frame = tk.Frame(root, bg="#f2f2f2")
btn_frame.pack(pady=20)

tk.Button(btn_frame, text="Add Product", width=15, command=add_product_window, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Delete Product", width=15, command=delete_product, bg="#f44336", fg="white").grid(row=0, column=1, padx=10)
tk.Button(btn_frame, text="Billing", width=15, command=billing_window, bg="#2196F3", fg="white").grid(row=0, column=2, padx=10)
tk.Button(btn_frame, text="Refresh", width=15, command=refresh_table, bg="#FF9800", fg="white").grid(row=0, column=3, padx=10)

# ---------- RUN ----------
refresh_table()
root.mainloop()
