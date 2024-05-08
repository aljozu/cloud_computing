-- Use the BOSTON database
\c BOSTON
CREATE TABLE IF NOT EXISTS product (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE,
    description TEXT,
    price NUMERIC,
    stock INTEGER
);