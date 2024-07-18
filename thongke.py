import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from databasetk import fetch_counts, fetch_sales_data


def create_bar_chart(data):
    """Vẽ biểu đồ hình cột cho doanh thu và số lượng sản phẩm theo ngày."""
    dates = [entry['thoigian'] for entry in data]
    revenues = [entry['doanh_thu'] for entry in data]
    quantities = [entry['so_luong'] for entry in data]

    fig, ax1 = plt.subplots(figsize=(14, 8))  # Tăng kích thước biểu đồ

    bar_width = 0.4
    index = range(len(dates))

    # Vẽ các cột cho doanh thu và số lượng
    bar1 = ax1.bar(index, revenues, bar_width, color='blue', label='Doanh thu')
    ax2 = ax1.twinx()
    bar2 = ax2.bar([i + bar_width for i in index], quantities, bar_width, color='red', label='Số lượng')

    # Thiết lập nhãn và tiêu đề
    ax1.set_xlabel('Ngày')
    ax1.set_ylabel('Doanh thu (VNĐ)', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax2.set_ylabel('Số lượng', color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    ax1.set_xticks([i + bar_width / 2 for i in index])
    ax1.set_xticklabels(dates, rotation=45, ha='right')

    # Thêm số liệu trên mỗi cột
    for bar in bar1:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2, yval, f'{yval:.2f}', ha='center', va='bottom')

    for bar in bar2:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width() / 2, yval, f'{yval}', ha='center', va='bottom')

    # Thêm chú giải (legend)
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    fig.tight_layout()
    return fig


def show_thongke(main_frame):
    def reset_statistics():
        for widget in main_frame.winfo_children():
            widget.destroy()
        show_thongke(main_frame)

    # Xóa các widget hiện tại trong main_frame
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Lấy số liệu thống kê
    try:
        product_count, employee_count, customer_count, baohanh_count = fetch_counts()
    except Exception as e:
        product_count = employee_count = customer_count = baohanh_count = "N/A"
        print(f"Error fetching counts: {e}")

    # Định nghĩa font chữ đậm màu đen
    font_style = ("Arial", 18, "bold")

    # Khung chứa thống kê
    stats_container = ctk.CTkFrame(main_frame, corner_radius=10, fg_color="#f0f0f0")
    stats_container.pack(pady=10, padx=10, fill=ctk.X)

    # Khung hiển thị số liệu sản phẩm
    stats_frame_product = ctk.CTkFrame(stats_container, fg_color="lightblue", corner_radius=10)
    stats_frame_product.pack(side=ctk.LEFT, padx=10, pady=10, expand=True, fill=ctk.BOTH)

    product_count_label = ctk.CTkLabel(stats_frame_product, text=f"Số lượng sản phẩm: {product_count}", font=font_style,
                                       text_color="black")
    product_count_label.pack(pady=20, padx=20)

    # Khung hiển thị số liệu nhân viên
    stats_frame_employee = ctk.CTkFrame(stats_container, fg_color="lightgreen", corner_radius=10)
    stats_frame_employee.pack(side=ctk.LEFT, padx=10, pady=10, expand=True, fill=ctk.BOTH)

    employee_count_label = ctk.CTkLabel(stats_frame_employee, text=f"Số lượng nhân viên: {employee_count}",
                                        font=font_style, text_color="black")
    employee_count_label.pack(pady=20, padx=20)

    # Khung hiển thị số liệu khách hàng
    stats_frame_customer = ctk.CTkFrame(stats_container, fg_color="lightcoral", corner_radius=10)
    stats_frame_customer.pack(side=ctk.LEFT, padx=10, pady=10, expand=True, fill=ctk.BOTH)

    customer_count_label = ctk.CTkLabel(stats_frame_customer, text=f"Số lượng khách hàng: {customer_count}",
                                        font=font_style, text_color="black")
    customer_count_label.pack(pady=20, padx=20)

    # Khung hiển thị số liệu đơn bảo hành
    stats_frame_baohanh = ctk.CTkFrame(stats_container, fg_color="lightyellow", corner_radius=10)
    stats_frame_baohanh.pack(side=ctk.LEFT, padx=10, pady=10, expand=True, fill=ctk.BOTH)

    baohanh_count_label = ctk.CTkLabel(stats_frame_baohanh, text=f"Số lượng đơn bảo hành: {baohanh_count}",
                                       font=font_style, text_color="black")
    baohanh_count_label.pack(pady=20, padx=20)

    # Lấy dữ liệu để vẽ biểu đồ
    try:
        sales_data = fetch_sales_data()
    except Exception as e:
        sales_data = []
        print(f"Error fetching sales data: {e}")

    # Tính tổng doanh thu và tổng số lượng sản phẩm đã bán
    total_revenue = sum(entry['doanh_thu'] for entry in sales_data) if sales_data else 0
    total_quantity_sold = sum(entry['so_luong'] for entry in sales_data) if sales_data else 0

    # Hiển thị tổng doanh thu
    total_revenue_label = ctk.CTkLabel(main_frame, text=f"Tổng doanh thu: {total_revenue:.2f} VNĐ", font=font_style,
                                       text_color="black")
    total_revenue_label.pack(pady=10)

    # Hiển thị tổng số sản phẩm đã bán
    total_quantity_label = ctk.CTkLabel(main_frame, text=f"Tổng số thiết bị di động đã bán: {total_quantity_sold}", font=font_style,
                                        text_color="black")
    total_quantity_label.pack(pady=10)

    # Khung chứa biểu đồ
    chart_frame = ctk.CTkFrame(main_frame, corner_radius=10, fg_color="#f0f0f0")
    chart_frame.pack(pady=20, padx=10, fill=ctk.BOTH, expand=True)

    if sales_data:
        fig = create_bar_chart(sales_data)
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    else:
        no_data_label = ctk.CTkLabel(chart_frame, text="Không có dữ liệu để hiển thị biểu đồ.",
                                     font=("Arial", 16, "bold"), text_color="red")
        no_data_label.pack(pady=20)

    # Cập nhật hiển thị
    main_frame.update_idletasks()
