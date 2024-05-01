import mysql.connector

# Connect to MySQL database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ajay15",
    database="projectxx"
)
cursor = connection.cursor()

# Sample product data
products_data = [
    ("Pen", 10.99, "515sXTO5QkL._AC_UF1000,1000_QL80_.jpg", "Description of Product 1"),
    ("Car", 11119.99, "Hyundai-Venue-2022.webp", "Description of Product 2"),
    ("Chair", 29.99, "sofa_WLCHRATCFVBL_1.webp", "Description of Product 3"),
    # Add more products as needed
]

# Insert product data into the database
for product in products_data:
    cursor.execute("INSERT INTO products (name, price, image_path, description) VALUES (%s, %s, %s, %s)", product)

# Commit changes and close connection
connection.commit()
connection.close()

print("Sample product data inserted successfully!")
