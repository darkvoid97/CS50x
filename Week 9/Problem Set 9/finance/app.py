import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # Get all the user's shares, stocks and cash
    stocks = db.execute(
        "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0", user_id=session.get("user_id"))
    cash = db.execute("SELECT cash FROM users WHERE id = :user_id",
                      user_id=session.get("user_id"))[0]["cash"]

    # Iterate over stocks and add price and total value
    total_value = cash
    grand_total = cash

    for stock in stocks:
        quote = lookup(stock["symbol"])
        stock["name"] = quote["name"]
        stock["price"] = quote["price"]
        stock["total_value"] = stock["price"] * stock["total_shares"]
        total_value += stock["total_value"]
        grand_total += stock["total_value"]

    return render_template("index.html", stocks=stocks, cash=cash, total_value=total_value, grand_total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # Handle POST and GET requests
    if request.method == "POST":
        # Validate the input
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("must provide symbol", 400)
        if not shares or not shares.isdigit() or int(shares) < 1:
            return apology("must provide a positive integer for shares amount", 400)

        # Check if the stock exists
        stock = lookup(symbol)
        if not stock:
            return apology("invalid symbol", 400)

        # Get the total price for the selected stock and check if the user can afford it
        total = float(shares) * float(stock["price"])
        user = session.get("user_id")
        cash = db.execute(f"SELECT cash FROM users WHERE id = {user}")[0]["cash"]
        if cash < total:
            return apology("you don't have enough cash", 400)
        # If the user has enough cash, update the new cash amount in the database by substracting the stock price
        db.execute(f"UPDATE users SET cash = {cash - total} WHERE id = {user}")

        # Update the transactions table of the database with this new purchase
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   user, symbol, shares, total)

        # Redirect user to the homepage
        flash("Successfully bought shares of the stock!")
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # Get all the user's transactions
    transactions = db.execute(
        "SELECT symbol, shares, price, timestamp FROM transactions WHERE user_id = ?", session.get("user_id"))

    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # Handle POST and GET requests
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide symbol", 400)

        quote = lookup(symbol)
        if not quote:
            return apology("invalid symbol", 400)

        return render_template("quoted.html", quote=quote)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Clear the user ID
    session.clear()

    # Handle the GET and POST requests
    if request.method == "POST":
        # Validate the input
        username = request.form.get("username")
        pwd = request.form.get("password")
        conf = request.form.get("confirmation")

        if not username:
            return apology("must input an username", 400)
        if not pwd:
            return apology("must input a password", 400)
        if not conf:
            return apology("must input password confirmation", 400)
        if pwd != conf:
            return apology("input password and confirmation don't match", 400)

        # Insert the input into the database, while checking that the username doesn't already exist
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                       username, generate_password_hash(pwd))
        except ValueError:
            return apology("username already exists", 400)
        # If everything goes well, flash a message to the user and then redirect them to the login page
        else:
            flash("Registered successfully! Please log in.")
            return redirect("/login")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # Handle GET and POST requests. POST will allow the sale to happen, while GET will list the options to sell
    if request.method == "POST":
        # Validate user input
        symbol = request.form.get("symbol")
        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("shares must be a positive integer", 400)
        if not symbol:
            return apology("invalid symbol", 400)
        if shares < 1:
            return apology("invalid shares amount", 400)

        # Get the total amount of shares for that stock currently owned by the user and check if the sale is possible
        stock = db.execute(
            "SELECT SUM(shares) as total_shares FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol", session.get("user_id"), symbol)
        if not stock or stock[0]["total_shares"] < shares:
            return apology("Not enough shares to sell", 400)

        # Get the stock's current price, calculate sell value and update user's cash
        info = lookup(symbol)
        if not info:
            return apology("invalid symbol", 400)

        sell_value = info["price"] * shares
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?",
                   sell_value, session.get("user_id"))

        # Insert sell transaction into database
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, timestamp) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)",
                   session.get("user_id"), symbol, -shares, info["price"])

        # Redirect to index page
        flash("Shares of stock are successfully sold!")
        return redirect("/")

    # GET request, list all the stocks the user can sell
    else:
        stocks = db.execute(
            "SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol", session.get("user_id"))
        symbols = [stock["symbol"] for stock in stocks]
        return render_template("sell.html", symbols=symbols)


