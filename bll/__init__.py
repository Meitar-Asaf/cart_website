from dal import add_to_list, delete_product, list_is_empty, select_all, delete_all, search_bar, update_quantity, update_picture_file, signup, login, select_filename_by_product_id, change_song, select_song_by_page, reset_products_table, get_user_id_by_username
import uuid
from flask import current_app, send_from_directory
from pathlib import Path
from werkzeug.security import generate_password_hash, check_password_hash
import shutil

def add_to_cart_bll(product = None, file = None, user_id = None):
    print("this is the info :",product, user_id)
    if file:
        filename = str(uuid.uuid4())
        image_path = Path(current_app.static_folder) / "images" / filename
        file.save(image_path)
    else:
        filename = None
    add_to_list(product, filename, user_id)


def delete_product_by_id_bll(product_id, user_id = None):
    filename = select_filename_by_product_id(product_id)[0][0]
    if filename:
        image_path = Path(current_app.static_folder) / "images" / filename
        image_path.unlink()
    delete_product(product_id, user_id)


def is_list_empty_bll(user_id):
    return list_is_empty(user_id)


def select_all_bll(user_id):
    return select_all(user_id)

def delete_all_bll(user_id):
    folder_path = Path(current_app.static_folder) / "images"
    if folder_path.exists() and folder_path.is_dir():
        for item in folder_path.iterdir():
            if item.is_file() or item.is_symlink():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
    delete_all(user_id)

def search_bar_bll(product, user_id):
    results = [p for p in search_bar(user_id) if product.lower() in p.lower()]
    print(results)
    return results

def update_quantity_bll(quantity, product_name, user_id):
    
    update_quantity(quantity, product_name, user_id)

def update_picture_file_bll(filename, id, user_id):
    filename_str = str(uuid.uuid4())
    image_path = Path(current_app.static_folder) / "images" / filename_str
    filename.save(image_path)
    update_picture_file(filename_str, id, user_id)

def signup_bll(username, password, role_id = None):
    new_password = generate_password_hash(password)
    if role_id:
        signup(username, new_password, role_id)
    else:
        signup(username, new_password)

def login_bll(username, password):
    login_info = login(username)
    if login_info:
        role_id,hashed_password, user_id = login_info
        if check_password_hash(hashed_password, password):
            return role_id, user_id
    
    raise ValueError("Wrong username or password")

def change_song_bll(page, file):
    filename = str(uuid.uuid4())
    image_path = Path(current_app.static_folder) / "music" / filename
    file.save(image_path)
    change_song(filename, page)

def play_song_bll(page):
    directory = Path(current_app.static_folder) / "music"
    filename = select_song_by_page(page)[0][0]
    return send_from_directory(directory, filename)

def get_user_id_by_username_bll(username):
    return get_user_id_by_username(username)

def reset_products_table_bll():
    reset_products_table()
