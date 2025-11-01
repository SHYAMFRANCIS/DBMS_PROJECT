import streamlit as st
import pandas as pd
from db_config import (
    register_user, login_user, add_item, view_items, get_item_by_id, 
    place_bid, get_bids_for_item, get_bids_by_user, get_items_by_seller,
    get_item_bids_by_seller, highest_bids, get_user_by_id
)

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None
    st.session_state.page = 'login'

# Title of the app
st.set_page_config(page_title="Online Auction System", page_icon="🔨", layout="wide")
st.title("🔨 Online Auction Management System")

def login_page():
    st.header("Login")
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        login_submitted = st.form_submit_button("Login")
        
        if login_submitted:
            user, message = login_user(email, password)
            if user:
                st.session_state.user = user
                st.success(message)
                st.rerun()
            else:
                st.error(message)

def register_page():
    st.header("Register")
    with st.form("register_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", options=["buyer", "seller"])
        register_submitted = st.form_submit_button("Register")
        
        if register_submitted:
            success, message = register_user(name, email, password, role)
            if success:
                st.success(message)
            else:
                st.error(message)

def logout():
    st.session_state.user = None
    st.session_state.page = 'login'
    st.success("Logged out successfully")
    st.rerun()

def seller_dashboard():
    st.header(f"Seller Dashboard - Welcome, {st.session_state.user['name']}")
    
    # Navigation
    seller_pages = ["Home", "Add Item", "View My Items", "My Item Bids"]
    seller_page = st.sidebar.selectbox("Seller Menu", seller_pages)
    
    if seller_page == "Home":
        st.subheader("Seller Overview")
        items, msg = get_items_by_seller(st.session_state.user['user_id'])
        st.metric("Total Items Listed", len(items))
        
        bids, msg = get_item_bids_by_seller(st.session_state.user['user_id'])
        st.metric("Total Bids Received", len(bids))
        
        if bids:
            df = pd.DataFrame(bids)
            st.subheader("Recent Bids")
            st.dataframe(df[['item_name', 'buyer_name', 'bid_amount', 'bid_time']].head(10))
    
    elif seller_page == "Add Item":
        st.subheader("Add New Item for Auction")
        with st.form("add_item_form"):
            item_name = st.text_input("Item Name")
            description = st.text_area("Description")
            base_price = st.number_input("Base Price", min_value=0.0, format="%.2f")
            submit_item = st.form_submit_button("Add Item")
            
            if submit_item:
                if item_name and base_price > 0:
                    success, message = add_item(item_name, description, base_price, st.session_state.user['user_id'])
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
                else:
                    st.error("Please fill in all required fields with valid data.")
    
    elif seller_page == "View My Items":
        st.subheader("Items You Have Listed")
        items, msg = get_items_by_seller(st.session_state.user['user_id'])
        
        if items:
            df = pd.DataFrame(items)
            df = df.rename(columns={'item_id': 'ID', 'item_name': 'Item Name', 'description': 'Description', 'base_price': 'Base Price'})
            st.dataframe(df)
        else:
            st.info("You haven't listed any items yet.")
    
    elif seller_page == "My Item Bids":
        st.subheader("Bids on Your Items")
        bids, msg = get_item_bids_by_seller(st.session_state.user['user_id'])
        
        if bids:
            df = pd.DataFrame(bids)
            df = df.rename(columns={
                'item_name': 'Item', 
                'buyer_name': 'Buyer', 
                'bid_amount': 'Bid Amount', 
                'bid_time': 'Time'
            })
            st.dataframe(df)
            
            # Option to download bids as CSV
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download bids as CSV",
                data=csv,
                file_name="my_item_bids.csv",
                mime="text/csv"
            )
        else:
            st.info("No bids have been placed on your items yet.")