@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    """Change user password"""
    # Handle the GET and POST requests
    if request.method == "POST":
        # Validate the input
        old = request.form.get("old_password")
        pwd = request.form.get("new_password")
        conf = request.form.get("confirmation")

        if not old or not pwd or not conf:
            return apology("must fill every field", 400)
        if pwd != conf:
            return apology("new password and confirmation don't match", 400)
        if old == pwd:
            return apology("new password cannot match the current password", 400)

        # Check if the user's current password is correct
        rows = db.execute("SELECT * FROM users WHERE id = ?", session.get("user_id"))
        if not check_password_hash(rows[0]["hash"], old):
            return apology("current password is not correct", 403)

        # Change the user's hashed password stored in the database
        db.execute("UPDATE users SET hash = ? WHERE id = ?",
                   generate_password_hash(pwd), session.get("user_id"))

        flash("Password is successfully changed!")
        return redirect("/")

    else:
        return render_template("change.html")


@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    """Add or Remove amount of cash for user"""
    # Validate the input
    cash = request.form.get("cash")

    if not cash:
        return apology("must provide cash amount", 400)
    try:
        cash = float(cash)
    except ValueError:
        return apology("must provide a valid number", 400)

    # 'zero' is technically an acceptable value, but I don't feel like wasting database queries to add nothing and changing literally nothing
    if cash != 0:
        # Update the user's cash amount in the database
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?",
                   f"{cash:.2f}", session.get("user_id"))

    # Redirect user to the homepage
    return redirect("/")


@app.route("/add_shares", methods=["GET", "POST"])
@login_required
def add_shares():
    """Add or Remove shares of a certain stock for user"""
    # Validate the input
    shares = request.form.get("shares")
    symbol = request.form.get("symbol")

    if not symbol:
        return apology("must provide symbol", 400)
    if not shares:
        return apology("must provide a valid integer for shares amount", 400)
    try:
        shares = int(shares)
    except ValueError:
        return apology("must provide a valid integer for shares amount", 400)

    # If value is positive, user is buying shares. If value is negative, user is selling shares. If value is zero, do nothing
    if shares != 0:
        # Buying shares
        if shares > 0:
            stock = lookup(symbol)
            if not stock:
                return apology("invalid symbol", 400)

            # Get the total price for the selected stock and check if the user can afford it
            total = float(shares) * float(stock["price"])
            user = session.get("user_id")
            cash = db.execute(f"SELECT cash FROM users WHERE id = {user}")[0]["cash"]
            if cash < total:
                return apology("you don't have enough cash", 400)
            # If the user has enough cash, update the new cash amount in the database by substracting the stock price
            db.execute("UPDATE users SET cash = ? - ? WHERE id = ?", cash, total, user)

            # Update the transactions table of the database with this new purchase
            db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                       user, symbol, shares, total)
            flash("Successfully bought shares of the stock!")

        # Selling shares
        elif shares < 0:
            # Get the total amount of shares for that stock currently owned by the user and check if the sale is possible
            sell_shares = -shares
            stock = db.execute(
                "SELECT SUM(shares) as total_shares FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol", session.get("user_id"), symbol)
            if not stock or stock[0]["total_shares"] < sell_shares:
                return apology("Not enough shares to sell", 400)

            # Get the stock's current price, calculate sell value and update user's cash
            info = lookup(symbol)
            if not info:
                return apology("invalid symbol", 400)

            sell_value = info["price"] * sell_shares
            db.execute("UPDATE users SET cash = cash + ? WHERE id = ?",
                       sell_value, session.get("user_id"))

            # Insert sell transaction into database
            db.execute("INSERT INTO transactions (user_id, symbol, shares, price, timestamp) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)", session.get(
                "user_id"), symbol, -sell_shares, info["price"])
            flash("Shares of stock are successfully sold!")

    # Redirect user to the homepage
    return redirect("/")
