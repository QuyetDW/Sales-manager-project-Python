from customtkinter import *
from PIL import Image
import mysql.connector
from Dashboard import show_dashboard  # Import hàm show_dashboard từ dashboard.py

# Kết nối tới cơ sở dữ liệu MySQL
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="btlpython"
    )

# Xử lý đăng nhập
def login():
    email = email_entry.get()
    password = password_entry.get()

    if not email or not password:
        CTkLabel(master=frame, text="Please enter email and password", text_color="red").pack(anchor="w", padx=(25, 0))
        return

    # Kết nối tới cơ sở dữ liệu
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT matkhau FROM nhanvien WHERE email = %s", (email,))
        result = cursor.fetchone()

        if result:
            stored_password = result[0]  # Lấy mật khẩu từ cơ sở dữ liệu

            # So sánh mật khẩu nhập vào với mật khẩu trong cơ sở dữ liệu
            if password == stored_password:
                CTkLabel(master=frame, text="Login successful", text_color="green").pack(anchor="w", padx=(25, 0))
                app.withdraw()  # Ẩn cửa sổ hiện tại
                show_dashboard()  # Hiển thị trang Dashboard
            else:
                CTkLabel(master=frame, text="Invalid password", text_color="red").pack(anchor="w", padx=(25, 0))
        else:
            CTkLabel(master=frame, text="Email not found", text_color="red").pack(anchor="w", padx=(25, 0))

    except Exception as e:
        print(f"Error: {e}")
        CTkLabel(master=frame, text="Error with database operation", text_color="red").pack(anchor="w", padx=(25, 0))

    cursor.close()
    conn.close()

# Hiển thị trang đăng ký
def show_registration():
    frame.pack_forget()  # Ẩn khung đăng nhập
    registration_frame = CTkFrame(master=app, width=300, height=480, fg_color="#ffffff")
    registration_frame.pack_propagate(0)
    registration_frame.pack(expand=True, side="right")

    # Thêm các nhãn và trường nhập liệu vào khung
    CTkLabel(master=registration_frame, text="Create Account", text_color="#601E88", anchor="w", justify="left",
             font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
    CTkLabel(master=registration_frame, text="Sign up with your details", text_color="#7E7E7E", anchor="w", justify="left",
             font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))

    CTkLabel(master=registration_frame, text="  Email:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14),
             image=email_icon, compound="left").pack(anchor="w", pady=(38, 0), padx=(25, 0))
    registration_email_entry = CTkEntry(master=registration_frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1,
                                        text_color="#000000")
    registration_email_entry.pack(anchor="w", padx=(25, 0))

    CTkLabel(master=registration_frame, text="  Password:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14),
             image=password_icon, compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))
    registration_password_entry = CTkEntry(master=registration_frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1,
                                           text_color="#000000", show="*")
    registration_password_entry.pack(anchor="w", padx=(25, 0))

    # Nút đăng ký
    CTkButton(master=registration_frame, text="Register", fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12),
              text_color="#ffffff", width=225, command=lambda: register_user(registration_email_entry.get(), registration_password_entry.get())).pack(anchor="w", pady=(40, 0), padx=(25, 0))

    # Nút quay lại trang đăng nhập
    CTkButton(master=registration_frame, text="Back to Login", fg_color="#EEEEEE", hover_color="#EEEEEE", font=("Arial Bold", 9),
              text_color="#601E88", width=225, command=lambda: [registration_frame.pack_forget(), frame.pack(expand=True, side="right")]).pack(anchor="w", pady=(20, 0), padx=(25, 0))

# Xử lý đăng ký người dùng
def register_user(email, password):
    if not email or not password:
        CTkLabel(master=frame, text="Please enter email and password", text_color="red").pack(anchor="w", padx=(25, 0))
        return

    # Kết nối tới cơ sở dữ liệu
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        # Kiểm tra email đã tồn tại
        cursor.execute("SELECT email FROM nhanvien WHERE email = %s", (email,))
        result = cursor.fetchone()

        if result:
            CTkLabel(master=frame, text="Email already exists", text_color="red").pack(anchor="w", padx=(25, 0))
        else:
            # Thêm người dùng mới vào cơ sở dữ liệu
            cursor.execute("INSERT INTO nhanvien (email, matkhau) VALUES (%s, %s)", (email, password))
            conn.commit()
            CTkLabel(master=frame, text="Registration successful", text_color="green").pack(anchor="w", padx=(25, 0))

    except Exception as e:
        print(f"Error: {e}")
        CTkLabel(master=frame, text="Error with database operation", text_color="red").pack(anchor="w", padx=(25, 0))

    cursor.close()
    conn.close()

# Tạo giao diện người dùng
app = CTk()
app.geometry("600x480")
app.resizable(0, 0)

# Load hình ảnh
side_img_data = Image.open("img/side-img.png")
email_icon_data = Image.open("img/email-icon.png")
password_icon_data = Image.open("img/password-icon.png")
google_icon_data = Image.open("img/google-icon.png")

# Tạo các đối tượng hình ảnh
side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(300, 480))
email_icon = CTkImage(dark_image=email_icon_data, light_image=email_icon_data, size=(20, 20))
password_icon = CTkImage(dark_image=password_icon_data, light_image=password_icon_data, size=(17, 17))
google_icon = CTkImage(dark_image=google_icon_data, light_image=google_icon_data, size=(17, 17))

# Thêm hình ảnh bên trái
CTkLabel(master=app, text="", image=side_img).pack(expand=True, side="left")

# Tạo khung bên phải
frame = CTkFrame(master=app, width=300, height=480, fg_color="#ffffff")
frame.pack_propagate(0)
frame.pack(expand=True, side="right")

# Thêm các nhãn và trường nhập liệu vào khung
CTkLabel(master=frame, text="Welcome Back!", text_color="#601E88", anchor="w", justify="left",
         font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
CTkLabel(master=frame, text="Sign in to your account", text_color="#7E7E7E", anchor="w", justify="left",
         font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))

CTkLabel(master=frame, text="  Email:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14),
         image=email_icon, compound="left").pack(anchor="w", pady=(38, 0), padx=(25, 0))
email_entry = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1,
                       text_color="#000000")
email_entry.pack(anchor="w", padx=(25, 0))

CTkLabel(master=frame, text="  Password:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14),
         image=password_icon, compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))
password_entry = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1,
                          text_color="#000000", show="*")
password_entry.pack(anchor="w", padx=(25, 0))

# Nút đăng nhập
CTkButton(master=frame, text="Login", fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12),
          text_color="#ffffff", width=225, command=login).pack(anchor="w", pady=(40, 0), padx=(25, 0))

# Nút chuyển đến trang đăng ký
CTkButton(master=frame, text="Register", fg_color="#EEEEEE", hover_color="#EEEEEE", font=("Arial Bold", 9),
          text_color="#601E88", width=225, command=show_registration).pack(anchor="w", pady=(10, 0), padx=(25, 0))

# Nút đăng nhập với Google (chưa được cấu hình để thực sự đăng nhập với Google)
CTkButton(master=frame, text="Continue With Google", fg_color="#EEEEEE", hover_color="#EEEEEE", font=("Arial Bold", 9),
          text_color="#601E88", width=225, image=google_icon).pack(anchor="w", pady=(20, 0), padx=(25, 0))

# Bắt đầu vòng lặp chính
app.mainloop()
