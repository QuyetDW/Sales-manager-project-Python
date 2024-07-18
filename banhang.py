import customtkinter as ctk
from tkinter import ttk, messagebox, Toplevel, Label
from database import fetch_all_employees, fetch_all_customers, fetch_all_products, fetch_sales_history, insert_sale, \
    delete_sales_history
import datetime
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import qrcode
from PIL import Image, ImageTk


def show_banhang(main_frame):
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Tạo tiêu đề lớn cho trang
    label = ctk.CTkLabel(main_frame, text="Trang Bán Hàng", font=("Arial", 30))
    label.pack(pady=10)

    # Khung chứa các form nhập liệu
    form_frame = ctk.CTkFrame(main_frame)
    form_frame.pack(pady=30)

    # Điều chỉnh font chữ lớn hơn cho các label
    font_size_label = ("Arial", 15)

    # Mã Nhân Viên
    ctk.CTkLabel(form_frame, text="Mã Nhân Viên:", font=font_size_label).grid(row=0, column=0, padx=10, pady=10,
                                                                              sticky='e')
    employee_cb = ttk.Combobox(form_frame, values=[f"{e[0]} - {e[1]}" for e in fetch_all_employees()],
                               font=font_size_label)
    employee_cb.grid(row=0, column=1, padx=10, pady=10)

    # Mã Khách Hàng
    ctk.CTkLabel(form_frame, text="Mã Khách Hàng:", font=font_size_label).grid(row=0, column=2, padx=10, pady=10,
                                                                               sticky='e')
    customer_cb = ttk.Combobox(form_frame, values=[f"{c[0]} - {c[1]}" for c in fetch_all_customers()],
                               font=font_size_label)
    customer_cb.grid(row=0, column=3, padx=10, pady=10)

    # Mã Sản Phẩm
    ctk.CTkLabel(form_frame, text="Mã Sản Phẩm:", font=font_size_label).grid(row=1, column=0, padx=10, pady=10,
                                                                             sticky='e')
    products = fetch_all_products()
    product_cb = ttk.Combobox(form_frame, values=[f"{p[0]} - {p[1]}" for p in products], font=font_size_label)
    product_cb.grid(row=1, column=1, padx=10, pady=10)

    # Số Lượng
    ctk.CTkLabel(form_frame, text="Số Lượng:", font=font_size_label).grid(row=1, column=2, padx=10, pady=10, sticky='e')
    quantity_entry = ctk.CTkEntry(form_frame, font=font_size_label)
    quantity_entry.grid(row=1, column=3, padx=10, pady=10)

    # Loại Giao Dịch
    ctk.CTkLabel(form_frame, text="Loại Giao Dịch:", font=font_size_label).grid(row=2, column=0, padx=10, pady=10,
                                                                                sticky='e')
    transaction_type_cb = ttk.Combobox(form_frame, values=["Tiền mặt", "Chuyển khoản"], font=font_size_label)
    transaction_type_cb.grid(row=2, column=1, padx=10, pady=10)

    # Ngày Mua Hàng
    ctk.CTkLabel(form_frame, text="Ngày Mua Hàng:", font=font_size_label).grid(row=2, column=2, padx=10, pady=10,
                                                                               sticky='e')
    purchase_date_entry = ctk.CTkEntry(form_frame, font=font_size_label)
    purchase_date_entry.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))
    purchase_date_entry.grid(row=2, column=3, padx=10, pady=10)

    # Bảng hiển thị dữ liệu
    data_frame = ctk.CTkFrame(main_frame)
    data_frame.pack(pady=10, fill="both", expand=True)

    columns = ("Mã Sản Phẩm", "Tên Sản Phẩm", "Số Lượng", "Giá", "Tổng Tiền")
    tree = ttk.Treeview(data_frame, columns=columns, show="headings", height=15)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor='center', width=150)

    # Điều chỉnh kích thước chữ cho bảng Treeview
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 16), padding=(5, 10))
    style.configure("Treeview", font=("Arial", 16), padding=(5, 10))

    tree.pack(fill="both", expand=True)

    # Hàm để thêm giao dịch vào bảng
    def add_to_table():
        try:
            product_details = product_cb.get().split(" - ")
            product_id = product_details[0]
            product_name = product_details[1]
            quantity = int(quantity_entry.get())
            product_price = next(p[2] for p in products if p[0] == int(product_id))
            total_price = quantity * product_price

            # Kiểm tra xem sản phẩm đã tồn tại trong bảng chưa
            existing_item = None
            for item in tree.get_children():
                values = tree.item(item)["values"]
                if values[0] == product_id:
                    existing_item = item
                    break

            if existing_item:
                # Nếu sản phẩm đã tồn tại, cập nhật số lượng và tổng giá
                current_quantity = tree.item(existing_item)["values"][2]
                new_quantity = current_quantity + quantity
                new_total_price = new_quantity * product_price
                tree.item(existing_item,
                          values=(product_id, product_name, new_quantity, product_price, new_total_price))
            else:
                # Nếu sản phẩm chưa tồn tại, thêm dòng mới
                tree.insert("", "end", values=(product_id, product_name, quantity, product_price, total_price))

            # Reset lại các trường nhập liệu
            quantity_entry.delete(0, 'end')
            product_cb.set('')
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi thêm giao dịch: {e}")

    # Hàm để xóa giao dịch khỏi bảng
    def delete_selected():
        selected_item = tree.selection()
        for item in selected_item:
            tree.delete(item)

    def checkout():
        try:
            employee_id = employee_cb.get().split(" - ")[0]
            employee_name = employee_cb.get().split(" - ")[1]
            customer_id = customer_cb.get().split(" - ")[0]
            customer_name = customer_cb.get().split(" - ")[1]
            transaction_type = transaction_type_cb.get()
            purchase_date = purchase_date_entry.get()

            total_amount = 0.0
            items_purchased = []

            for item in tree.get_children():
                values = tree.item(item)["values"]
                product_id = values[0]
                product_name = values[1]
                quantity = int(values[2])
                price = float(values[3])
                total_price = float(values[4])

                items_purchased.append(
                    f"Sản phẩm: {product_name} (Mã: {product_id}), Số lượng: {quantity}, Giá: {price} VNĐ, Tổng: {total_price} VNĐ")

                insert_sale(product_id, customer_id, employee_id, transaction_type, quantity, total_price,
                            purchase_date)

                total_amount += total_price

            details = (
                    f"Thông tin giao dịch:\n\n"
                    f"Nhân viên: {employee_name} (Mã: {employee_id})\n"
                    f"Khách hàng: {customer_name} (Mã: {customer_id})\n"
                    f"Ngày mua: {purchase_date}\n"
                    f"Loại giao dịch: {transaction_type}\n\n"
                    f"Các sản phẩm đã mua:\n" + "\n".join(items_purchased) + "\n\n"
                                                                             f"Tổng tiền: {total_amount} VNĐ"
            )

            messagebox.showinfo("Chi Tiết Thanh Toán", details)

            # Thông báo hỏi in hóa đơn
            if messagebox.askyesno("In hóa đơn", "Bạn có muốn in hóa đơn này không?"):
                print_receipt_as_pdf(employee_name, customer_name, transaction_type, purchase_date, items_purchased,
                                     total_amount)

            if transaction_type == "Chuyển khoản":
                show_qr_code(total_amount)

            tree.delete(*tree.get_children())

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể thanh toán: {e}")

    def show_qr_code(amount):
        qr_data = f"Amount to pay: {amount} VNĐ"
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill='black', back_color='white')

        # Convert the QR image to a format that Tkinter can use
        qr_img = qr_img.resize((200, 200), Image.Resampling.LANCZOS)  # Updated to use Resampling.LANCZOS
        qr_img = ImageTk.PhotoImage(qr_img)

        # Create a new window to display the QR code
        qr_window = Toplevel()
        qr_window.title("QR Code for Payment")
        qr_label = Label(qr_window, image=qr_img)
        qr_label.image = qr_img  # Keep a reference to avoid garbage collection
        qr_label.pack(padx=20, pady=20)

    def print_receipt_as_pdf(employee_name, customer_name, transaction_type, purchase_date, items_purchased,
                             total_amount):
        try:
            # Tạo tên file PDF
            pdf_filename = f"hoadon_{customer_name}_{purchase_date.replace('-', '')}.pdf"

            # Khởi tạo canvas
            c = canvas.Canvas(pdf_filename, pagesize=letter)
            width, height = letter

            # Đăng ký phông chữ DejaVu Sans
            pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
            c.setFont("DejaVuSans", 20)

            # Tiêu đề hóa đơn
            c.drawString(100, height - 50, "HÓA ĐƠN MUA HÀNG")

            # Thông tin cơ bản
            c.setFont("DejaVuSans", 12)
            c.drawString(100, height - 100, f"Nhân viên: {employee_name}")
            c.drawString(100, height - 120, f"Khách hàng: {customer_name}")
            c.drawString(100, height - 140, f"Ngày mua: {purchase_date}")
            c.drawString(100, height - 160, f"Loại giao dịch: {transaction_type}")

            # Thông tin sản phẩm
            c.setFont("DejaVuSans", 12)
            c.drawString(100, height - 200, "Danh sách sản phẩm:")

            y_position = height - 220
            for item in items_purchased:
                if y_position < 100:
                    c.showPage()
                    y_position = height - 50
                    c.setFont("DejaVuSans", 12)  # Đặt lại phông chữ sau khi đổi trang
                c.drawString(100, y_position, item)
                y_position -= 20

            # Tổng tiền
            c.drawString(100, y_position - 20, f"Tổng tiền: {total_amount} VNĐ")

            # Lưu file PDF
            c.save()

            messagebox.showinfo("Thông báo", f"Hóa đơn đã được lưu thành file PDF: {pdf_filename}")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tạo hóa đơn PDF: {e}")

    def show_sales_history():
        try:
            tree.delete(*tree.get_children())
            columns = ("Mã Sản Phẩm", "Tên Sản Phẩm", "Số Lượng", "Giá", "Ngày Mua", "Tên Nhân Viên", "Tên Khách Hàng")
            tree["columns"] = columns
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, anchor='center', width=150)  # Giảm chiều rộng của cột để tiết kiệm không gian

            sales_history = fetch_sales_history()
            for record in sales_history:
                tree.insert("", "end", values=record)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể hiển thị lịch sử mua hàng: {e}")

    # Hàm để xóa lịch sử mua hàng
    def delete_sales_history_func():
        try:
            response = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa toàn bộ lịch sử mua hàng không?")
            if response:
                delete_sales_history()
                messagebox.showinfo("Thành công", "Lịch sử mua hàng đã được xóa thành công.")
                tree.delete(*tree.get_children())
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xóa lịch sử mua hàng: {e}")

    # Nút thêm
    add_button = ctk.CTkButton(form_frame, text="Thêm Giỏ Hàng", command=add_to_table, font=font_size_label)
    add_button.grid(row=3, column=1, padx=10, pady=10, sticky='we')

    # Nút thanh toán
    checkout_button = ctk.CTkButton(form_frame, text="Thanh Toán", command=checkout, font=font_size_label)
    checkout_button.grid(row=3, column=2, padx=10, pady=10, sticky='we')

    # Nút xóa
    delete_button = ctk.CTkButton(form_frame, text="Xóa", command=delete_selected, font=font_size_label)
    delete_button.grid(row=3, column=3, padx=10, pady=10, sticky='we')

    # Nút lịch sử mua hàng
    history_button = ctk.CTkButton(form_frame, text="Lịch Sử Mua Hàng", command=show_sales_history,
                                   font=font_size_label)
    history_button.grid(row=5, column=0, columnspan=4, padx=10, pady=10, sticky='we')

    # Nút xóa lịch sử mua hàng
    delete_history_button = ctk.CTkButton(form_frame, text="Xóa Lịch Sử Mua Hàng", command=delete_sales_history_func,
                                          font=font_size_label)
    delete_history_button.grid(row=6, column=0, columnspan=4, padx=10, pady=10, sticky='we')

    # Cấu hình lưới để các widget co dãn hợp lý
    form_frame.grid_columnconfigure(0, weight=1)
    form_frame.grid_columnconfigure(1, weight=1)
    form_frame.grid_columnconfigure(2, weight=1)
    form_frame.grid_columnconfigure(3, weight=1)
    form_frame.grid_rowconfigure(0, weight=1)
    form_frame.grid_rowconfigure(1, weight=1)
    form_frame.grid_rowconfigure(2, weight=1)
    form_frame.grid_rowconfigure(3, weight=1)
    form_frame.grid_rowconfigure(4, weight=1)
    form_frame.grid_rowconfigure(5, weight=1)
    form_frame.grid_rowconfigure(6, weight=1)

