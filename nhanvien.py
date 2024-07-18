import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
import database

selected_id = None

def show_nhanvien(main_frame):
    global selected_id

    def display_data():
        rows = database.fetch_data()
        update_table(rows)

    def update_table(rows):
        for row in tree.get_children():
            tree.delete(row)
        for row in rows:
            tree.insert("", tk.END, values=row)

    def clear_entries():
        entry_name.delete(0, tk.END)
        entry_phone.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_password.delete(0, tk.END)
        entry_position.delete(0, tk.END)
        entry_startdate.delete(0, tk.END)
        entry_salary.delete(0, tk.END)

    def add_employee():
        name = entry_name.get().strip()
        phone = entry_phone.get().strip()
        email = entry_email.get().strip()
        password = entry_password.get().strip()
        position = entry_position.get().strip()
        start_date = entry_startdate.get().strip()
        salary = entry_salary.get().strip()

        if not (name and phone and email and password and position and start_date and salary):
            messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin nhân viên.")
            return

        database.add_employee(name, phone, email, password, position, start_date, float(salary))
        messagebox.showinfo("Thông báo", "Thêm nhân viên thành công")
        clear_entries()
        display_data()

    def edit_employee():
        if not selected_id:
            messagebox.showerror("Lỗi", "Vui lòng chọn nhân viên cần cập nhật.")
            return

        name = entry_name.get().strip()
        phone = entry_phone.get().strip()
        email = entry_email.get().strip()
        password = entry_password.get().strip()
        position = entry_position.get().strip()
        start_date = entry_startdate.get().strip()
        salary = entry_salary.get().strip()

        if not (name and phone and email and password and position and start_date and salary):
            messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin nhân viên.")
            return

        database.edit_employee(selected_id, name, phone, email, password, position, start_date, float(salary))
        messagebox.showinfo("Thông báo", "Cập nhật nhân viên thành công")
        clear_entries()
        display_data()

    def delete_employee():
        if not selected_id:
            messagebox.showerror("Lỗi", "Vui lòng chọn nhân viên cần xóa.")
            return

        database.delete_employee(selected_id)
        messagebox.showinfo("Thông báo", "Xóa nhân viên thành công")
        clear_entries()
        display_data()

    def search_employee():
        rows = database.search_employee(entry_search.get())
        update_table(rows)

    def on_select(event):
        global selected_id
        selected_row = tree.focus()
        data = tree.item(selected_row, 'values')
        selected_id = data[0]
        clear_entries()
        entry_name.insert(0, data[1])
        entry_phone.insert(0, data[2])
        entry_email.insert(0, data[3])
        entry_password.insert(0, data[4])
        entry_position.insert(0, data[5])
        entry_startdate.insert(0, data[6])
        entry_salary.insert(0, data[7])

    for widget in main_frame.winfo_children():
        widget.destroy()

    label = ctk.CTkLabel(main_frame, text="Trang Nhân Viên", font=("Arial", 24))
    label.pack(pady=20)

    font_size_label = ("Arial", 15)

    # Form Frame
    form_frame = ctk.CTkFrame(main_frame)
    form_frame.pack(side="top", fill="x", padx=20, pady=20)

    # Center form frame widgets
    form_frame.grid_columnconfigure((0, 5), weight=1)
    form_frame.grid_columnconfigure((1, 2, 3, 4), weight=0)

    # Table Frame
    table_frame = ctk.CTkFrame(main_frame)
    table_frame.pack(side="bottom", fill="both", expand=True, padx=20, pady=20)

    # Form widgets
    ctk.CTkLabel(form_frame, text="Tên NV", font=font_size_label).grid(row=0, column=1, padx=10, pady=5, sticky="w")
    entry_name = ctk.CTkEntry(form_frame, font=font_size_label)
    entry_name.grid(row=0, column=2, padx=10, pady=5)

    ctk.CTkLabel(form_frame, text="SĐT", font=font_size_label).grid(row=1, column=1, padx=10, pady=5, sticky="w")
    entry_phone = ctk.CTkEntry(form_frame, font=font_size_label)
    entry_phone.grid(row=1, column=2, padx=10, pady=5)

    ctk.CTkLabel(form_frame, text="Email", font=font_size_label).grid(row=2, column=1, padx=10, pady=5, sticky="w")
    entry_email = ctk.CTkEntry(form_frame, font=font_size_label)
    entry_email.grid(row=2, column=2, padx=10, pady=5)

    ctk.CTkLabel(form_frame, text="Mật Khẩu", font=font_size_label).grid(row=3, column=1, padx=10, pady=5, sticky="w")
    entry_password = ctk.CTkEntry(form_frame, show="*", font=font_size_label)
    entry_password.grid(row=3, column=2, padx=10, pady=5)

    ctk.CTkLabel(form_frame, text="Chức Vụ", font=font_size_label).grid(row=0, column=3, padx=10, pady=5, sticky="w")
    entry_position = ctk.CTkEntry(form_frame, font=font_size_label)
    entry_position.grid(row=0, column=4, padx=10, pady=5)

    ctk.CTkLabel(form_frame, text="Ngày Bắt Đầu", font=font_size_label).grid(row=1, column=3, padx=10, pady=5, sticky="w")
    entry_startdate = ctk.CTkEntry(form_frame, font=font_size_label)
    entry_startdate.grid(row=1, column=4, padx=10, pady=5)

    ctk.CTkLabel(form_frame, text="Lương", font=font_size_label).grid(row=2, column=3, padx=10, pady=5, sticky="w")
    entry_salary = ctk.CTkEntry(form_frame, font=font_size_label)
    entry_salary.grid(row=2, column=4, padx=10, pady=5)

    # Buttons
    button_frame = ctk.CTkFrame(main_frame)
    button_frame.pack(pady=10, fill="x")
    button_frame.grid_columnconfigure((0, 7), weight=1)
    button_frame.grid_columnconfigure((1, 2, 3, 4, 5, 6), weight=0)

    ctk.CTkButton(button_frame, text="Thêm", command=add_employee, font=font_size_label).grid(row=0, column=1, padx=10, pady=10)
    ctk.CTkButton(button_frame, text="Sửa", command=edit_employee, font=font_size_label).grid(row=0, column=2, padx=10, pady=10)
    ctk.CTkButton(button_frame, text="Xóa", command=delete_employee, font=font_size_label).grid(row=0, column=3, padx=10, pady=10)
    ctk.CTkButton(button_frame, text="Tìm Kiếm", command=search_employee, font=font_size_label).grid(row=0, column=5, padx=10, pady=10)

    # Search entry
    entry_search = ctk.CTkEntry(button_frame)
    entry_search.grid(row=0, column=4, padx=10, pady=10)

    # Table
    columns = ("ID", "Tên NV", "SĐT", "Email", "Mật Khẩu", "Chức Vụ", "Ngày Bắt Đầu", "Lương")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, stretch=tk.YES, width=100)

    scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree.pack(fill="both", expand=True)

    tree.bind("<ButtonRelease-1>", on_select)

    # Initial data display
    display_data()

# Example usage
if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Quản Lý Nhân Viên")
    app.geometry("1200x700")

    main_frame = ctk.CTkFrame(app)
    main_frame.pack(fill="both", expand=True)

    show_nhanvien(main_frame)

    app.mainloop()
