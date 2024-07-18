CREATE DATABASE btlpython;

USE btlpython;

CREATE TABLE sanpham (
    idsp INT PRIMARY KEY AUTO_INCREMENT,
    tensp VARCHAR(100) NOT NULL,
    thuonghieu VARCHAR(50),
    giaban FLOAT,
    baohanh INT,
    mota TEXT
);

CREATE TABLE nhanvien (
    idnv INT PRIMARY KEY AUTO_INCREMENT,
    tennv VARCHAR(50) NOT NULL,
    sdt VARCHAR(20),
    email VARCHAR(100),
    matkhau VARCHAR(20),
    chucvu VARCHAR(50),
    ngaybatdau DATE,
    luong FLOAT
);

CREATE TABLE khachhang (
    idkh INT PRIMARY KEY AUTO_INCREMENT,
    tenkh VARCHAR(50) NOT NULL,
    sdt VARCHAR(20),
    email VARCHAR(100),
    diachi VARCHAR(255)
);

CREATE TABLE khohang (
    idkho INT PRIMARY KEY AUTO_INCREMENT,
    idsp INT,
    tensp VARCHAR(100),
    soluong INT,
    tondau INT,
    nhapxuat INT,
    tenkho VARCHAR(50),
    capnhap DATETIME,
    FOREIGN KEY (idsp) REFERENCES sanpham(idsp)
);

CREATE TABLE banhang (
    idbanhang INT PRIMARY KEY AUTO_INCREMENT,
    idsp INT,
    idkh INT,
    idnv INT,
    loaigd VARCHAR(10), 
    soluong INT,
    thoigian DATE,
    gia FLOAT,
    FOREIGN KEY (idsp) REFERENCES sanpham(idsp),
    FOREIGN KEY (idkh) REFERENCES khachhang(idkh),
    FOREIGN KEY (idnv) REFERENCES nhanvien(idnv)
);

CREATE TABLE baohanh (
    idbaohanh INT PRIMARY KEY AUTO_INCREMENT,
    idsp INT,
    idkh INT,
    ngaynhan DATE,
    ngaytra DATE,
    trangthai VARCHAR(50),
    FOREIGN KEY (idsp) REFERENCES sanpham(idsp),
    FOREIGN KEY (idkh) REFERENCES khachhang(idkh)
);

CREATE TABLE doanhthu (
    iddt INT PRIMARY KEY AUTO_INCREMENT,
    idgd INT,
    ngay DATE,
    tongdt FLOAT,
    FOREIGN KEY (idgd) REFERENCES banhang(idbanhang)
);
