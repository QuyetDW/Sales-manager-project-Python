import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
import tkinter as tk

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456@Ab",
    database="btlpython"
)
c = conn.cursor()
# Initialize the main app
app = ctk.CTk()
app.title("Employee Management")
app.geometry("800x600")


# Define functions for CRUD operations
def add_employee():
    tennv = entry_name.get()
    sdt = entry_phone.get()
    email = entry_email.get()
    matkhau = entry_password.get()
    chucvu = entry_position.get()
    ngaybatdau = entry_start_date.get()
    luong = entry_salary.get()

    if not (tennv and sdt and email and matkhau and chucvu and ngaybatdau and luong):
        messagebox.showerror("Error", "All fields are required")
        return

    c.execute("INSERT INTO nhanvien (tennv, sdt, email, matkhau, chucvu, ngaybatdau, luong) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (tennv, sdt, email, matkhau, chucvu, ngaybatdau, float(luong)))
    conn.commit()
    load_employees()
    clear_fields()
    messagebox.showinfo("Success", "Employee added successfully")

def update_employee():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror("Error", "Select an employee to update")
        return

    employee_id = tree.item(selected_item, 'values')[0]
    tennv = entry_name.get()
    sdt = entry_phone.get()
    email = entry_email.get()
    matkhau = entry_password.get()
    chucvu = entry_position.get()
    ngaybatdau = entry_start_date.get()
    luong = entry_salary.get()

    if not (tennv and sdt and email and matkhau and chucvu and ngaybatdau and luong):
        messagebox.showerror("Error", "All fields are required")
        return

    c.execute("""UPDATE nhanvien SET tennv=?, sdt=?, email=?, matkhau=?, chucvu=?, ngaybatdau=?, luong=?
                 WHERE idnv=?""",
              (tennv, sdt, email, matkhau, chucvu, ngaybatdau, float(luong), employee_id))
    conn.commit()
    load_employees()
    clear_fields()
    messagebox.showinfo("Success", "Employee updated successfully")

def delete_employee():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror("Error", "Select an employee to delete")
        return

    employee_id = tree.item(selected_item, 'values')[0]
    c.execute("DELETE FROM nhanvien WHERE idnv=?", (employee_id,))
    conn.commit()
    load_employees()
    clear_fields()
    messagebox.showinfo("Success", "Employee deleted successfully")

def search_employee():
    search_name = entry_name.get()
    for row in tree.get_children():
        tree.delete(row)
    c.execute("SELECT * FROM nhanvien WHERE tennv LIKE ?", ('%' + search_name + '%',))
    for row in c.fetchall():
        tree.insert("", ctk.END, values=row)

def load_employees():
    for row in tree.get_children():
        tree.delete(row)
    c.execute("SELECT * FROM nhanvien")
    for row in c.fetchall():
        tree.insert("", ctk.END, values=row)

def clear_fields():
    entry_name.delete(0, ctk.END)
    entry_phone.delete(0, ctk.END)
    entry_email.delete(0, ctk.END)
    entry_password.delete(0, ctk.END)
    entry_position.delete(0, ctk.END)
    entry_start_date.delete(0, ctk.END)
    entry_salary.delete(0, ctk.END)

def on_exit():
    conn.close()
    app.quit()

# Create UI components
frame = ctk.CTkFrame(app)
frame.pack(pady=20)

# Name
label_name = ctk.CTkLabel(frame, text="Name")
label_name.grid(row=0, column=0, padx=10, pady=5, sticky=ctk.W)
entry_name = ctk.CTkEntry(frame)
entry_name.grid(row=0, column=1, padx=10, pady=5, sticky=ctk.EW)

# Phone
label_phone = ctk.CTkLabel(frame, text="Phone")
label_phone.grid(row=1, column=0, padx=10, pady=5, sticky=ctk.W)
entry_phone = ctk.CTkEntry(frame)
entry_phone.grid(row=1, column=1, padx=10, pady=5, sticky=ctk.EW)

# Email
label_email = ctk.CTkLabel(frame, text="Email")
label_email.grid(row=2, column=0, padx=10, pady=5, sticky=ctk.W)
entry_email = ctk.CTkEntry(frame)
entry_email.grid(row=2, column=1, padx=10, pady=5, sticky=ctk.EW)

# Password
label_password = ctk.CTkLabel(frame, text="Password")
label_password.grid(row=3, column=0, padx=10, pady=5, sticky=ctk.W)
entry_password = ctk.CTkEntry(frame, show="*")
entry_password.grid(row=3, column=1, padx=10, pady=5, sticky=ctk.EW)

# Position
label_position = ctk.CTkLabel(frame, text="Position")
label_position.grid(row=4, column=0, padx=10, pady=5, sticky=ctk.W)
entry_position = ctk.CTkEntry(frame)
entry_position.grid(row=4, column=1, padx=10, pady=5, sticky=ctk.EW)

# Start Date
label_start_date = ctk.CTkLabel(frame, text="Start Date (YYYY-MM-DD)")
label_start_date.grid(row=5, column=0, padx=10, pady=5, sticky=ctk.W)
entry_start_date = ctk.CTkEntry(frame)
entry_start_date.grid(row=5, column=1, padx=10, pady=5, sticky=ctk.EW)

# Salary
label_salary = ctk.CTkLabel(frame, text="Salary")
label_salary.grid(row=6, column=0, padx=10, pady=5, sticky=ctk.W)
entry_salary = ctk.CTkEntry(frame)
entry_salary.grid(row=6, column=1, padx=10, pady=5, sticky=ctk.EW)

# Buttons
button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=10)

btn_add = ctk.CTkButton(button_frame, text="Add", command=add_employee)
btn_add.grid(row=0, column=0, padx=10, pady=10)

btn_update = ctk.CTkButton(button_frame, text="Update", command=update_employee)
btn_update.grid(row=0, column=1, padx=10, pady=10)

btn_delete = ctk.CTkButton(button_frame, text="Delete", command=delete_employee)
btn_delete.grid(row=0, column=2, padx=10, pady=10)

btn_search = ctk.CTkButton(button_frame, text="Search", command=search_employee)
btn_search.grid(row=0, column=3, padx=10, pady=10)

btn_exit = ctk.CTkButton(button_frame, text="Exit", command=on_exit)
btn_exit.grid(row=0, column=4, padx=10, pady=10)

# Employee List
tree_frame = ctk.CTkFrame(app)
tree_frame.pack(pady=10)

columns = ("ID", "Name", "Phone", "Email", "Position", "Start Date", "Salary")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Phone", text="Phone")
tree.heading("Email", text="Email")
tree.heading("Position", text="Position")
tree.heading("Start Date", text="Start Date")
tree.heading("Salary", text="Salary")

tree.pack(fill=ctk.BOTH, expand=True)
load_employees()

app.mainloop()
