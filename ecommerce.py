import tkinter as tk
from PIL import ImageTk, Image
import mysql.connector
from datetime import datetime

class ECommerceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("E-Commerce")
        self.root.geometry("800x600")

        self.cart = []  # Initialize an empty cart

        self.create_main_page()

    def connect_to_database(self):
        # Connect to MySQL database
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="ajay15",
            database="projectxx"
        )
        self.cursor = self.connection.cursor()

    def fetch_products(self):
        # Fetch products from the database
        self.connect_to_database()
        self.cursor.execute("SELECT * FROM products")
        self.products = self.cursor.fetchall()
        self.connection.close()

    def add_to_cart(self, product):
        # Add the product to the cart
        self.cart.append(product)

        # Insert the product into the cart table in the database
        self.connect_to_database()
        query = "INSERT INTO cart (product_name, price, added_at) VALUES (%s, %s, %s)"
        added_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data = (product[0], product[1], added_at)
        self.cursor.execute(query, data)
        self.connection.commit()
        self.connection.close()

        print("Product added to cart:", product[0])

    def create_main_page(self):
        self.fetch_products()

        # Main Frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(pady=20)

        # Title
        title_label = tk.Label(main_frame, text="Welcome to Our E-Commerce Site", font=("Helvetica", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Product Listings
        for idx, product in enumerate(self.products):
            product_frame = tk.Frame(main_frame, bd=2, relief="groove")
            product_frame.grid(row=idx+1, column=0, padx=10, pady=5, sticky="w")

            # Product Image
            img = Image.open(product[2])  # Assuming the image path is stored in the 3rd column (index 2)
            img = img.resize((100, 100))
            img = ImageTk.PhotoImage(img)
            image_label = tk.Label(product_frame, image=img)
            image_label.image = img
            image_label.grid(row=0, column=0, padx=10, pady=5)

            # Product Details
            name_label = tk.Label(product_frame, text=product[0], font=("Helvetica", 14, "bold"))
            name_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")
            price_label = tk.Label(product_frame, text=f"Price: ${product[1]}", font=("Helvetica", 12))
            price_label.grid(row=1, column=1, padx=10, pady=5, sticky="w")
            description_label = tk.Label(product_frame, text=product[3])
            description_label.grid(row=2, column=1, padx=10, pady=5, sticky="w")

            # Add to Cart Button
            add_to_cart_button = tk.Button(product_frame, text="Add to Cart", command=lambda prod=product: self.add_to_cart(prod), bg="#4CAF50", fg="white")
            add_to_cart_button.grid(row=0, column=2, padx=10, pady=5)

        # View Cart Button
        view_cart_button = tk.Button(main_frame, text="View Cart", command=self.view_cart, bg="#4CAF50", fg="white")
        view_cart_button.grid(row=idx+2, column=0, columnspan=3, pady=10)

    def view_cart(self):
        # Fetch cart contents from the database
        self.connect_to_database()
        self.cursor.execute("SELECT * FROM cart")
        cart_contents = self.cursor.fetchall()
        self.connection.close()

        # Create a new window to display cart contents
        cart_window = tk.Toplevel(self.root)
        cart_window.title("Your Cart")

        # Cart Frame
        cart_frame = tk.Frame(cart_window)
        cart_frame.pack(pady=20)

        # Title
        title_label = tk.Label(cart_frame, text="Your Cart", font=("Helvetica", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Scrollbar for the cart
        scrollbar = tk.Scrollbar(cart_frame, orient="vertical")
        scrollbar.grid(row=1, column=3, rowspan=10, sticky="ns")

        # Cart Listings
        cart_canvas = tk.Canvas(cart_frame, yscrollcommand=scrollbar.set)
        cart_canvas.grid(row=1, column=0, columnspan=3)
        scrollbar.config(command=cart_canvas.yview)

        inner_frame = tk.Frame(cart_canvas)
        cart_canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        for idx, item in enumerate(cart_contents):
            item_frame = tk.Frame(inner_frame, bd=2, relief="groove")
            item_frame.grid(row=idx, column=0, padx=10, pady=5, sticky="w")

            # Product Name
            name_label = tk.Label(item_frame, text=item[1], font=("Helvetica", 14, "bold"))
            name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

            # Product Price
            price_label = tk.Label(item_frame, text=f"Price: ${item[2]}", font=("Helvetica", 12))
            price_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Total Price
        total_price = sum(item[2] for item in cart_contents)
        total_label = tk.Label(cart_frame, text=f"Total: ${total_price}", font=("Helvetica", 14))
        total_label.grid(row=len(cart_contents)+2, column=0, columnspan=3, pady=10)

        # Update inner frame window size
        inner_frame.update_idletasks()
        cart_canvas.config(scrollregion=cart_canvas.bbox("all"))

        # Centering the window on the screen
        cart_window.update_idletasks()
        width = cart_window.winfo_width()
        height = cart_window.winfo_height()
        x = (cart_window.winfo_screenwidth() // 2) - (width // 2)
        y = (cart_window.winfo_screenheight() // 2) - (height // 2)
        cart_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
