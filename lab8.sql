

-- Lab 8
-- Bài 1: So sánh Window Function với GROUP BY
--  thử viết một câu lệnh GROUP BY để lấy tên sản phẩm và giá trung bình.
SELECT product_name, AVG(price) as avg_price
FROM products
GROUP BY product_name;
--Sử dụng Window Function
SELECT 
    product_name, 
    price, 
    AVG(price) OVER () AS avg_overall_price
FROM products;

-- So sánh kết quả:
-- GROUP BY: Thu nhỏ số lượng hàng trả về. Nếu có 100 sản phẩm, kết quả có thể chỉ còn vài hàng 
--(nếu trùng tên) và bạn chỉ thấy dữ liệu của "nhóm" đó.
-- Window Function: Giữ nguyên số lượng hàng ban đầu (ví dụ 100 hàng sản phẩm). Nó tính toán dựa 
-- trên một "cửa sổ" dữ liệu nhưng không làm mất đi định danh của từng hàng.

--Bài 2: Phân tích trong từng nhóm với PARTITION BY.
--so sánh giá của một sản phẩm với giá trung bình của các sản phẩm trong cùng danh mục (category).
SELECT 
    supplier_id,
    product_name,
    price,
    AVG(price) OVER (PARTITION BY supplier_id) AS avg_supplier_price
FROM products;

--Ở Bài 1 (OVER ()): Cột giá trung bình là duy nhất cho tất cả các dòng.
--Ở Bài 2 (OVER (PARTITION BY ...)): Cột giá trung bình sẽ thay đổi tùy theo sản phẩm 
--đó thuộc nhóm nào.

--PHần II
-- Bài 3: Xếp hạng sản phẩm
-- 1. Chuẩn bị (Cập nhật dữ liệu để có giá bằng nhau)
UPDATE products SET price = 28000000 WHERE product_id = 1;
-- 2. Thực hành (Viết câu lệnh xếp hạng)
SELECT 
    product_name, 
    price,
    ROW_NUMBER() OVER (ORDER BY price DESC) AS row_num,
    RANK() OVER (ORDER BY price DESC) AS rank_num,
    DENSE_RANK() OVER (ORDER BY price DESC) AS dense_rank_num
FROM products;

--Sự khác biệt:
--ROW_NUMBER(): Đánh số thứ tự liên tục và duy nhất cho mỗi hàng. Ngay cả khi giá bằng nhau 
--nó vẫn tăng số (1, 2, 3...). Không bao giờ có hai hàng trùng số nhau.

--RANK(): Các hàng có cùng giá trị sẽ nhận cùng một thứ hạng. Tuy nhiên, nó sẽ nhảy cóc số thứ 
--tự phía sau. (Ví dụ: có hai vị trí số 1, thì vị trí tiếp theo sẽ nhảy thẳng lên số 3,bỏquasố2).

--DENSE_RANK(): Các hàng cùng giá trị cũng nhận cùng một thứ hạng, nhưng nó không nhảy cóc số.

-- Bài 4: Tính tổng lũy kế doanh thu theo ngày.
-- Sử dụng các hàm tổng hợp như SUM()trên một cửa sổ được sắp xếp để tính toán các giá trị lũy kế 
--(running total).
-- Bước 1: Tính tổng doanh thu cho mỗi ngày
WITH daily_revenue AS (
    SELECT 
        DATE(o.order_date) AS order_day, 
        SUM(od.quantity * od.unit_price) AS total_daily_revenue
    FROM orders o
    JOIN order_details od ON o.order_id = od.order_id
    GROUP BY DATE(o.order_date)
)
-- Bước 2: Tính tổng lũy kế (Running Total)
SELECT 
    order_day,
    total_daily_revenue,
    SUM(total_daily_revenue) OVER (ORDER BY order_day) AS running_total_revenue
FROM daily_revenue
ORDER BY order_day;
