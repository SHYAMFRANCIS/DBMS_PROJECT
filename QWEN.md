# Online Auction Management System - QWEN.md

## Project Overview

This is an **Online Auction Management System** built with Python, MySQL, and Streamlit. The application allows users to register as either buyers or sellers, with role-based dashboards that provide different functionality:

- **Sellers** can list items for auction, view their listings, and see bids placed on their items
- **Buyers** can browse available auction items, place bids, and view their bidding history

The system is built using a Streamlit frontend with a Python backend that handles MySQL database operations, including user authentication, item listings, and bid management.

## Architecture

- **Frontend**: Streamlit web application
- **Backend**: Python with MySQL connector
- **Database**: MySQL with three main tables (users, items, bids)
- **Authentication**: Secure password hashing using bcrypt

## Key Files

- `app.py` - Main Streamlit application with user interface and session state management
- `db_config.py` - Database connection and all CRUD operations for users, items, and bids
- `schema.sql` - MySQL database schema and table creation script
- `requirements.txt` - Python dependencies
- `README.md` - Project documentation

## Database Schema

The application uses three main tables:

1. **users** - Stores user information (user_id, name, email, hashed password, role)
2. **items** - Stores auction items (item_id, name, description, base_price, seller_id)
3. **bids** - Stores bid information (bid_id, item_id, buyer_id, bid_amount, bid_time)

The schema includes foreign key constraints and indexes for performance optimization.

## Building and Running

### Prerequisites

- Python 3.7+
- MySQL Server
- pip (Python package manager)

### Setup Commands

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up MySQL database:**
   - Ensure MySQL server is running
   - Update database credentials in `db_config.py` if needed
   - Execute the schema file to create the database and tables:
     ```sql
     mysql -u root -p < schema.sql
     ```
     Or connect to MySQL and run:
     ```sql
     CREATE DATABASE auction_db;
     USE auction_db;
     SOURCE schema.sql;
     ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

### Default Database Configuration

The application expects a MySQL database named `auction_db` with the following default settings in `db_config.py`:
- Host: localhost
- Database: auction_db
- Username: root
- Password: 12345678 (Note: This is hardcoded in the current config)
- Port: 3306

### Features

- User authentication (register/login with password hashing)
- Role-based dashboards (buyer/seller)
- Item listing and browsing
- Real-time bidding system with validation (bids must be higher than current highest bid)
- Bid tracking and history
- CSV export for reports
- Secure password hashing with bcrypt

### Development Notes

The application uses Streamlit's session state for managing user authentication and navigation between pages. All database operations are handled through functions in `db_config.py` with proper connection management and error handling.

The application follows a clear separation of concerns:
- `app.py` handles user interface and navigation logic
- `db_config.py` handles all database operations and business logic
- `schema.sql` defines the database structure

### Security Considerations

- Passwords are hashed using bcrypt before storage
- Input validation is implemented for forms
- SQL queries use parameterized statements to prevent injection attacks

### Dependencies

The project requires the following Python packages:
- streamlit
- mysql-connector-python
- pandas
- bcrypt
- python-dotenv

### Testing

To test the application:
1. Register a new user account (as either buyer or seller)
2. Login with the registered credentials
3. Use the appropriate dashboard functionality based on user role
4. For sellers: add items and view bids on their items
5. For buyers: browse items and place bids (ensuring bid amounts are higher than current highest bid)