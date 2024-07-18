import mysql.connector


def fetch_sales_data():
    try:
        # Kết nối tới cơ sở dữ liệu
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='btlpython'
        )

        # Nếu kết nối thành công, thực hiện truy vấn
        if conn.is_connected():
            query = """
            SELECT thoigian, SUM(gia * soluong) AS doanh_thu, SUM(soluong) AS so_luong
            FROM banhang
            GROUP BY thoigian
            ORDER BY thoigian
            """

            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            result = cursor.fetchall()

            # Đóng cursor và kết nối
            cursor.close()
            conn.close()

            return result
        else:
            print("Không thể kết nối tới cơ sở dữ liệu.")
            return []

    except mysql.connector.Error as err:
        print(f"Lỗi: {err}")
        return []

def fetch_counts():
    try:
        # Kết nối tới cơ sở dữ liệu MySQL
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="btlpython"
        )

        cursor = connection.cursor()

        # Đếm số lượng sản phẩm
        cursor.execute("SELECT COUNT(*) FROM sanpham")
        product_count = cursor.fetchone()[0]

        # Đếm số lượng nhân viên
        cursor.execute("SELECT COUNT(*) FROM nhanvien")
        employee_count = cursor.fetchone()[0]

        # Đếm số lượng khách hàng
        cursor.execute("SELECT COUNT(*) FROM khachhang")
        customer_count = cursor.fetchone()[0]

        # Đếm số lượng đơn bảo hành
        cursor.execute("SELECT COUNT(*) FROM baohanh")
        baohanh_count = cursor.fetchone()[0]

        return product_count, employee_count, customer_count, baohanh_count

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None, None, None, None

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()