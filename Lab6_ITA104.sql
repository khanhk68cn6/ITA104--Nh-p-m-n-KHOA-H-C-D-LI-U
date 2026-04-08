
-- Lab 6
-- Phần I
--Bài 1: Tổng quan thống kê về sản phẩm
SELECT
    COUNT(MaSP) AS "SoLuongSanPham",
    AVG(DonGiaNiemYet) AS "GiaTrungBinh",
    MIN(DonGiaNiemYet) AS "GiaThapNhat",
    MAX(DonGiaNiemYet) AS "GiaCaoNhat"
FROM SanPham;
--Bài 2: Phân tích nhà cung cấp
SELECT 
     n. TenNCC,
	 COUNT(s.MaSP) as "TongSoSanPham"
From NhaCungCap n
JOIN SanPham s On n.MaNCC = s.MaNCC
GROUP By n.TenNCC
HAVING COUNT (s.MaSP) > 1;
-- Phần II
-- Bài 3: Xử lý và định dạng ngày đặt hàng
SELECT 
   MaHD, 
   TO_CHAR(NgayHD, 'DD/MM/YYYY') AS "NgayDinhDang"
FROM HoaDon
WHERE 
    EXTRACT(MONTH FROM NgayHD) = 10 
    AND EXTRACT(YEAR FROM NgayHD) = 2023;
-- Bai 4: Báo cáo doanh thu theo khách hàng
SELECT 
    k.TenKH, 
    SUM(c.SoLuong * c.DonGiaBan) AS TongChiTieu
FROM KhachHang k
JOIN HoaDon h ON k.MaKH = h.MaKH
JOIN ChiTietHoaDon c ON h.MaHD = c.MaHD
GROUP BY k.TenKH
HAVING SUM(c.SoLuong * c.DonGiaBan) > 100000
ORDER BY TongChiTieu DESC;
