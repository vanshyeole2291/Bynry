INSERT INTO companies (name) VALUES ('Test Company');
INSERT INTO warehouses (company_id, name) VALUES (1, 'Main Warehouse');
INSERT INTO products (name, sku, price, low_stock_threshold) VALUES ('Widget A', 'WID-001', 100.00, 20);
INSERT INTO inventory (product_id, warehouse_id, quantity) VALUES (1, 1, 5);
INSERT INTO suppliers (name, contact_email) VALUES ('Supplier Corp', 'orders@supplier.com');
INSERT INTO product_suppliers (product_id, supplier_id) VALUES (1, 1);
