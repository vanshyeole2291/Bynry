CREATE TABLE companies (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE warehouses (
    id BIGSERIAL PRIMARY KEY,
    company_id BIGINT NOT NULL REFERENCES companies(id),
    name VARCHAR(255) NOT NULL
);

CREATE TABLE products (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    sku VARCHAR(100) UNIQUE NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    low_stock_threshold INT DEFAULT 10,
    is_bundle BOOLEAN DEFAULT FALSE
);

CREATE TABLE inventory (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT NOT NULL REFERENCES products(id),
    warehouse_id BIGINT NOT NULL REFERENCES warehouses(id),
    quantity INT DEFAULT 0,
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE inventory_history (
    id BIGSERIAL PRIMARY KEY,
    inventory_id BIGINT NOT NULL REFERENCES inventory(id),
    change_amount INT NOT NULL,
    change_reason VARCHAR(255),
    changed_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE suppliers (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    contact_email VARCHAR(255)
);

CREATE TABLE product_suppliers (
    product_id BIGINT NOT NULL REFERENCES products(id),
    supplier_id BIGINT NOT NULL REFERENCES suppliers(id),
    PRIMARY KEY (product_id, supplier_id)
);

CREATE TABLE product_bundles (
    bundle_id BIGINT NOT NULL REFERENCES products(id),
    component_id BIGINT NOT NULL REFERENCES products(id),
    quantity INT NOT NULL DEFAULT 1,
    PRIMARY KEY (bundle_id, component_id)
);
