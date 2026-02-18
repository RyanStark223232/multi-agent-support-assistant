DROP TABLE IF EXISTS tickets;
DROP TABLE IF EXISTS customers;

-- Customers table
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    segment TEXT,
    created_at TEXT
);

-- Support tickets table
CREATE TABLE tickets (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    subject TEXT NOT NULL,
    description TEXT,
    status TEXT,
    created_at TEXT,
    resolved_at TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);