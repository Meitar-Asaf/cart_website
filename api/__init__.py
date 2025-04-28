from api.cart_view import cart_bp
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from bll import add_to_cart_bll, select_all_bll, search_bar_bll,update_quantity_bll, update_picture_file_bll, signup_bll, login_bll, change_song_bll, play_song_bll, reset_products_table_bll, get_user_id_by_username_bll
from werkzeug.utils import secure_filename
from flask import session
from pathlib import Path
import atexit
import shutil

app = Flask(__name__, static_folder="../static", template_folder="../static/templates")
app.secret_key = 'my_very_secret_key'
app.register_blueprint(cart_bp)

def clear_images_folder():
    folder = Path("static/images")  # תוודאי שזה הנתיב הנכון
    if folder.exists() and folder.is_dir():
        for item in folder.iterdir():
            if item.is_file() or item.is_symlink():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
atexit.register(clear_images_folder)

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password")
        username = request.form.get("username")
        if password and username:
            login_result = login_bll(username, password)
            print(login_result)
            if login_result:
                session['username'] = username
                session['user_id'] = login_result[1]
                session['role_id'] = login_result[0]
                print(session['role_id'])
                return redirect(url_for('submit', products = select_all_bll(session['user_id'])))
            flash("Wrong username or password")
        if not password:
            flash("You didn't enter a password")
        if not username:
            flash("You didn't enter a username")
    return render_template("login.html")
        
@app.route("/signup", methods = ["GET", "POST"])
def signup():
    try:
        if request.method == "POST":
            password = request.form.get("password")
            username = request.form.get("username")
            role = request.form.get("role")
            if password and username:
                if role:
                    role_lower = role.lower()
                    if role_lower == "admin" or role_lower == "user":
                        if role_lower == "admin":
                            session['role_id'] = 1
                        else:
                            session['role_id'] = 2
                        signup_bll(username, password, session['role_id'])
                    else:
                        flash("Invalid role")
                        return render_template("signup.html")
                else:
                    signup_bll(username, password)
                    session['role_id'] = 2
                print(session['role_id'])
                session['username'] = username
                session['user_id'] = get_user_id_by_username_bll(session['username'])
                flash("You've registered successfully!")

                return redirect(url_for('submit'))
            if not password:
                    flash("You didn't enter a password")
            if not username:
                    flash("You didn't enter a username")
    except Exception as e:
        flash(str(e))
    return render_template("signup.html")

@app.route("/", methods=["POST", "GET"])
def submit():
    if not session.get("user_id"):
        abort(404)
    if request.method == "POST":
        product_name = request.form.get("product")
        print(product_name)
        print(session['user_id'])
        file =request.files.get("1img")
        add_to_cart_bll(product_name, file, session['user_id'])
        return redirect(url_for("cart_bp.cart"))
    products = select_all_bll(session.get('user_id'))
    if products:
        return render_template("home.html", cart_page=url_for("cart_bp.cart"), products = products)
    return render_template("home.html", cart_page=url_for("cart_bp.cart"))
    
    


# @app.route("/delete_all")
# def delete_all():




@app.route("/products/search", methods = ["GET", "POST"])
def search():
    search_text = str(request.args['search'])
    print(search_text)
    search_results =search_bar_bll(search_text, session['user_id'])
    if not search_results:
        abort(404)
    return render_template("home.html", products = select_all_bll(session['user_id']), search_results = search_results)

@app.route("/admin/upload", methods = ["POST"])
def update_picture_file():
    if session['role_id'] == 1:
        product_id = request.form.get("id") 
        filename = request.files["updateImage"]
        update_picture_file_bll(filename, product_id, session['user_id'])
        return redirect(url_for("cart_bp.cart"))
    else:
        raise Exception("Only admin can update product images")
    
        

@app.route("/logout", methods = ["POST"])
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route("/admin/change_songs", methods = ["POST", "GET"])
def admin_change_songs():
    if request.method == "GET":
        if session['role_id'] != 1:
            flash("Users cannot access this page, admins only!")
        else:
            return render_template("song_choose_cart_and_home.html")
        
    if request.method == "POST":
        file = request.files.get("homepage song")
        page = "home"
        if not file:
            file = request.files.get("cart song")
            page  = "cart"
        if file:
            change_song_bll(page, file)
        else:
            flash("No song was chosen.")
            return render_template("song_choose_cart_and_home.html")
        
    return redirect(url_for('submit', products = select_all_bll(session['user_id'])))

@app.route("/song")
def home_play_song():
    song = play_song_bll("home")
    if not song:
         return redirect(url_for('submit', products = select_all_bll(session['user_id'])))
    return song







@app.errorhandler(404)
def page_not_found(error):
    if request.path == "/products/search":
        error.description = "Product not in cart"
    return render_template("404.html", error=error)
print(app.url_map)
#@app.errorhandler(Exception)
# def flash_exceptions(e):
#     flash(str(e))
#     print(str(e))
#     if 'user_id' in session:
#         return redirect(url_for('submit', products=select_all_bll(session['user_id'])))
#     else:
#         return redirect(url_for('login'))
