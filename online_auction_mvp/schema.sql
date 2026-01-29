


CREATE DATABASE IF NOT EXISTS auction_db;
USE auction_db;


CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    role ENUM('buyer', 'seller') NOT NULL
);


CREATE TABLE IF NOT EXISTS items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL,
    description TEXT,
    base_price FLOAT NOT NULL,
    seller_id INT,
    FOREIGN KEY (seller_id) REFERENCES users(user_id)
);


CREATE TABLE IF NOT EXISTS bids (
    bid_id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT,
    buyer_id INT,
    bid_amount FLOAT NOT NULL,
    bid_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES items(item_id),
    FOREIGN KEY (buyer_id) REFERENCES users(user_id)
);


CREATE INDEX idx_items_seller_id ON items(seller_id);
CREATE INDEX idx_bids_item_id ON bids(item_id);
CREATE INDEX idx_bids_buyer_id ON bids(buyer_id);
CREATE INDEX idx_bids_bid_time ON bids(bid_time);