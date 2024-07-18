import mysql.connector
from mysql.connector import Error

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="btlpython"
    )

def fetch_all_employees():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT idnv, tennv FROM nhanvien")
    employees = cursor.fetchall()
    connection.close()
    return employees

def fetch_all_customers():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT idkh, tenkh FROM khachhang")
    customers = cursor.fetchall()
    connection.close()
    return customers

def fetch_all_products():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT idsp, tensp, giaban FROM sanpham")
    products = cursor.fetchall()
    connection.close()
    return products

def insert_sale(idsp, idkh, idnv, loaigd, soluong, gia, ngaymua):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO banhang (idsp, idkh, idnv, loaigd, soluong, thoigian, gia) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (idsp, idkh, idnv, loaigd, soluong, ngaymua, gia))
    connection.commit()
    connection.close()

def fetch_sales_history():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT banhang.idsp, sanpham.tensp, banhang.soluong, banhang.gia, banhang.thoigian, nhanvien.tennv, khachhang.tenkh
        FROM banhang
        JOIN sanpham ON banhang.idsp = sanpham.idsp
        JOIN nhanvien ON banhang.idnv = nhanvien.idnv
        JOIN khachhang ON banhang.idkh = khachhang.idkh
    """)
    sales_history = cursor.fetchall()
    connection.close()
    return sales_history
def delete_sales_history():
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM banhang")
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        connection.close()

# Fetch data from database
def fetch_data():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nhanvien")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Add employee
def add_employee(tennv, sdt, email, matkhau, chucvu, ngaybatdau, luong):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO nhanvien (tennv, sdt, email, matkhau, chucvu, ngaybatdau, luong) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (tennv, sdt, email, matkhau, chucvu, ngaybatdau, luong)
    cursor.execute(sql, values)
    conn.commit()
    conn.close()

# Edit employee
def edit_employee(idnv, tennv, sdt, email, matkhau, chucvu, ngaybatdau, luong):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "UPDATE nhanvien SET tennv=%s, sdt=%s, email=%s, matkhau=%s, chucvu=%s, ngaybatdau=%s, luong=%s WHERE idnv=%s"
    values = (tennv, sdt, email, matkhau, chucvu, ngaybatdau, luong, idnv)
    cursor.execute(sql, values)
    conn.commit()
    conn.close()

# Delete employee
def delete_employee(idnv):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "DELETE FROM nhanvien WHERE idnv=%s"
    cursor.execute(sql, (idnv,))
    conn.commit()
    conn.close()

# Search employee
def search_employee(keyword):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "SELECT * FROM nhanvien WHERE tennv LIKE %s"
    cursor.execute(sql, ('%' + keyword + '%',))
    rows = cursor.fetchall()
    conn.close()
    return rows

def fetch_all_product():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT idsp, tensp, thuonghieu, giaban, baohanh, mota FROM sanpham")
    rows = cursor.fetchall()
    conn.close()
    return rows

def insert_product(tensp, thuonghieu, giaban, baohanh, mota):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO sanpham (tensp, thuonghieu, giaban, baohanh, mota) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (tensp, thuonghieu, giaban, baohanh, mota))
    conn.commit()
    conn.close()

def delete_product(idsp):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "DELETE FROM sanpham WHERE idsp = %s"
    cursor.execute(sql, (idsp,))
    conn.commit()
    conn.close()

def update_product(idsp, tensp, thuonghieu, giaban, baohanh, mota):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "UPDATE sanpham SET tensp = %s, thuonghieu = %s, giaban = %s, baohanh = %s, mota = %s WHERE idsp = %s"
    cursor.execute(sql, (tensp, thuonghieu, giaban, baohanh, mota, idsp))
    conn.commit()
    conn.close()

def search_products(keyword):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "SELECT idsp, tensp, thuonghieu, giaban, baohanh, mota FROM sanpham WHERE tensp LIKE %s"
    cursor.execute(sql, ('%' + keyword + '%',))
    rows = cursor.fetchall()
    conn.close()
    return rows

# Function to add a new customer
def add_customer(tenkh, sdt, email, diachi):
    try:
        conn = get_connection()
        if conn is None:
            raise Exception("Database connection failed")
        cursor = conn.cursor()
        sql = "INSERT INTO khachhang (tenkh, sdt, email, diachi) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (tenkh, sdt, email, diachi))
        conn.commit()
        conn.close()
    except Error as e:
        print(f"Error adding customer: {e}")

# Function to update a customer
def update_customer(idkh, tenkh, sdt, email, diachi):
    try:
        conn = get_connection()
        if conn is None:
            raise Exception("Database connection failed")
        cursor = conn.cursor()
        sql = "UPDATE khachhang SET tenkh = %s, sdt = %s, email = %s, diachi = %s WHERE idkh = %s"
        cursor.execute(sql, (tenkh, sdt, email, diachi, idkh))
        conn.commit()
        conn.close()
    except Error as e:
        print(f"Error updating customer: {e}")

# Function to delete a customer
def delete_customer(idkh):
    try:
        conn = get_connection()
        if conn is None:
            raise Exception("Database connection failed")
        cursor = conn.cursor()
        sql = "DELETE FROM khachhang WHERE idkh = %s"
        cursor.execute(sql, (idkh,))
        conn.commit()
        conn.close()
    except Error as e:
        print(f"Error deleting customer: {e}")

# Function to search for customers
def search_customers(keyword):
    try:
        conn = get_connection()
        if conn is None:
            raise Exception("Database connection failed")
        cursor = conn.cursor()
        sql = "SELECT * FROM khachhang WHERE tenkh LIKE %s OR sdt LIKE %s OR email LIKE %s OR diachi LIKE %s"
        cursor.execute(sql, ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%'))
        results = cursor.fetchall()
        conn.close()
        return results
    except Error as e:
        print(f"Error searching customers: {e}")
        return []

# Function to get all customers
def get_all_customers():
    try:
        conn = get_connection()
        if conn is None:
            raise Exception("Database connection failed")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM khachhang")
        results = cursor.fetchall()
        conn.close()
        return results
    except Error as e:
        print(f"Error retrieving customers: {e}")
        return []


# Function to add a new warranty record
def add_warranty(idsp, idkh, ngaynhan, ngaytra, trangthai):
    try:
        conn = get_connection()
        if conn is None:
            raise Exception("Database connection failed")
        cursor = conn.cursor()
        sql = "INSERT INTO baohanh (idsp, idkh, ngaynhan, ngaytra, trangthai) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (idsp, idkh, ngaynhan, ngaytra, trangthai))
        conn.commit()
        conn.close()
    except Error as e:
        print(f"Error adding warranty: {e}")

# Function to update a warranty record
def update_warranty(idbaohanh, idsp, idkh, ngaynhan, ngaytra, trangthai):
    try:
        conn = get_connection()
        if conn is None:
            raise Exception("Database connection failed")
        cursor = conn.cursor()
        sql = "UPDATE baohanh SET idsp = %s, idkh = %s, ngaynhan = %s, ngaytra = %s, trangthai = %s WHERE idbaohanh = %s"
        cursor.execute(sql, (idsp, idkh, ngaynhan, ngaytra, trangthai, idbaohanh))
        conn.commit()
        conn.close()
    except Error as e:
        print(f"Error updating warranty: {e}")

# Function to delete a warranty record
def delete_warranty(idbaohanh):
    try:
        conn = get_connection()
        if conn is None:
            raise Exception("Database connection failed")
        cursor = conn.cursor()
        sql = "DELETE FROM baohanh WHERE idbaohanh = %s"
        cursor.execute(sql, (idbaohanh,))
        conn.commit()
        conn.close()
    except Error as e:
        print(f"Error deleting warranty: {e}")

# Function to search for warranty records
def search_warranties(keyword):
    try:
        conn = get_connection()
        if conn is None:
            raise Exception("Database connection failed")
        cursor = conn.cursor()
        sql = """
        SELECT * FROM baohanh 
        WHERE idsp LIKE %s OR idkh LIKE %s OR trangthai LIKE %s
        """
        cursor.execute(sql, ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%'))
        results = cursor.fetchall()
        conn.close()
        return results
    except Error as e:
        print(f"Error searching warranties: {e}")
        return []

# Function to get all warranty records
def get_all_warranties():
    try:
        conn = get_connection()
        if conn is None:
            raise Exception("Database connection failed")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM baohanh")
        results = cursor.fetchall()
        conn.close()
        return results
    except Error as e:
        print(f"Error retrieving warranties: {e}")
        return []

# Function to check if a customer exists
# Function to check if a product exists
def product_exists(idsp):
    try:
        conn = get_connection()
        if conn is None:
            raise Exception("Database connection failed")
        cursor = conn.cursor()
        sql = "SELECT COUNT(*) FROM sanpham WHERE idsp = %s"
        cursor.execute(sql, (idsp,))
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0
    except Error as e:
        print(f"Error checking product existence: {e}")
        return False

# Function to check if a customer exists
def customer_exists(idkh):
    try:
        conn = get_connection()
        if conn is None:
            raise Exception("Database connection failed")
        cursor = conn.cursor()
        sql = "SELECT COUNT(*) FROM khachhang WHERE idkh = %s"
        cursor.execute(sql, (idkh,))
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0
    except Error as e:
        print(f"Error checking customer existence: {e}")
        return False

