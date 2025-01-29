import streamlit as st
import mysql.connector
from PIL import Image
import io

# Database connection
def get_db_connection():
    connection = mysql.connector.connect(
        host="82.180.143.66",
        user="u263681140_students1",
        password="testStudents@123",
        database="u263681140_students1"
    )
    return connection

def insert_product(name, amount, img_binary, group):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "INSERT INTO products (name, amount, img, `group`) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (name, amount, img_binary, group))
    connection.commit()
    cursor.close()
    connection.close()
# Streamlit app
st.title("Product Registration")

# Input fields
product_name = st.text_input("Product Name")
product_amount = st.number_input("Amount", min_value=0.0, format="%.2f")
product_image = st.file_uploader("Upload Product Image", type=["jpg", "jpeg", "png"])
product_group = st.selectbox("Select Group", ["VegStarter","VegStarter", "VegMainCource", "NonVegMainCource", "Roti", "Rice", "Beverage"])

if st.button("Register Product"):
    if not product_name:
        st.error("Please enter the product name.")
    elif product_amount <= 0:
        st.error("Please enter a valid amount.")
    elif not product_image:
        st.error("Please upload a product image.")
    elif not product_group:
        st.error("Please select a group.")
    else:
        # Convert uploaded image to binary
        img_binary = product_image.read()
        try:
            # Insert into database
            insert_product(product_name, product_amount, img_binary, product_group)
            st.success("Product registered successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Optional: Display products
if st.checkbox("Show Registered Products"):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT name, amount, group, img FROM products")
    products = cursor.fetchall()
    cursor.close()
    connection.close()

    for product in products:
        st.write(f"**Name:** {product[0]}")
        st.write(f"**Amount:** {product[1]}")
        st.write(f"**Group:** {product[2]}")
        img = Image.open(io.BytesIO(product[3]))
        st.image(img, caption=product[0], use_column_width=True)
