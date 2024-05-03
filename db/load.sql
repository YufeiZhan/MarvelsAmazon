\COPY Users FROM 'Users.csv' WITH DELIMITER ',' NULL '' CSV
-- since id is auto-generated; we need the next command to adjust the counter
-- for auto-generation so next INSERT will not clash with ids loaded above:
SELECT pg_catalog.setval('public.Users_uid_seq',
                         (SELECT MAX(Users.uid)+1 FROM Users),
                         false);

\COPY Products FROM 'Products.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.Products_pid_seq',
                         (SELECT MAX(Products.pid)+1 FROM Products),
                         false);

\COPY Inventory FROM 'Inventory.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.Inventory_iid_seq',
                         (SELECT MAX(Inventory.iid)+1 FROM Inventory),
                         false);

\COPY CartItems FROM 'CartItems.csv' WITH DELIMITER ',' NULL '' CSV
                         
\COPY Orders FROM 'Orders.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.Orders_oid_seq',
                         (SELECT MAX(Orders.oid)+1 FROM Orders),
                         false);

\COPY OrderItems FROM 'OrderItems.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.OrderItems_oiid_seq',
                         (SELECT MAX(OrderItems.oiid)+1 FROM OrderItems),
                         false);

\COPY BalanceHistory FROM 'BalanceHistory.csv' WITH DELIMITER ',' NULL '' CSV;

\COPY Coupon FROM 'Coupon.csv' WITH DELIMITER ',' NULL '' CSV;

\COPY SellerReview FROM 'SellerReview.csv' WITH DELIMITER ',' NULL '' CSV;                                                                                                    

\COPY ProductReview FROM 'ProductReview.csv' WITH DELIMITER ',' NULL '' CSV;                                                                                                    

\COPY Upvotes FROM 'Upvotes.csv' WITH DELIMITER ',' NULL '' CSV;                                                                                                    
