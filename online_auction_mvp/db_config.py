import mysql.connector
from mysql.connector import Error
import bcrypt
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'auction_db'),
    'user': os.getenv('DB_USER', 'root'),  
    'password': os.getenv('DB_PASSWORD', '12345678'),  # Default for backward compatibility, but recommend using env file
    'port': int(os.getenv('DB_PORT', 3306))
}

def create_connection():
    """
    Create a connection to the MySQL database
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

def register_user(name, email, password, role):
    """
    Register a new user with hashed password
    """
    connection = create_connection()
    if connection is None:
        return False, "Database connection failed"
    
    try:
        cursor = connection.cursor()
       
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        
        query = "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, email, hashed_password.decode('utf-8'), role))
        connection.commit()
        
        return True, "User registered successfully"
    except Error as e:
        if e.errno == 1062:  
            return False, "Email already exists"
        return False, f"Error registering user: {e}"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def login_user(email, password):
    """
    Authenticate user login
    """
    connection = create_connection()
    if connection is None:
        return None, "Database connection failed"
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()
        
        if user:
            
            if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                return user, "Login successful"
            else:
                return None, "Incorrect password"
        else:
            return None, "User not found"
    except Error as e:
        return None, f"Error during login: {e}"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def add_item(item_name, description, base_price, seller_id):
    """
    Add a new item for auction
    """
    connection = create_connection()
    if connection is None:
        return False, "Database connection failed"
    
    try:
        cursor = connection.cursor()
        
        
        query = "INSERT INTO items (item_name, description, base_price, seller_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (item_name, description, base_price, seller_id))
        connection.commit()
        
        return True, "Item added successfully"
    except Error as e:
        return False, f"Error adding item: {e}"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def view_items():
    """
    View all items available for auction
    """
    connection = create_connection()
    if connection is None:
        return [], "Database connection failed"
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT i.item_id, i.item_name, i.description, i.base_price, u.name as seller_name
        FROM items i
        JOIN users u ON i.seller_id = u.user_id
        ORDER BY i.item_id
        """
        cursor.execute(query)
        items = cursor.fetchall()
        return items, "Items retrieved successfully"
    except Error as e:
        return [], f"Error retrieving items: {e}"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_item_by_id(item_id):
    """
    Get a specific item by its ID
    """
    connection = create_connection()
    if connection is None:
        return None, "Database connection failed"
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT i.*, u.name as seller_name
        FROM items i
        JOIN users u ON i.seller_id = u.user_id
        WHERE i.item_id = %s
        """
        cursor.execute(query, (item_id,))
        item = cursor.fetchone()
        return item, "Item retrieved successfully"
    except Error as e:
        return None, f"Error retrieving item: {e}"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def place_bid(item_id, buyer_id, bid_amount):
    """
    Place a bid on an item
    """
    connection = create_connection()
    if connection is None:
        return False, "Database connection failed"
    
    try:
        cursor = connection.cursor()
        
       
        item_query = "SELECT base_price FROM items WHERE item_id = %s"
        cursor.execute(item_query, (item_id,))
        item = cursor.fetchone()
        
        if not item:
            return False, "Item does not exist"
        
       
        if bid_amount <= item[0]:
            return False, f"Bid must be higher than base price of {item[0]}"
        
        
        bid_query = "SELECT MAX(bid_amount) as max_bid FROM bids WHERE item_id = %s"
        cursor.execute(bid_query, (item_id,))
        result = cursor.fetchone()
        max_bid = result[0]
        
        if max_bid is not None and bid_amount <= max_bid:
            return False, f"Bid must be higher than current highest bid of {max_bid}"
        
       
        query = "INSERT INTO bids (item_id, buyer_id, bid_amount) VALUES (%s, %s, %s)"
        cursor.execute(query, (item_id, buyer_id, bid_amount))
        connection.commit()
        
        return True, "Bid placed successfully"
    except Error as e:
        return False, f"Error placing bid: {e}"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_bids_for_item(item_id):
    """
    Get all bids for a specific item
    """
    connection = create_connection()
    if connection is None:
        return [], "Database connection failed"
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT b.*, u.name as buyer_name
        FROM bids b
        JOIN users u ON b.buyer_id = u.user_id
        WHERE b.item_id = %s
        ORDER BY b.bid_amount DESC
        """
        cursor.execute(query, (item_id,))
        bids = cursor.fetchall()
        return bids, "Bids retrieved successfully"
    except Error as e:
        return [], f"Error retrieving bids: {e}"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_bids_by_user(user_id):
    """
    Get all bids placed by a specific user
    """
    connection = create_connection()
    if connection is None:
        return [], "Database connection failed"
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT b.*, i.item_name
        FROM bids b
        JOIN items i ON b.item_id = i.item_id
        WHERE b.buyer_id = %s
        ORDER BY b.bid_time DESC
        """
        cursor.execute(query, (user_id,))
        bids = cursor.fetchall()
        return bids, "Bids retrieved successfully"
    except Error as e:
        return [], f"Error retrieving bids: {e}"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_items_by_seller(seller_id):
    """
    Get all items listed by a specific seller
    """
    connection = create_connection()
    if connection is None:
        return [], "Database connection failed"
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT i.item_id, i.item_name, i.description, i.base_price, i.seller_id
        FROM items i
        WHERE i.seller_id = %s
        ORDER BY i.item_id
        """
        cursor.execute(query, (seller_id,))
        items = cursor.fetchall()
        return items, "Items retrieved successfully"
    except Error as e:
        return [], f"Error retrieving items: {e}"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_item_bids_by_seller(seller_id):
    """
    Get all bids placed on items listed by a specific seller
    """
    connection = create_connection()
    if connection is None:
        return [], "Database connection failed"
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT b.*, i.item_name, u.name as buyer_name
        FROM bids b
        JOIN items i ON b.item_id = i.item_id
        JOIN users u ON b.buyer_id = u.user_id
        WHERE i.seller_id = %s
        ORDER BY b.bid_time DESC
        """
        cursor.execute(query, (seller_id,))
        bids = cursor.fetchall()
        return bids, "Bids retrieved successfully"
    except Error as e:
        return [], f"Error retrieving bids: {e}"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def highest_bids():
    """
    Get the highest bid for each item
    """
    connection = create_connection()
    if connection is None:
        return [], "Database connection failed"
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT i.item_name, i.item_id, u.name as buyer_name, b.bid_amount, b.bid_time
        FROM items i
        LEFT JOIN (
            SELECT item_id, MAX(bid_amount) as max_bid
            FROM bids
            GROUP BY item_id
        ) max_bids ON i.item_id = max_bids.item_id
        LEFT JOIN bids b ON i.item_id = b.item_id AND b.bid_amount = max_bids.max_bid
        LEFT JOIN users u ON b.buyer_id = u.user_id
        ORDER BY b.bid_amount DESC
        """
        cursor.execute(query)
        highest_bids = cursor.fetchall()
        return highest_bids, "Highest bids retrieved successfully"
    except Error as e:
        return [], f"Error retrieving highest bids: {e}"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_user_by_id(user_id):
    """
    Get user details by ID
    """
    connection = create_connection()
    if connection is None:
        return None, "Database connection failed"
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT user_id, name, email, role FROM users WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()
        return user, "User retrieved successfully"
    except Error as e:
        return None, f"Error retrieving user: {e}"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()