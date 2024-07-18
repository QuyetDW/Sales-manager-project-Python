import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox
from banhang import show_banhang
from nhanvien import show_nhanvien
from khachhang import show_khachhang
from sanpham import show_sanpham
from baohanh import show_baohanh
from thongke import show_thongke

def show_dashboard():
    def show_page(page_name):
        for widget in main_frame.winfo_children():
            widget.destroy()

        if page_name == "Dashboard":
            show_home_dashboard(main_frame)
        elif page_name == "Bán Hàng":
            show_banhang(main_frame)
        elif page_name == "Nhân Viên":
            show_nhanvien(main_frame)
        elif page_name == "Khách Hàng":
            show_khachhang(main_frame)
        elif page_name == "Sản Phẩm":
            show_sanpham(main_frame)
        elif page_name == "Bảo Hành":
            show_baohanh(main_frame)
        elif page_name == "Thống Kê":
            show_thongke(main_frame)

    def show_home_dashboard(frame):
        label = ctk.CTkLabel(frame, text="Chào mừng đến với cửa hàng di động của chúng tôi !", font=("Arial", 24, "bold"))
        label.pack(pady=20)

        # Display current date and time
        datetime_frame = ctk.CTkFrame(frame, fg_color="#e1e1e1")
        datetime_frame.pack(pady=10)
        update_datetime(datetime_frame)

        # Display store information
        info_frame = ctk.CTkFrame(frame, fg_color="#f2f2f2")
        info_frame.pack(pady=10)
        store_info_label = ctk.CTkLabel(info_frame, text="Cửa hàng bán thiết bị di động EAUT\nĐịa chỉ: Số 1 đường Trịnh Văn Bô, Thành phố Bắc Từ Nam", font=("Arial", 18))
        store_info_label.pack(pady=10)

        image_frame = ctk.CTkFrame(frame, fg_color="#e1e1e1")
        image_frame.pack(pady=10, expand=True, fill='both')

    def update_datetime(frame):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for widget in frame.winfo_children():
            widget.destroy()
        ctk.CTkLabel(frame, text=f"Ngày giờ hiện tại: {now}", font=("Arial", 18)).pack(pady=10)
        frame.after(1000, lambda: update_datetime(frame))

    def confirm_exit():
        if messagebox.askyesno("Xác nhận thoát", "Bạn có chắc chắn muốn thoát?"):
            root.quit()

    # Tạo cửa sổ chính
    root = ctk.CTk()
    root.title("Dashboard")
    root.geometry("800x600")
    root.minsize(600, 400)

    # Cấu hình lưới cho cửa sổ chính
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    # Tạo menu điều hướng bên trái
    menu_frame = ctk.CTkFrame(root, width=200)
    menu_frame.grid(row=0, column=0, sticky="nswe")

    menu_label = ctk.CTkLabel(menu_frame, text="Menu", font=("Arial", 16), text_color="black")
    menu_label.pack(pady=10)

    # Các lựa chọn chức năng
    btn_dashboard = ctk.CTkButton(menu_frame, text="Dashboard", command=lambda: show_page("Dashboard"), hover_color="#45a049")
    btn_dashboard.pack(pady=5)

    btn_banhang = ctk.CTkButton(menu_frame, text="Bán Hàng", command=lambda: show_page("Bán Hàng"), hover_color="#0b7dda")
    btn_banhang.pack(pady=5)

    btn_nhanvien = ctk.CTkButton(menu_frame, text="Nhân Viên", command=lambda: show_page("Nhân Viên"), hover_color="#e68a00")
    btn_nhanvien.pack(pady=5)

    btn_khachhang = ctk.CTkButton(menu_frame, text="Khách Hàng", command=lambda: show_page("Khách Hàng"), hover_color="#7b1fa2")
    btn_khachhang.pack(pady=5)

    btn_sanpham = ctk.CTkButton(menu_frame, text="Sản Phẩm", command=lambda: show_page("Sản Phẩm"), hover_color="#303f9f")
    btn_sanpham.pack(pady=5)

    btn_baohanh = ctk.CTkButton(menu_frame, text="Bảo Hành", command=lambda: show_page("Bảo Hành"), hover_color="#e64a19")
    btn_baohanh.pack(pady=5)

    btn_thongke = ctk.CTkButton(menu_frame, text="Thống Kê", command=lambda: show_page("Thống Kê"), hover_color="#5d4037")
    btn_thongke.pack(pady=5)

    btn_exit = ctk.CTkButton(menu_frame, text="Exit", command=confirm_exit, hover_color="#d32f2f")
    btn_exit.pack(pady=5)

    # Tạo khung chính để hiển thị nội dung
    main_frame = ctk.CTkFrame(root, fg_color="#f0f0f0")
    main_frame.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

    # Cấu hình co dãn
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=5)
    root.grid_rowconfigure(0, weight=1)

    # Hiển thị trang mặc định
    show_page("Dashboard")

    # Khởi chạy ứng dụng
    root.mainloop()

if __name__ == "__main__":
    show_dashboard()
