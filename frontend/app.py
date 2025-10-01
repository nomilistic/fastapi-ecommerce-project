# streamlit_app.py
import streamlit as st
import api_client
import os
# from dotenv import load_dotenv
# import os
# import tempfile
# from PIL import Image

# load_dotenv()
# API_URL = os.getenv("API_URL", "http://localhost:8000")

# st.set_page_config(page_title="Ecom - Frontend", layout="wide")
if "token" not in st.session_state:
    st.session_state["role"] = None


st.title("The WATCH House")

if st.session_state.get("role") == "admin":
    menu = ["Products", "Add Product", "Update Product", "Delete Product", "Logout"]
elif st.session_state.get("role") == "customer":
    menu = ["Products", "My Cart", "Checkout","My Orders", "Logout"]
else:
    menu = ["Products","Signup", "Login"]

choice = st.sidebar.selectbox("Menu", menu)

if choice == "Products":
    st.subheader("Products")
    items = api_client.get_products()
    if isinstance(items, list):
        for item in items:
            st.markdown(f"<h3 style='font-size:22px;'>{item['name']} - 💲{item['price']}</h3>", unsafe_allow_html=True)

            
            if st.session_state.get("role") == "customer":
                quantity = st.number_input("Quantity",key=f"qty_{item['id']}",min_value=1, step=1,width=121)
                if st.button("Add to Cart",key=f"btn_{item['id']}"):    
                    payload = {"name": item["name"],"quantity": quantity}
                    r = api_client.add_to_cart(payload,st.session_state["token"])
                    if r.status_code == 200:
                        st.success("✅ Product added to cart!")
                    else:
                        st.error(f"❌ {r.text}")
                                 
            if st.session_state.get("role") == "admin":
                st.markdown(f"*{item['id']}*")
    else:
        st.warning("⚠️ Could not fetch items.")

elif choice == "Signup":
    st.subheader("Create Account")
    username = st.text_input("Userame")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        r = api_client.register(username, email, password)
        if r.status_code == 200 or r.status_code == 201:
            st.success("✅ Account created successfully! Please log in.")
        else:
            st.error(f"❌ {r.json().get('detail', 'Registration failed')}")
elif choice == "Login":
    st.subheader("Login to your account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        r = api_client.login(username, password)
        if r.status_code == 200:
            token_data = r.json()
            st.session_state["token"] = token_data["access_token"]
            st.session_state["role"] = token_data["role"]
            st.success("✅ Logged in successfully!")
        else:
            st.error(f"❌ {r.json().get('detail', 'Invalid credentials')}")
elif choice == "My Cart":
    st.subheader("Your Cart")
    cart_items = api_client.view_cart(st.session_state["token"])
    total_bill=0
    if isinstance(cart_items, list):
        for item in cart_items:

            st.markdown(f"<h3 style='font-size:22px;'>{item['id']}. {item["name"]}", unsafe_allow_html=True)
            st.markdown(f"<h4 style='font-size:18px;'>Quantity: {item['quantity']}</h4>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='font-size:18px;'>Price: 💲{item['price']}</h4>", unsafe_allow_html=True)
            total_bill += item['price']
            

    else:
        st.warning("⚠️ Could not fetch items.")

    st.markdown(f"<h3 style='font-size:22px;'>Total Bill: {total_bill}", unsafe_allow_html=True)     
elif choice == "Logout":
    st.session_state["token"] = None
    st.session_state["role"] = None
    st.session_state["username"] = None
    st.success("Logged out successfully!")
    st.rerun() 
elif choice == "Add Product":
    st.subheader("Add new product")

    name = st.text_input("Product Name")
    price = st.text_input("Price")
    quantity_available = st.text_input("Quantity Available")
    if st.button("Add Product"):
        payload = {"name": name, "price": price, "quantity_available": quantity_available}
        r = api_client.add_product(payload, st.session_state["token"])
        if r.status_code == 200:
            st.success("✅ Product added successfully!")
        else:
            st.error(f"❌ {r.text}")
elif choice == "Update Product":
    st.subheader("Update Product")

    id = st.number_input("Product ID",min_value=1, step=1)
    name = st.text_input("Product Name")
    price = st.text_input("Price")
    quantity_available = st.text_input("Quantity Available")
    if st.button("Update Product"):
        payload = {"id":id,"name": name, "price": price, "quantity_available": quantity_available}
        r = api_client.update_product(payload, st.session_state["token"])
        if r.status_code == 200:
            st.success("✅ Product updated successfully!")
        else:
            st.error(f"❌ {r.text}")
elif choice == "Delete Product":
    st.subheader("Delete Product")

    id = st.number_input("Product ID",min_value=1, step=1)
    if st.button("Delete Product"):
        r = api_client.delete_product(id,st.session_state["token"])
        if r.status_code == 200:
            st.success("Product was successfully deleted")
        else:
            st.error(f"❌ {r.text}")
elif choice == "Checkout":
    st.subheader("Checkout")
    cart_items = api_client.view_cart(st.session_state["token"])
    total_bill=0
    if isinstance(cart_items, list):
        for item in cart_items:

            st.markdown(f"<h3 style='font-size:22px;'>{item['id']}. {item["name"]}", unsafe_allow_html=True)
            st.markdown(f"<h4 style='font-size:18px;'>Quantity: {item['quantity']}</h4>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='font-size:18px;'>Price: 💲{item['price']}</h4>", unsafe_allow_html=True)
            total_bill += item['price']
            

    else:
        st.warning("⚠️ Could not fetch items.")

    st.markdown(f"<h3 style='font-size:22px;'>Total Bill: {total_bill}", unsafe_allow_html=True)

    st.write("Proceed with payment / confirm order here...")
    if st.button("Complete Checkout"):
        r = api_client.place_order(st.session_state["token"])
        if r.status_code == 200:
            st.success("Thank You For purchasing with us!")
        else:
            st.error("It's not you, it's us. Unable to process your order.")
elif choice == "My Orders":
    st.subheader("Your Order History")
    orders = api_client.view_orders(st.session_state["token"])
    if isinstance(orders, list):
        for order in orders:
            st.markdown(f"<h3 style='font-size:22px;'>Total Bill: 💲{order['total_price']}</h3>", unsafe_allow_html=True)
            # st.markdown(f"<h3 style='font-size:22px;'>Ordered At: {order['created_at']}</h3>", unsafe_allow_html=True)

            st.markdown("<h3 style='font-size:22px;'>Order Breakdown:</h3>", unsafe_allow_html=True)  
            st.json(order['order_details'])         
    else:
        st.warning("⚠️ Could not fetch items.")


