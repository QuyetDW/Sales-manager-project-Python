import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
import database

# Function to refresh the warranty list
def refresh_warranty_list(tree):
    for i in tree.get_children():
        tree.delete(i)
    for row in database.get_all_warranties():
        tree.insert('', 'end', values=row)

def show_baohanh(main_frame):
    for widget in main_frame.winfo_children():
        widget.destroy()

    label = ctk.CTkLabel(main_frame, text="Quản Lý Bảo Hành", font=("Arial", 24))
    label.pack(pady=20)
    font_size_label = ("Arial", 15)

    # Entry fields for warranty data
    entry_frame = ctk.CTkFrame(main_frame)
    entry_frame.pack(pady=10)

    ctk.CTkLabel(entry_frame, text="ID Sản phẩm:", font=font_size_label).grid(row=0, column=0, padx=5, pady=5)
    idsp_entry = ctk.CTkEntry(entry_frame, width=150, font=font_size_label)
    idsp_entry.grid(row=0, column=1, padx=5, pady=5)

    ctk.CTkLabel(entry_frame, text="ID Khách hàng:", font=font_size_label).grid(row=1, column=0, padx=5, pady=5)
    idkh_entry = ctk.CTkEntry(entry_frame, width=150, font=font_size_label)
    idkh_entry.grid(row=1, column=1, padx=5, pady=5)

    ctk.CTkLabel(entry_frame, text="Ngày Nhận:", font=font_size_label).grid(row=0, column=2, padx=5, pady=5)
    ngaynhan_entry = DateEntry(entry_frame, background='darkblue', foreground='white', borderwidth=2, font=font_size_label)
    ngaynhan_entry.grid(row=0, column=3, padx=5, pady=5)

    ctk.CTkLabel(entry_frame, text="Ngày Trả:", font=font_size_label).grid(row=1, column=2, padx=5, pady=5)
    ngaytra_entry = DateEntry(entry_frame, background='darkblue', foreground='white', borderwidth=2, font=font_size_label)
    ngaytra_entry.grid(row=1, column=3, padx=5, pady=5)

    ctk.CTkLabel(entry_frame, text="Trạng Thái:", font=font_size_label).grid(row=2, column=2, padx=5, pady=5)
    trangthai_options = ["Chưa được duyệt", "Đang chờ duyệt", "Duyệt bảo hành", "Huỷ bảo hành"]
    trangthai_combobox = ttk.Combobox(entry_frame, values=trangthai_options, width=25)
    trangthai_combobox.grid(row=2, column=3, padx=5, pady=5)
    trangthai_combobox.current(0)  # Set default value

    # Function to add a warranty record
    def add_warranty():
        try:
            idsp = idsp_entry.get()
            idkh = idkh_entry.get()

            if not database.product_exists(idsp):
                messagebox.showerror("Lỗi", "ID sản phẩm không tồn tại")
                return
            if not database.customer_exists(idkh):
                messagebox.showerror("Lỗi", "ID khách hàng không tồn tại")
                return

            ngaynhan = ngaynhan_entry.get_date().strftime('%Y-%m-%d')
            ngaytra = ngaytra_entry.get_date().strftime('%Y-%m-%d')
            trangthai = trangthai_combobox.get()

            if idsp and idkh:
                database.add_warranty(idsp, idkh, ngaynhan, ngaytra, trangthai)
                refresh_warranty_list(tree)
                messagebox.showinfo("Thành công", "Thêm hồ sơ bảo hành thành công")
            else:
                messagebox.showerror("Lỗi", "ID sản phẩm và ID khách hàng là bắt buộc")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể thêm hồ sơ bảo hành: {e}")

    # Function to update a warranty record
    def update_warranty():
        try:
            selected_item = tree.selection()
            if selected_item:
                idbaohanh = tree.item(selected_item)["values"][0]
                idsp = idsp_entry.get()
                idkh = idkh_entry.get()

                if not database.product_exists(idsp):
                    messagebox.showerror("Lỗi", "ID sản phẩm không tồn tại")
                    return
                if not database.customer_exists(idkh):
                    messagebox.showerror("Lỗi", "ID khách hàng không tồn tại")
                    return

                ngaynhan = ngaynhan_entry.get_date().strftime('%Y-%m-%d')
                ngaytra = ngaytra_entry.get_date().strftime('%Y-%m-%d')
                trangthai = trangthai_combobox.get()

                database.update_warranty(idbaohanh, idsp, idkh, ngaynhan, ngaytra, trangthai)
                refresh_warranty_list(tree)
                messagebox.showinfo("Thành công", "Hồ sơ bảo hành được cập nhật thành công")
            else:
                messagebox.showerror("Lỗi", "Chọn bản ghi bảo hành để cập nhật")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể cập nhật hồ sơ bảo hành: {e}")

    # Function to delete a warranty record
    def delete_warranty():
        try:
            selected_item = tree.selection()
            if selected_item:
                idbaohanh = tree.item(selected_item)["values"][0]
                database.delete_warranty(idbaohanh)
                refresh_warranty_list(tree)
                messagebox.showinfo("Thành công", "Xóa hồ sơ bảo hành thành công")
            else:
                messagebox.showerror("Lỗi", "Chọn bản ghi bảo hành để xóa")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không xóa được hồ sơ bảo hành: {e}")

    # Function to search for warranty records
    def search_warranties():
        try:
            keyword = search_entry.get()
            results = database.search_warranties(keyword)
            for i in tree.get_children():
                tree.delete(i)
            for row in results:
                tree.insert('', 'end', values=row)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tìm kiếm hồ sơ bảo hành: {e}")

    # Function to populate the entry fields when a row is clicked
    def on_tree_select(event):
        selected_item = tree.selection()
        if selected_item:
            item = tree.item(selected_item)
            values = item['values']
            idsp_entry.delete(0, 'end')
            idsp_entry.insert(0, values[1])
            idkh_entry.delete(0, 'end')
            idkh_entry.insert(0, values[2])
            ngaynhan_entry.set_date(values[3])
            ngaytra_entry.set_date(values[4])
            trangthai_combobox.set(values[5])

    # Buttons for add, update, delete, and search
    button_frame = ctk.CTkFrame(main_frame)
    button_frame.pack(pady=10, fill='x', padx=70)

    add_button = ctk.CTkButton(button_frame, text="Thêm", command=add_warranty)
    add_button.grid(row=1, column=0, padx=5, pady=5)

    update_button = ctk.CTkButton(button_frame, text="Sửa", command=update_warranty)
    update_button.grid(row=1, column=1, padx=5, pady=5)

    delete_button = ctk.CTkButton(button_frame, text="Xóa", command=delete_warranty)
    delete_button.grid(row=1, column=2, padx=5, pady=5)

    ctk.CTkLabel(button_frame, text="Tìm kiếm:").grid(row=1, column=3, padx=5, pady=5)
    search_entry = ctk.CTkEntry(button_frame, width=200)
    search_entry.grid(row=1, column=4, padx=5, pady=5)
    search_button = ctk.CTkButton(button_frame, text="Tìm", command=search_warranties)
    search_button.grid(row=1, column=5, padx=5, pady=5)

    # Frame for treeview and scrollbar
    tree_frame = ctk.CTkFrame(main_frame)
    tree_frame.pack(pady=10, fill='both', expand=True)

    # Treeview to display warranty records
    columns = ("idbaohanh", "idsp", "idkh", "ngaynhan", "ngaytra", "trangthai")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
    tree.heading("idbaohanh", text="ID")
    tree.heading("idsp", text="ID sản phẩm")
    tree.heading("idkh", text="ID khách hàng")
    tree.heading("ngaynhan", text="Ngày Nhận")
    tree.heading("ngaytra", text="Ngày Trả")
    tree.heading("trangthai", text="Trạng Thái")

    # Scrollbar for treeview
    scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side='right', fill='y')
    tree.pack(pady=10, padx=20, fill='both', expand=True)

    # Bind the treeview select event to populate the entry fields
    tree.bind('<<TreeviewSelect>>', on_tree_select)

    # Refresh the treeview with all warranty records initially
    refresh_warranty_list(tree)

# Main application setup
if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("800x600")
    app.title("Quản Lý Bảo Hành")

    main_frame = ctk.CTkFrame(app)
    main_frame.pack(pady=20, padx=20, fill="both", expand=True)

    show_baohanh(main_frame)

    app.mainloop()
