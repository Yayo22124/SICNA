CREATE TABLE IF NOT EXISTS tbb_products(
    code INT(4) UNSIGNED ZEROFILL NOT NULL,
    name CHAR(50),
    stock INT NOT NULL,
    value FLOAT,
    id_category tinyint NULL,
    PRIMARY KEY(code)
);

CREATE TABLE IF NOT EXISTS tbb_categories(
    id tinyint NOT NULL,
    name CHAR(40) NOT NULL,
    description VARCHAR(200),
    PRIMARY KEY(id)
);

ALTER TABLE products ADD FOREIGN KEY(id_category) REFERENCES categories(id);