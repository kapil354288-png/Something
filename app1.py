import streamlit as st
import pandas as pd
import numpy as np
from pymongo import MongoClient

# ------------------------------------
# CONNECT TO MONGODB USING SECRETS
# ------------------------------------
# In .streamlit/secrets.toml, add:
# [mongo]
# uri = "mongodb+srv://<username>:<password>@cluster.mongodb.net/"
# db = "streamlit_app"

client = MongoClient(st.secrets["mongo"]["uri"])
db = client[st.secrets["mongo"]["db"]]
users_collection = db["users"]

# ------------------------------------
# HELPER FUNCTIONS
# ------------------------------------
def create_user(name, username, password, role="user"):
    users_collection.insert_one({
        "name": name,
        "username": username,
        "password": password,
        "role": role
    })

def get_user(username):
    return users_collection.find_one({"username": username})

def validate_user(username, password):
    user = get_user(username)
    if user and user["password"] == password:
        return user
    return None

def load_users_as_dataframe():
    """Load all users into a pandas DataFrame."""
    data = list(users_collection.find({}, {"_id": 0}))
    if not data:
        return pd.DataFrame(columns=["name", "username", "role"])
    return pd.DataFrame(data)

# ------------------------------------
# STREAMLIT APP UI
# ------------------------------------
st.title("🔐 Streamlit + MongoDB + Pandas + NumPy App")

menu = ["Login", "Admin Panel"]
choice = st.sidebar.selectbox("Select Page", menu)

# ------------------------------------
# LOGIN PAGE
# ------------------------------------
if choice == "Login":
    st.subheader("User Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = validate_user(username, password)
        if user:
            st.success(f"Welcome, {user['name']}!")
            if user["role"] == "admin":
                st.info("You are logged in as an **Admin**.")
            else:
                st.info("You are logged in as a **User**.")

                # NumPy + Pandas Demo
                st.write("### 📊 Generate Random Data with NumPy")
                size = st.slider("Select number of random values:", 5, 100, 10)
                data = np.random.randint(1, 100, size)
                df = pd.DataFrame(data, columns=["Random Numbers"])
                st.dataframe(df)

                st.write("### 📈 Summary Statistics using Pandas")
                st.write(df.describe())

        else:
            st.error("Invalid username or password!")

# ------------------------------------
# ADMIN PANEL
# ------------------------------------
elif choice == "Admin Panel":
    st.subheader("Admin - Create or View Users")

    admin_user = st.text_input("Admin Username")
    admin_pass = st.text_input("Admin Password", type="password")

    if st.button("Validate Admin"):
        admin = validate_user(admin_user, admin_pass)
        if admin and admin["role"] == "admin":
            st.success("✅ Admin authenticated successfully!")

            # Create new user section
            st.write("### 👤 Create New User Account")
            name = st.text_input("Name")
            new_username = st.text_input("New Username")
            new_password = st.text_input("New Password", type="password")
            role = st.selectbox("Role", ["user", "admin"])

            if st.button("Create User"):
                if get_user(new_username):
                    st.warning("⚠️ Username already exists!")
                else:
                    create_user(name, new_username, new_password, role)
                    st.success(f"✅ User '{new_username}' created successfully!")

            # Display all users
            st.write("### 🧾 All Registered Users")
            df_users = load_users_as_dataframe()
            st.dataframe(df_users)
        else:
            st.error("Invalid admin credentials!")
