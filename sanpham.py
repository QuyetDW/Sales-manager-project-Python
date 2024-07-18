import customtkinter as ctk
from tkinter import ttk, messagebox
from database import fetch_all_product, insert_product, delete_product, update_product, search_products

def show_sanpham(main_frame):
    # Clear the main frame
    for widget in main_frame.winfo_children():
        widget.destroy()

    label = ctk.CTkLabel(main_frame, text="Trang Quản Lý Sản Phẩm Thiết Bị Di Động", font=("Arial", 30))
    label.pack(pady=20)

    form_frame = ctk.CTkFrame(main_frame, corner_radius=10)
    form_frame.pack(pady=20, padx=20, fill="x")

    font_size_label = ("Arial", 15)
    entry_width = 300

    # Adjusted layout for two-column entry form
    ctk.CTkLabel(form_frame, text="Tên Sản Phẩm:", font=font_size_label).grid(row=0, column=0, padx=10, pady=10, sticky='e')
    product_name_entry = ctk.CTkEntry(form_frame, font=font_size_label, width=entry_width)
    product_name_entry.grid(row=0, column=1, padx=10, pady=10)

    ctk.CTkLabel(form_frame, text="Thương Hiệu:", font=font_size_label).grid(row=0, column=2, padx=10, pady=10, sticky='e')
    brand_entry = ctk.CTkEntry(form_frame, font=font_size_label, width=entry_width)
    brand_entry.grid(row=0, column=3, padx=10, pady=10)

    ctk.CTkLabel(form_frame, text="Giá Bán:", font=font_size_label).grid(row=1, column=0, padx=10, pady=10, sticky='e')
    price_entry = ctk.CTkEntry(form_frame, font=font_size_label, width=entry_width)
    price_entry.grid(row=1, column=1, padx=10, pady=10)

    ctk.CTkLabel(form_frame, text="Bảo Hành (Tháng):", font=font_size_label).grid(row=1, column=2, padx=10, pady=10, sticky='e')
    warranty_entry = ctk.CTkEntry(form_frame, font=font_size_label, width=entry_width)
    warranty_entry.grid(row=1, column=3, padx=10, pady=10)

    ctk.CTkLabel(form_frame, text="Mô Tả:", font=font_size_label).grid(row=2, column=0, padx=10, pady=10, sticky='e')
    description_entry = ctk.CTkEntry(form_frame, font=font_size_label, width=entry_width)
    description_entry.grid(row=2, column=1, padx=10, pady=10)

    # Search bar and search button

    search_entry = ctk.CTkEntry(form_frame, font=font_size_label, width=entry_width)
    search_entry.grid(row=3, column=1, padx=10, pady=10, columnspan=2)

    search_button = ctk.CTkButton(form_frame, text="Tìm Kiếm", command=lambda: search_product(search_entry.get()), font=font_size_label)
    search_button.grid(row=3, column=2, padx=10, pady=10)

    # Function buttons
    button_frame = ctk.CTkFrame(form_frame, corner_radius=10)
    button_frame.grid(row=4, column=0, columnspan=4, pady=20)

    add_button = ctk.CTkButton(button_frame, text="Thêm", command=lambda: add_product(), font=font_size_label)
    add_button.grid(row=0, column=0, padx=5, pady=10)

    delete_button = ctk.CTkButton(button_frame, text="Xóa", command=lambda: delete_selected(), font=font_size_label)
    delete_button.grid(row=0, column=1, padx=5, pady=10)

    update_button = ctk.CTkButton(button_frame, text="Cập Nhật", command=lambda: update_product_func(), font=font_size_label)
    update_button.grid(row=0, column=2, padx=5, pady=10)

    refresh_button = ctk.CTkButton(button_frame, text="Làm Mới", command=lambda: refresh_table(), font=font_size_label)
    refresh_button.grid(row=0, column=3, padx=5, pady=10)

    form_frame.grid_columnconfigure(0, weight=1)
    form_frame.grid_columnconfigure(1, weight=1)
    form_frame.grid_columnconfigure(2, weight=1)
    form_frame.grid_columnconfigure(3, weight=1)
    form_frame.grid_rowconfigure(0, weight=1)
    form_frame.grid_rowconfigure(1, weight=1)
    form_frame.grid_rowconfigure(2, weight=1)
    form_frame.grid_rowconfigure(3, weight=1)
    form_frame.grid_rowconfigure(4, weight=1)

    # Data table
    data_frame = ctk.CTkFrame(main_frame, corner_radius=10)
    data_frame.pack(pady=10, padx=20, fill="both", expand=True)

    columns = ("ID Sản Phẩm", "Tên Sản Phẩm", "Thương Hiệu", "Giá Bán", "Bảo Hành", "Mô Tả")
    tree = ttk.Treeview(data_frame, columns=columns, show="headings", height=15)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor='center', width=150)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 16), padding=(5, 10))
    style.configure("Treeview", font=("Arial", 16), padding=(5, 10))

    tree.pack(fill="both", expand=True)

    def refresh_table():
        try:
            for row in tree.get_children():
                tree.delete(row)
            for row in fetch_all_product():
                tree.insert('', 'end', values=row)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể làm mới bảng dữ liệu: {e}")

    def add_product():
        try:
            product_name = product_name_entry.get()
            brand = brand_entry.get()
            price = price_entry.get()
            warranty = warranty_entry.get()
            description = description_entry.get()

            if not product_name or not brand or not price or not warranty:
                raise ValueError("Các trường bắt buộc không được để trống.")

            if not price.replace('.', '', 1).isdigit() or not warranty.isdigit():
                raise ValueError("Giá và bảo hành phải là số hợp lệ.")

            insert_product(product_name, brand, float(price), int(warranty), description)
            messagebox.showinfo("Thông báo", "Thêm sản phẩm thành công!")
            refresh_table()

            product_name_entry.delete(0, 'end')
            brand_entry.delete(0, 'end')
            price_entry.delete(0, 'end')
            warranty_entry.delete(0, 'end')
            description_entry.delete(0, 'end')
        except ValueError as ve:
            messagebox.showerror("Lỗi", str(ve))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể thêm sản phẩm: {e}")

    def delete_selected():
        try:
            selected_item = tree.selection()
            if selected_item:
                product_id = tree.item(selected_item, 'values')[0]
                delete_product(product_id)
                messagebox.showinfo("Thông báo", "Xóa sản phẩm thành công!")
                refresh_table()
            else:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn sản phẩm để xóa!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xóa sản phẩm: {e}")

    def update_product_func():
        try:
            selected_item = tree.selection()
            if selected_item:
                product_id = tree.item(selected_item, 'values')[0]
                product_name = product_name_entry.get()
                brand = brand_entry.get()
                price = price_entry.get()
                warranty = warranty_entry.get()
                description = description_entry.get()

                if not product_name or not brand:
                    raise ValueError("Các trường bắt buộc không được để trống.")

                if not price.replace('.', '', 1).isdigit() or not warranty.isdigit():
                    raise ValueError("Giá và bảo hành phải là số hợp lệ.")

                update_product(product_id, product_name, brand, float(price), int(warranty), description)
                messagebox.showinfo("Thông báo", "Cập nhật sản phẩm thành công!")
                refresh_table()
            else:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn sản phẩm để cập nhật!")
        except ValueError as ve:
            messagebox.showerror("Lỗi", str(ve))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể cập nhật sản phẩm: {e}")

    def search_product(keyword):
        try:
            if keyword:
                tree.delete(*tree.get_children())
                results = search_products(keyword)
                if results:
                    for row in results:
                        tree.insert('', 'end', values=row)
                else:
                    messagebox.showinfo("Thông báo", "Không tìm thấy sản phẩm nào.")
            else:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập từ khóa để tìm kiếm!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tìm kiếm sản phẩm: {e}")

    def on_tree_select(event):
        selected_item = tree.selection()
        if selected_item:
            values = tree.item(selected_item, 'values')
            if len(values) >= 6:
                product_name_entry.delete(0, 'end')
                product_name_entry.insert(0, values[1])

                brand_entry.delete(0, 'end')
                brand_entry.insert(0, values[2])

                price_entry.delete(0, 'end')
                price_entry.insert(0, values[3])

                warranty_entry.delete(0, 'end')
                warranty_entry.insert(0, values[4])

                description_entry.delete(0, 'end')
                description_entry.insert(0, values[5])
            else:
                product_name_entry.delete(0, 'end')
                brand_entry.delete(0, 'end')
                price_entry.delete(0, 'end')
                warranty_entry.delete(0, 'end')
                description_entry.delete(0, 'end')
                messagebox.showwarning("Cảnh báo", "Dữ liệu không đầy đủ để hiển thị.")
        else:
            product_name_entry.delete(0, 'end')
            brand_entry.delete(0, 'end')
            price_entry.delete(0, 'end')
            warranty_entry.delete(0, 'end')
            description_entry.delete(0, 'end')

    tree.bind("<<TreeviewSelect>>", on_tree_select)

    refresh_table()
