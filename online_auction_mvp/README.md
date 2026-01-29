# Online Auction Management System

A Minimum Viable Product (MVP) for a web-based online auction platform. Users can register, list items for sale, and bid on items listed by other users. The application is built using Python with the Streamlit framework for the user interface and MySQL for the database backend.

For a more detailed setup guide, including troubleshooting and connecting with MySQL Workbench, please see [setup.md](setup.md).

##  Features

*   **User Management:** Secure user registration and login system with distinct roles.
*   **Item Listings:** Sellers can list items for auction with a name, description, and a starting base price.
*   **Bidding System:** Buyers can browse available items and place bids.
*   **Data Integrity:** Foreign key constraints in the database ensure relationships between users, items, and bids are maintained.

##  Technology Stack

*   **Framework:** [Streamlit](https://streamlit.io/)
*   **Language:** Python 3
*   **Database:** MySQL

##  Getting Started

Follow these steps to get the application running on your local machine.

### Prerequisites

Ensure you have the following installed:
*   Docker and Docker Compose (for containerized installation - recommended)
*   OR Python 3.7+ and MySQL Server 8.0+ (for local installation)
*   Git (optional)

### 1. Clone the Repository

```bash
git clone https://github.com/SHYAMFRANCIS/DBMS_PROJECT.git
cd online-auction-mvp
```

### 2. Running with Docker (Recommended)

The easiest way to run the application is using Docker Compose, which will set up both the application and MySQL database in containers:

```bash
# Make sure Docker and docker-compose are installed
# From the project directory, run:
docker-compose up
```

The application will be available in your web browser at `http://localhost:8501`.

To stop the services, press `Ctrl+C` or run:
```bash
docker-compose down
```

### 3. Local Installation (Alternative Method)

If you prefer to run the application locally without Docker:

#### Set Up a Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies.

```bash
# Create the environment
python -m venv venv

# Activate the environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

#### Install Dependencies

Install the required Python packages.

```bash
pip install -r requirements.txt
```

#### Database Setup

1.  Make sure your MySQL server is running.
2.  Execute the `schema.sql` script to create the database and tables. You will be prompted for your MySQL root password.

    ```bash
    mysql -u root -p < schema.sql
    ```

3.  **(Optional)** If your MySQL credentials are not the default (`root`/`12345678`), update them in the `db_config.py` file.

#### Run the Application

Start the Streamlit development server.

```bash
streamlit run app.py
```

The application will be available in your web browser at `http://localhost:8501`.

##  Database Configuration

The application expects a MySQL database named `auction_db`. By default, it connects using:
- Host: localhost
- Database: auction_db
- Username: root
- Password: (empty)
- Port: 3306

To change these settings, update the `DB_CONFIG` dictionary in `db_config.py`.

##  How to Use

1. **Registration:** New users can register with their name, email, password, and role (buyer or seller).

2. **Login:** Registered users can log in with their email and password.

3. **Seller Functions:**
   - Add new items for auction
   - View items they've listed
   - See bids placed on their items

4. **Buyer Functions:**
   - Browse available auction items
   - Place bids on items
   - View their bidding history
   - See top bids across all items

##  Project Structure

```
online_auction_mvp/
│
├── app.py                 # Main Streamlit application
├── db_config.py           # Database connection and helper functions
├── schema.sql             # MySQL database schema
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose configuration
└── setup.md               # Detailed setup guide
```

##  Database Schema

The application relies on a simple yet effective relational database schema:

*   `users`: Stores user information, including credentials and roles.
    -   `user_id`, `name`, `email`, `password_hash`, `role`
*   `items`: Contains details about the items up for auction.
    -   `item_id`, `name`, `description`, `base_price`, `seller_id` (FK to `users`)
*   `bids`: Records all bids placed on items.
    -   `bid_id`, `item_id` (FK to `items`), `buyer_id` (FK to `users`), `bid_amount`, `bid_time`

##  Contributing

This is an MVP, and there is plenty of room for improvement. Contributions are welcome! Feel free to fork the repository, make changes, and submit a pull request.

Potential areas for future development include:
*   Real-time bidding updates with websockets.
*   Auction end times and automatic winner selection.
*   User dashboards to view listed items and bidding history.
*   Image uploads for auction items.

## 📝 License

This project is open source and available under the [GNU License](LICENSE).
