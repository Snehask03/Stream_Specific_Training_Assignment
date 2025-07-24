use BikeStores

-- Assignment Question

-- Day 1
select * from production.products
select * from production.categories
select * from production.brands
select * from sales.order_items

/*
1.Create a product catalog view with price the marketing team needs a view of active products model_year>=2018)
Along with brand, category and price 
Show the product_id, product_name, brand_name, category_name, list_price
Display the view using the order by category_name and product_name
*/
create view ProductCatalog as
select p.product_id, p.product_name, b.brand_name, c.category_name, p.model_year, p.list_price
from production.brands b
join production.products p on p.brand_id = b.brand_id
join production.categories c on c.category_id = p.category_id
where p.model_year > 2018

select * from ProductCatalog
order by product_name, category_name


--2. The inventory team wants to identify products that haven't been sold. Create a view listing all products that have zero sales.
create view productswithzerosales as 
select p.product_id, p.product_name, p.model_year, p.list_price
from production.products p 
left join sales.order_items oi on p.product_id = oi.product_id
where oi.product_id is null

select * from productswithzerosales

/*3.
Write a query that:
Ranks products within each category by list price (highest first)
Returns only the first product per category
Expected Output:
category_name, product_name, list_price — only one row per category
*/

with Rankedproducts as (
	select c.category_name,p.product_name, p.list_price,
	ROW_NUMBER() over(partition by c.category_name order by p.list_price desc) as rn
	from production.products p
	join production.categories c on p.category_id = c.category_id

)
select category_name, product_name, list_price 
from RankedProducts
where rn = 1

-- Day 2
-- 1.Write a scalar-valued function that takes a product_id as input and returns the list_price of that product.
CREATE FUNCTION ProductWithPrice
(@productid int)
RETURNS DECIMAL(10,2)
AS 
BEGIN
DECLARE @price DECIMAL(10,2)
SELECT @price = list_price FROM production.products WHERE product_id = @productid
RETURN @price
END

SELECT dbo.ProductWithPrice(1)

-- 2.Write an inline table-valued function that returns all products for a given category_id.
select * from production.products
CREATE FUNCTION GetSameCategoryProduct
(@categoryid int)
RETURNS TABLE
AS
RETURN (SELECT * FROM production.products WHERE category_id = @categoryid)

SELECT * FROM dbo.GetSameCategoryProduct(6)

/*
3.Create a function that takes a store_id and returns the total sales amount for that store.
Use the sales.orders and sales.order_items tables. Sum the list_price * quantity for all orders from that store.
*/
CREATE FUNCTION GetTotalSales
(@storeid int)
RETURNS TABLE
AS
RETURN (SELECT s.store_id, SUM(oi.quantity * oi.list_price) AS total_sales_amount
		FROM sales.orders o 
		JOIN sales.order_items oi on o.order_id = oi.order_id
		JOIN sales.stores s on o.store_id = s.store_id
		WHERE o.store_id = @storeid
		GROUP BY s.store_id)

SELECT * FROM dbo.GetTotalSales(2)
select * from sales.orders

-- 4.Write a table-valued function that takes two dates as input and returns all orders placed between those dates.
CREATE FUNCTION GetAllOrdersPlacedInBetween
(@startdate date,
@enddate date)
RETURNS TABLE
AS
RETURN (SELECT * FROM sales.orders WHERE order_date BETWEEN @startdate AND @enddate)

SELECT * FROM dbo.GetAllOrdersPlacedInBetween('2016-01-01', '2016-03-30')

-- 5.Write a function that takes a brand_id and returns the number of products for that brand.
CREATE FUNCTION GetBrandProductsCount
(@brandid int)
RETURNS int
AS
BEGIN
DECLARE @count int
SELECT @count = count(product_id) FROM production.products WHERE brand_id = @brandid
RETURN @count
END

SELECT dbo.GetBrandProductsCount(9)

-- Day 3
/*
1. Create a trigger that logs any update to the list_price of a product in the production.products table.
in a new table price_change_log
logid
    product_id 
    old_price
    new_price   
  change_date
*/
CREATE TABLE price_change_log(
logid int identity(1,1) primary key,
product_id int,
old_price decimal(10, 2),
new_price decimal(10, 2),
change_date datetime default getdate()
)

CREATE TRIGGER trg_price_change
ON 
production.products
AFTER UPDATE
AS 
BEGIN
	INSERT INTO price_change_log(product_id, old_price, new_price, change_date)
	SELECT d.product_id, d.list_price as old_price, i.list_price as new_price, GETDATE()
	FROM deleted d 
	JOIN inserted i on d.product_id = i.product_id
	WHERE d.list_price <> i.list_price
END
select * from production.products
UPDATE production.products SET list_price = list_price + 10 WHERE product_id = 1
select * from dbo.price_change_log

-- 2. Create a trigger that Prevent deletion of a product if it exists in any open order.
select *  from sales.orders
CREATE TRIGGER trg_prevent_product_deletion
ON production.products
INSTEAD OF DELETE
AS 
BEGIN
	IF EXISTS(
		SELECT 1 FROM deleted d
		JOIN sales.order_items oi ON d.product_id = oi.product_id
		JOIN sales.orders o on oi.order_id = o.order_id
		WHERE o.order_status IN (1,2)
		)
		BEGIN
		PRINT 'Cannot Delete the product because it exists in an open order'
		RETURN
		END
	DELETE FROM production.products 
	WHERE product_id IN (SELECT product_id FROM deleted)
END

-- SQL ASSIGNMENTS FINAL
/*
1.Total Sales by Store (Only High-Performing Stores)
List each store's name and the total sales amount (sum of quantity × list price) 
for all orders. Only include stores where the total sales amount exceeds $50,000.
*/
SELECT s.store_name , sum(oi.quantity*oi.list_price) as total_sales
FROM sales.orders o
JOIN sales.order_items oi on o.order_id = oi.order_id
JOIN sales.stores s on o.store_id = s.store_id
GROUP BY s.store_name
HAVING SUM(oi.quantity * oi.list_price) > 50000

-- 2.Top Selling Products by Quantity 
-- Find the top 5 best-selling products by total quantity ordered.
select * from sales.order_items
select * from production.products
SELECT TOP 5 p.product_name, sum(oi.quantity) as total_quantity_sold
FROM sales.order_items oi
JOIN production.products p
on p.product_id = oi.product_id
GROUP BY p.product_name
ORDER BY total_quantity_sold desc

-- 3.how monthly sales totals (sum of line total) for the year 2016.
Select MONTH(o.order_date) as Sales_Month, sum(oi.list_price * oi.quantity) as Total_Monthly_Sales
from production.products p 
Join sales.order_items oi on p.product_id = oi.product_id
join sales.orders o on oi.order_id = o.order_id
where YEAR(o.order_date) = 2016
group by MONTH(o.order_date)

-- 4. High Revenue Stores List all stores whose total revenue is greater than ₹100,000
Select s.store_name, sum(oi.list_price * oi.quantity) as Total_Revenue
from sales.stores s 
join sales.orders o on s.store_id = o.store_id
join sales.order_items oi on o.order_id = oi.order_id
group by s.store_name
having sum(oi.list_price * oi.quantity) > 100000
