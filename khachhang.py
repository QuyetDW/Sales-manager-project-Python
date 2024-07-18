import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk
import database

# Function to refresh the customer list
def refresh_customer_list(tree):
    for i in tree.get_children():
        tree.delete(i)
    for row in database.get_all_customers():
        tree.insert('', 'end', values=row)

def show_khachhang(main_frame):
    for widget in main_frame.winfo_children():
        widget.destroy()

    label = ctk.CTkLabel(main_frame, text="Trang Khách Hàng", font=("Arial", 24))
    label.pack(pady=20)
    font_size_label = ("Arial", 15)

    # Entry fields for customer data
    entry_frame = ctk.CTkFrame(main_frame)
    entry_frame.pack(pady=10)

    ctk.CTkLabel(entry_frame, text="Tên khách hàng:", font=font_size_label).grid(row=0, column=0, padx=5, pady=5)
    tenkh_entry = ctk.CTkEntry(entry_frame, width=200, font=font_size_label)
    tenkh_entry.grid(row=0, column=1, padx=5, pady=5)

    ctk.CTkLabel(entry_frame, text="Số điện thoại:", font=font_size_label).grid(row=1, column=0, padx=5, pady=5)
    sdt_entry = ctk.CTkEntry(entry_frame, width=200, font=font_size_label)
    sdt_entry.grid(row=1, column=1, padx=5, pady=5)

    ctk.CTkLabel(entry_frame, text="Email:", font=font_size_label).grid(row=2, column=0, padx=5, pady=5)
    email_entry = ctk.CTkEntry(entry_frame, width=200, font=font_size_label)
    email_entry.grid(row=2, column=1, padx=5, pady=5)

    ctk.CTkLabel(entry_frame, text="Địa chỉ:", font=font_size_label).grid(row=3, column=0, padx=5, pady=5)
    diachi_entry = ctk.CTkEntry(entry_frame, width=200, font=font_size_label)
    diachi_entry.grid(row=3, column=1, padx=5, pady=5)

    # Function to add a customer
    def add_customer():
        try:
            tenkh = tenkh_entry.get()
            sdt = sdt_entry.get()
            email = email_entry.get()
            diachi = diachi_entry.get()
            if tenkh:
                database.add_customer(tenkh, sdt, email, diachi)
                refresh_customer_list(tree)
                messagebox.showinfo("Thành công", "Thêm khách hàng thành công")
            else:
                messagebox.showerror("Lỗi", "Tên là bắt buộc")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thêm được khách hàng: {e}")

    # Function to update a customer
    def update_customer():
        try:
            selected_item = tree.selection()
            if selected_item:
                idkh = tree.item(selected_item)["values"][0]
                tenkh = tenkh_entry.get()
                sdt = sdt_entry.get()
                email = email_entry.get()
                diachi = diachi_entry.get()
                database.update_customer(idkh, tenkh, sdt, email, diachi)
                refresh_customer_list(tree)
                messagebox.showinfo("Thành công", "Khách hàng cập nhật thành công")
            else:
                messagebox.showerror("Lỗi", "Chọn khách hàng để cập nhật")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể cập nhật khách hàng: {e}")

    # Function to delete a customer
    def delete_customer():
        try:
            selected_item = tree.selection()
            if selected_item:
                idkh = tree.item(selected_item)["values"][0]
                database.delete_customer(idkh)
                refresh_customer_list(tree)
                messagebox.showinfo("Thành công", "Xóa khách hàng thành công")
            else:
                messagebox.showerror("Lỗi", "Chọn khách hàng cần xóa")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xóa khách hàng: {e}")

    # Function to search customers
    def search_customers():
        try:
            keyword = search_entry.get()
            results = database.search_customers(keyword)
            for i in tree.get_children():
                tree.delete(i)
            for row in results:
                tree.insert('', 'end', values=row)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không tìm kiếm được khách hàng: {e}")

    # Function to populate the entry fields when a row is clicked
    def on_tree_select(event):
        selected_item = tree.selection()
        if selected_item:
            item = tree.item(selected_item)
            values = item['values']
            tenkh_entry.delete(0, 'end')
            tenkh_entry.insert(0, values[1])
            sdt_entry.delete(0, 'end')
            sdt_entry.insert(0, values[2])
            email_entry.delete(0, 'end')
            email_entry.insert(0, values[3])
            diachi_entry.delete(0, 'end')
            diachi_entry.insert(0, values[4])

    # Buttons for add, update, delete, and search
    button_frame = ctk.CTkFrame(main_frame)
    button_frame.pack(pady=10, fill="x")

    add_button = ctk.CTkButton(button_frame, text="Thêm", command=add_customer)
    add_button.grid(row=0, column=0, padx=5, pady=5)

    update_button = ctk.CTkButton(button_frame, text="Sửa", command=update_customer)
    update_button.grid(row=0, column=1, padx=5, pady=5)

    delete_button = ctk.CTkButton(button_frame, text="Xóa", command=delete_customer)
    delete_button.grid(row=0, column=2, padx=5, pady=5)

    ctk.CTkLabel(button_frame, text="Tìm kiếm:").grid(row=0, column=3, padx=5, pady=5)
    search_entry = ctk.CTkEntry(button_frame, width=200)
    search_entry.grid(row=0, column=4, padx=5, pady=5)

    search_button = ctk.CTkButton(button_frame, text="Tìm", command=search_customers)
    search_button.grid(row=0, column=5, padx=5, pady=5)

    # Frame for treeview and scrollbar
    tree_frame = ctk.CTkFrame(main_frame)
    tree_frame.pack(pady=10, fill='both', expand=True)

    # Treeview to display customers
    columns = ("idkh", "tenkh", "sdt", "email", "diachi")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
    tree.heading("idkh", text="ID")
    tree.heading("tenkh", text="Tên khách hàng")
    tree.heading("sdt", text="Số điện thoại")
    tree.heading("email", text="Email")
    tree.heading("diachi", text="Địa chỉ")

    # Scrollbar for the treeview
    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(pady=10, fill='both', expand=True)

    # Bind the treeview select event to populate the entry fields
    tree.bind('<<TreeviewSelect>>', on_tree_select)

    # Refresh the treeview with all customers initially
    refresh_customer_list(tree)

# Main application setup
if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("800x600")
    app.title("Quản Lý Khách Hàng")

    main_frame = ctk.CTkFrame(app)
    main_frame.pack(pady=20, padx=20, fill="both", expand=True)

    show_khachhang(main_frame)

    app.mainloop()