def buyer_dashboard():
    st.header(f"Buyer Dashboard - Welcome, {st.session_state.user['name']}")
    
    # Navigation
    buyer_pages = ["Browse Items", "Place Bid", "My Bids", "Top Bids"]
    buyer_page = st.sidebar.selectbox("Buyer Menu", buyer_pages)
    
    if buyer_page == "Browse Items":
        st.subheader("Items Available for Auction")
        items, msg = view_items()
        
        if items:
            df = pd.DataFrame(items)
            df = df.rename(columns={
                'item_id': 'ID', 
                'item_name': 'Item Name', 
                'description': 'Description', 
                'base_price': 'Base Price',
                'seller_name': 'Seller'
            })
            st.dataframe(df)
        else:
            st.info("No items available for auction at the moment.")
    
    elif buyer_page == "Place Bid":
        st.subheader("Place a Bid")
        items, msg = view_items()
        
        if items:
            # Get item names for selection
            item_options = {item['item_name']: item['item_id'] for item in items}
            selected_item_name = st.selectbox("Select Item", options=list(item_options.keys()))
            selected_item_id = item_options[selected_item_name]
            
            # Get item details
            item, msg = get_item_by_id(selected_item_id)
            
            if item:
                st.write(f"**Item:** {item['item_name']}")
                st.write(f"**Description:** {item['description']}")
                st.write(f"**Base Price:** ${item['base_price']:.2f}")
                
                # Get current highest bid
                bids, msg = get_bids_for_item(selected_item_id)
                if bids:
                    highest_bid = max(bids, key=lambda x: x['bid_amount'])
                    st.write(f"**Current Highest Bid:** ${highest_bid['bid_amount']:.2f} by {highest_bid['buyer_name']}")
                    min_bid = highest_bid['bid_amount'] + 0.01
                else:
                    min_bid = item['base_price']
                    st.write(f"**Starting Bid:** ${min_bid:.2f}")
                
                with st.form("bid_form"):
                    bid_amount = st.number_input(
                        "Your Bid Amount", 
                        min_value=min_bid, 
                        format="%.2f"
                    )
                    submit_bid = st.form_submit_button("Place Bid")
                    
                    if submit_bid:
                        success, message = place_bid(selected_item_id, st.session_state.user['user_id'], bid_amount)
                        if success:
                            st.success(message)
                        else:
                            st.error(message)
        else:
            st.info("No items available for bidding at the moment.")
    
    elif buyer_page == "My Bids":
        st.subheader("Your Bidding History")
        bids, msg = get_bids_by_user(st.session_state.user['user_id'])
        
        if bids:
            df = pd.DataFrame(bids)
            df = df.rename(columns={
                'item_name': 'Item', 
                'bid_amount': 'Bid Amount', 
                'bid_time': 'Time'
            })
            st.dataframe(df)
            
            # Option to download bids as CSV
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download my bids as CSV",
                data=csv,
                file_name="my_bids.csv",
                mime="text/csv"
            )
        else:
            st.info("You haven't placed any bids yet.")
    
    elif buyer_page == "Top Bids":
        st.subheader("Highest Bids Across All Items")
        top_bids, msg = highest_bids()
        
        if top_bids:
            df = pd.DataFrame(top_bids)
            df = df.rename(columns={
                'item_name': 'Item', 
                'buyer_name': 'Winner', 
                'bid_amount': 'Winning Bid', 
                'bid_time': 'Time'
            })
            st.dataframe(df)
            
            # Option to download highest bids as CSV
            if not df.empty:
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download top bids as CSV",
                    data=csv,
                    file_name="top_bids.csv",
                    mime="text/csv"
                )
        else:
            st.info("No bids have been placed yet.")

def main():
    # Show login/register options if not logged in
    if st.session_state.user is None:
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Go to", ["Login", "Register"])
        
        if page == "Login":
            login_page()
        else:
            register_page()
    else:
        # Show logout button if logged in
        col1, col2 = st.columns([4, 1])
        with col2:
            if st.button("Logout"):
                logout()
        
        # Show appropriate dashboard based on user role
        if st.session_state.user['role'] == 'seller':
            seller_dashboard()
        else:  # buyer
            buyer_dashboard()

if __name__ == "__main__":
    main()