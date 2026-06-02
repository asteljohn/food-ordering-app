import bcrypt
from flask import Flask, render_template, request, redirect, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import sqlite3

app = Flask(__name__)
app.secret_key = "foodsecretkey"

limiter = Limiter(
    get_remote_address,
    app=app
)

@app.after_request
def add_security_headers(response):
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Content-Security-Policy'] = "default-src 'self'; img-src 'self' data: https:; style-src 'self' 'unsafe-inline' https:; script-src 'self' 'unsafe-inline' https:;"
    #response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response

# DATABASE CONNECTION
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# HOME PAGE
@app.route('/')
def home():
    return render_template("welcome.html")


# USER REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Hash password
        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

        conn = get_db()

        conn.execute(
            "INSERT INTO users (name,email,password) VALUES (?,?,?)",
            (name, email, hashed_password)
        )

        conn.commit()

        return redirect('/login')

    return render_template("register.html")


# USER LOGIN
@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        conn = get_db()

        user = conn.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        ).fetchone()

        if user:

            stored_password = user['password']

            # New bcrypt users
            if stored_password.startswith('$2b$'):

                if bcrypt.checkpw(
                    password.encode('utf-8'),
                    stored_password.encode('utf-8')
                ):
                    session['user_id'] = user['id']
                    session['name'] = user['name']
                    return redirect('/user_dashboard')

            # Old plain-text users
            elif password == stored_password:

                session['user_id'] = user['id']
                session['name'] = user['name']
                return redirect('/user_dashboard')

    return render_template("login.html")


# USER DASHBOARD
@app.route('/user_dashboard')
def user_dashboard():

    conn = get_db()

    foods = conn.execute(
        "SELECT * FROM food_items"
    ).fetchall()

    return render_template(
        "user_dashboard.html",
        name=session.get('name'),
        foods=foods
    )

# ADMIN LOGIN
@app.route('/admin_login', methods=['GET','POST'])
@limiter.limit("5 per minute")
def admin_login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if username == "Astel" and password == "Astel@2005":
            session['admin'] = username
            return redirect('/admin_dashboard')

    return render_template("admin_login.html")


@app.route('/admin_dashboard')
def admin_dashboard():

    if 'admin' not in session:
        return redirect('/admin_login')

    conn = get_db()

    total_orders = conn.execute(
        "SELECT COUNT(*) FROM orders"
    ).fetchone()[0]

    total_users = conn.execute(
        "SELECT COUNT(*) FROM users"
    ).fetchone()[0]

    total_foods = conn.execute(
        "SELECT COUNT(*) FROM food_items"
    ).fetchone()[0]

    return render_template(
        "admin_dashboard.html",
        total_orders=total_orders,
        total_users=total_users,
        total_foods=total_foods
    )

# ADD FOOD
@app.route('/add_food', methods=['GET', 'POST'])
def add_food():

    if 'admin' not in session:
        return redirect('/admin_login')

    if request.method == 'POST':

        food_name = request.form['food_name']
        price = request.form['price']

        conn = get_db()

        conn.execute(
            "INSERT INTO food_items (food_name, price) VALUES (?, ?)",
            (food_name, price)
        )

        conn.commit()

        return redirect('/add_food')

    return render_template("add_food.html")

# MANAGE FOOD
@app.route('/manage_food')
def manage_food():

    if 'admin' not in session:
        return redirect('/admin_login')

    conn = get_db()

    foods = conn.execute(
        "SELECT * FROM food_items"
    ).fetchall()

    return render_template(
        "manage_food.html",
        foods=foods
    )

# DELETE FOOD
@app.route('/delete_food/<int:id>')
def delete_food(id):

    if 'admin' not in session:
        return redirect('/admin_login')

    conn = get_db()

    conn.execute(
        "DELETE FROM food_items WHERE id=?",
        (id,)
    )

    conn.commit()

    return redirect('/manage_food')

@app.route('/edit_food/<int:id>', methods=['GET', 'POST'])
def edit_food(id):

    if 'admin' not in session:
        return redirect('/admin_login')

    conn = get_db()

    if request.method == 'POST':

        food_name = request.form['food_name']
        price = request.form['price']

        conn.execute(
            "UPDATE food_items SET food_name=?, price=? WHERE id=?",
            (food_name, price, id)
        )

        conn.commit()

        return redirect('/manage_food')

    food = conn.execute(
        "SELECT * FROM food_items WHERE id=?",
        (id,)
    ).fetchone()

    return render_template(
        'edit_food.html',
        food=food
    )

@app.route('/view_orders')
def view_orders():

    if 'admin' not in session:
        return redirect('/admin_login')

    conn = get_db()

    orders = conn.execute(
        "SELECT * FROM orders ORDER BY id DESC"
    ).fetchall()

    return render_template(
        "view_orders.html",
        orders=orders
    )

@app.route('/update_order_status')
def update_order_status():

    if 'admin' not in session:
        return redirect('/admin_login')

    conn = get_db()

    orders = conn.execute(
        "SELECT * FROM orders ORDER BY id DESC"
    ).fetchall()

    return render_template(
        "update_order_status.html",
        orders=orders
    )

@app.route('/change_status/<int:id>/<status>')
def change_status(id, status):

    if 'admin' not in session:
        return redirect('/admin_login')

    conn = get_db()

    conn.execute(
        "UPDATE orders SET status=? WHERE id=?",
        (status, id)
    )

    conn.commit()

    return redirect('/update_order_status')

@app.route('/update_status/<int:id>')
def update_status(id):

    if 'admin' not in session:
        return redirect('/admin_login')

    conn = get_db()

    conn.execute(
        "UPDATE orders SET status='Delivered' WHERE id=?",
        (id,)
    )

    conn.commit()

    return redirect('/view_orders')

@app.route('/manage_users')
def manage_users():

    if 'admin' not in session:
        return redirect('/admin_login')

    conn = get_db()

    users = conn.execute(
        "SELECT * FROM users"
    ).fetchall()

    return render_template(
        "manage_users.html",
        users=users
    )

# ORDER FOOD
@app.route('/order/<int:id>')
def order_food(id):

    conn = get_db()

    food = conn.execute(
        "SELECT * FROM food_items WHERE id=?",
        (id,)
    ).fetchone()

    if food:

        conn.execute(
            "INSERT INTO orders (user_name, food_name, price) VALUES (?, ?, ?)",
            (
                session['name'],
                food['food_name'],
                food['price']
            )
        )

        conn.commit()

        print("Order placed successfully")

    return redirect('/user_dashboard')

@app.route('/my_orders')
def my_orders():

    if 'name' not in session:
        return redirect('/login')

    conn = get_db()

    orders = conn.execute(
        "SELECT * FROM orders WHERE user_name=?",
        (session.get('name'),)
    ).fetchall()

    return render_template(
        "my_orders.html",
        orders=orders
    )

# LOGOUT
@app.route('/logout')
def logout():

    session.clear()

    return redirect('/')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
