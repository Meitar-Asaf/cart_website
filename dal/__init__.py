from flask import render_template, url_for, flash
import sqlite3
import os

DB_FILE = "products.db"


def init_db():
    print("init db start")
    print("DB FILE:", os.path.abspath(DB_FILE))
    reset_products_table()
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""DROP TABLE IF EXISTS roles""")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS roles(
            role_id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL) """)
        cursor.execute("""
        INSERT INTO roles(role) VALUES('admin')""")
        cursor.execute("""
        INSERT INTO roles(role) VALUES('user')""")
        cursor.execute("""DROP TABLE IF EXISTS users""")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role_id INTEGER DEFAULT 2,
            FOREIGN KEY (role_id) REFERENCES roles(role_id)
        )
        """)
        cursor.execute("""DROP TABLE IF EXISTS songs""")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS songs (
            page TEXT PRIMARY KEY DEFAULT 'home',
            filename TEXT
        )
        """)
        cursor.execute("INSERT INTO songs(page) VALUES('cart')")
        cursor.execute("INSERT INTO songs DEFAULT VALUES")
        print("New table created.")
        conn.commit()


def reset_products_table():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""DROP TABLE IF EXISTS products""")
        conn.commit()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quantity INTEGER DEFAULT 1,
            title TEXT NOT NULL,
            completed BOOLEAN DEFAULT 0,
            filename TEXT,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES roles(user_id)
        )
        """)
        conn.commit()


def change_song(filename, page):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE songs SET filename = ? WHERE page = ?", (filename, page))
        conn.commit()


def select_all(user_id):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE user_id = ?", (user_id,))
        return cursor.fetchall()


def add_to_list(product=None, filename=None, user_id=None):
    print(product, user_id)
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        lower_products_list = [
            i[2].lower() for i in select_all(user_id)]

        if product.lower() not in lower_products_list:
            product = product[0].upper() + product[1:].lower()
            cursor.execute(
                "INSERT INTO products (title, filename, user_id) VALUES (?, ?, ?)", (product, filename, user_id))
            conn.commit()
        else:
            raise ValueError("Item already exists!")


def get_user_id_by_username(username):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT user_id FROM users WHERE username = ?", (username,))
        return cursor.fetchall()[0][0]


def list_is_empty(user_id):
    return len(select_all(user_id)) == 0


def delete_product(product_id, user_id):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM products WHERE id = ? AND user_id = ?", (product_id, user_id))
        conn.commit()


def delete_all(user_id):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE user_id = ?", (user_id,))
        conn.commit()


def search_bar(user_id):
    print(select_all(user_id))
    index = 0
    results = []
    for product in select_all(user_id):
        for p in product[2].lower():
            while index < len(product[2]) and product[2][index].isdigit():
                index += 1
        results.append(product[2][index:].strip())
    print(results)
    return results


def update_quantity(quantity=None, product=None, user_id=None):
    print(search_bar(user_id))
    print(product.lower())
    search_bar_list = []
    for i in search_bar(user_id):
        print(i.lower() == product.lower())
        search_bar_list.append(i. lower())
    print(search_bar_list)
    if product.lower() not in search_bar_list:
        raise ValueError("Product not in the list")
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        product = product[0].upper() + product[1:].lower()
        cursor.execute(
            "UPDATE products SET quantity = ? WHERE title = ? AND user_id", (quantity, product, user_id))
        conn.commit()


def select_song_by_page(page):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT filename FROM songs WHERE page = ?", (page,))
        return cursor.fetchall()


def select_filename_by_product_id(product_id):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT filename FROM products WHERE id = ?", (product_id,))
        return cursor.fetchall()


def update_picture_file(filename=None, id=None, user_id=None):
    id_list = [i[0] for i in select_all(user_id)]
    print(id_list)
    if int(id) not in id_list:
        raise ValueError("The product id is not in the list.")
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE products SET filename = ? WHERE id = ? AND user_id = ?", (filename, id, user_id))
        conn.commit()


def signup(username, password, role_id=None):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        if role_id:
            cursor.execute(
                "INSERT INTO users (username, password, role_id) VALUES(?, ?, ?)", (username, password, role_id))
            conn.commit()
        else:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES(?, ?)", (username, password))
            conn.commit()


def select_all_users():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        return cursor.execute("SELECT * FROM users").fetchall()


def login(username):
    for i in select_all_users():
        if username == i[1]:
            return i[1], i[2], i[0]
        if not username:
            raise ValueError("Username does not exist!")