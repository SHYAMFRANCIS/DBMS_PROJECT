# Online Auction Management System

An online auction platform built with Python, MySQL, and Streamlit that allows sellers to list items and buyers to bid on them.

## 🚀 Features

- User authentication (register/login)
- Role-based dashboards (buyer/seller)
- Item listing and browsing
- Real-time bidding system
- Bid tracking and history
- CSV export for reports
- Secure password hashing

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python
- **Database:** MySQL
- **Libraries:** mysql-connector-python, pandas, bcrypt

## 📋 Prerequisites

- Python 3.7+
- MySQL Server
- pip (Python package manager)

## 📦 Installation

1. **Clone or download** this repository to your local machine.

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up MySQL database:**
   - Make sure your MySQL server is running
   - Update database credentials in `db_config.py` if needed (default assumes root user with no password)
   - Execute the schema file to create the database and tables:
     ```sql
     mysql -u root -p < schema.sql
     ```

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## 🔐 Database Configuration

The application expects a MySQL database named `auction_db`. By default, it connects using:
- Host: localhost
- Database: auction_db
- Username: root
- Password: (empty)
- Port: 3306

To change these settings, update the `DB_CONFIG` dictionary in `db_config.py`.

## 🎮 How to Use

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

## 🏗️ Project Structure

```
online_auction_mvp/
│
├── app.py                 # Main Streamlit application
├── db_config.py           # Database connection and helper functions
├── schema.sql             # MySQL database schema
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
└── assets/                # Optional images or logos
```

## 📁 Database Schema

The system uses three main tables:

1. **users** - Stores user information (ID, name, email, password, role)
2. **items** - Stores auction items (ID, name, description, base price, seller ID)
3. **bids** - Stores bid information (ID, item ID, buyer ID, bid amount, timestamp)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

If you encounter any issues or have questions, please file an issue in the repository.