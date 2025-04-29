from flask import Flask, render_template, request, redirect, url_for, flash, abort, Blueprint, jsonify, send_from_directory, current_app, session
from pathlib import Path
from bll import add_to_cart_bll, delete_product_by_id_bll, is_list_empty_bll, select_all_bll, delete_all_bll, update_quantity_bll, play_song_bll
from werkzeug.utils import secure_filename
cart_bp = Blueprint("cart_bp", __name__, url_prefix= "/cart")
@cart_bp.route("/", methods = ["GET","PUT"])
def cart():
    if is_list_empty_bll(session['user_id']):
        return render_template("cart.html", delete_message="The list is empty")
    print(session['user_id'])
    products = select_all_bll(session['user_id'])
    if request.method == "GET":
        return render_template("cart.html", products=products),200
    
    if request.method == "PUT":
        return jsonify(products), 200

@cart_bp.route("/delete_product/<int:id>", methods=["POST"])
def delete(id):
    delete_product_by_id_bll(id, session['user_id'])
    return redirect(url_for("cart_bp.cart"))

@cart_bp.route("/delete_all", methods=["POST"])
def delete_all():
    delete_all_bll(session['user_id'])
    return redirect(url_for("cart_bp.cart"))


@cart_bp.route("/update_product_quantity", methods = ["POST"])
def update_quantity():
    quantity = request.form.get("quantity")
    product = request.form.get("products_list_dropdown")
    if quantity and product:
        update_quantity_bll(quantity, product, session['user_id'])
    return redirect(url_for('submit'))

@cart_bp.route("/images/<string:filename>")
def get_image(filename):
    print('filename', filename)
    directory = Path(current_app.static_folder) / "images"
    return send_from_directory(directory, filename)

@cart_bp.route("/song")
def cart_play_song():
    song = play_song_bll("cart")
    if not song:
        return redirect(url_for("cart_bp.cart"))
    return song

