# Online Auction Management System - Setup Guide

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Database Setup](#database-setup)
4. [Running the Application](#running-the-application)
5. [Connecting MySQL Workbench](#connecting-mysql-workbench)
6. [Troubleshooting](#troubleshooting)

## Prerequisites

Before setting up the application, ensure you have the following installed on your system:

- Python 3.7 or higher
- MySQL Server (8.0 or higher recommended)
- MySQL Workbench (optional, for database management)
- Git (optional, for cloning the repository)

## Installation

1. Clone the repository (if not already done):
   ```bash
   git clone https://github.com/yourusername/online-auction-mvp.git
   cd online-auction-mvp
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Database Setup

1. Ensure MySQL Server is running on your system.

2. Create the database and tables by running the schema script:
   ```sql
   mysql -u root -p < schema.sql
   ```
   
   Or connect to MySQL and run:
   ```sql
   CREATE DATABASE auction_db;
   USE auction_db;
   SOURCE schema.sql;
   ```

3. Update database credentials in `db_config.py` if needed:
   - Host: localhost (default)
   - Database: auction_db (default)
   - Username: root (default)
   - Password: 12345678 (default - change if needed)
   - Port: 3306 (default)

## Running the Application

1. Navigate to the project directory:
   ```bash
   cd online-auction-mvp
   ```

2. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

3. The application will open in your default browser at `http://localhost:8501`

4. If the browser doesn't open automatically, visit `http://localhost:8501` manually.

## Connecting MySQL Workbench

1. Open MySQL Workbench.

2. Click on the `+` sign to add a new connection in the "MySQL Connections" section.

3. Fill in the connection details:
   - Connection Name: `auction_db_local` (or any name you prefer)
   - Hostname: `localhost` (or `127.0.0.1`)
   - Port: `3306`
   - Username: `root` (or your MySQL username)
   - Password: Click on "Store in Keychain" and enter your MySQL password

4. Click "Test Connection" to verify the connection works.

5. Save the connection and click on it to connect to your MySQL server.

6. Once connected, you'll see your databases in the navigation panel. 
   Select the `auction_db` database from the schema list (or create it if it doesn't exist).

7. You can now view and manage the tables (users, items, bids) using the visual interface:
   - Right-click on a table name and select "Select Rows" to view data
   - Use the "SQL Editor" tab to run custom queries

## Troubleshooting

### Common Issues and Solutions

1. **MySQL Connection Error**:
   - Ensure MySQL Server is running
   - Check credentials in `db_config.py`
   - Verify MySQL port (default is 3306)

2. **Port Already in Use Error**:
   - The application runs on port 8501 by default
   - Check if another Streamlit app is running
   - Use `streamlit run app.py --server.port 8502` to use a different port

3. **Python Dependencies Error**:
   - Make sure you're in the correct virtual environment
   - Run `pip install -r requirements.txt` again

4. **MySQL Workbench Connection Issues**:
   - Check that the MySQL Server service is running
   - Verify username and password are correct
   - Make sure the port number is correct (usually 3306)

### Database Schema Overview
The application uses three main tables:
- `users`: Stores user information (user_id, name, email, hashed password, role)
- `items`: Stores auction items (item_id, name, description, base_price, seller_id)
- `bids`: Stores bid information (bid_id, item_id, buyer_id, bid_amount, bid_time)

Foreign key relationships ensure data integrity between these tables.