import sqlite3
import bcrypt

def initialize_database():
 try:
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()

    # Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,  -- Store a hashed version for security
            email TEXT UNIQUE
        )
    ''')

    # Budgets table
    c.execute('''
        CREATE TABLE IF NOT EXISTS budgets (
            user_id INTEGER,
            month INTEGER,
            year INTEGER,
            amount REAL,
            PRIMARY KEY (user_id, month, year)
        )
    ''')

    # Recurring expenses table
    c.execute('''
        CREATE TABLE IF NOT EXISTS recurring_expenses (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            description TEXT,
            amount REAL,
            recurrence_type TEXT,
            next_due_date TEXT
        )
    ''')

    # Savings goals table
    c.execute('''
        CREATE TABLE IF NOT EXISTS savings_goals (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            description TEXT,
            target_amount REAL,
            current_amount REAL
        )
    ''')

    # Expenses table
    c.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                description TEXT,
                amount REAL,
                date TEXT
            )
        ''')

    conn.commit()
    conn.close()

 except sqlite3.Error as e:
    print(f"Database error: {e}")
 except Exception as e:
    print(f"Unexpected error: {e}")



initialize_database()

class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password  # Store a hashed version for security
        self.email = email

class Budget:
    def __init__(self, user_id, month, year, amount):
        self.user_id = user_id
        self.month = month
        self.year = year
        self.amount = amount

class RecurringExpense:
    def __init__(self, user_id, description, amount, recurrence_type, next_due_date):
        self.user_id = user_id
        self.description = description
        self.amount = amount
        self.recurrence_type = recurrence_type
        self.next_due_date = next_due_date

class SavingsGoal:
    def __init__(self, user_id, description, target_amount, current_amount=0):
        self.user_id = user_id
        self.description = description
        self.target_amount = target_amount
        self.current_amount = current_amount

def register_user(username, password, email):
 try:
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()

    # Check if the username or email already exists
    c.execute("SELECT * FROM users WHERE username=? OR email=?", (username, email))
    existing_user = c.fetchone()

    if existing_user:
        print("Username or email already exists.")
        return False

    # Insert the new user
    c.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, password, email))
    conn.commit()
    conn.close()

 except sqlite3.IntegrityError:
    print("Username or email already exists. Please choose a different one.")

 except sqlite3.Error as e:
  print(f"Database error: {e}")
 except Exception as e:
  print(f"Unexpected error: {e}")

  print("User registered successfully!")
  return True

def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

def check_password(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def login_user(username: str, password: str) -> bool:
 try:
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()

    c.execute("SELECT password FROM users WHERE username=?", (username,))
    stored_password = c.fetchone()

    conn.close()

 except sqlite3.Error as e:
    print(f"Database error: {e}")

 except Exception as e:
  print(f"Unexpected error: {e}")

 if stored_password and check_password(password, stored_password[0].encode('utf-8')):
        print("Login successful!")
        return True
 else:
        print("Invalid username or password.")
        return False
def logout_user():
    print("User logged out successfully!")


def add_expense(user_id, description, amount, date):
    try:
        conn = sqlite3.connect('expenses.db')
        c = conn.cursor()

        c.execute("INSERT INTO expenses (user_id, description, amount, date) VALUES (?, ?, ?, ?)",
                  (user_id, description, amount, date))
        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

        print("Expense added successfully!")

def view_expenses(user_id):
 try:
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()

    c.execute("SELECT description, amount, date FROM expenses WHERE user_id=?", (user_id,))
    expenses = c.fetchall()

    conn.close()

 except sqlite3.Error as e:
    print(f"Database error: {e}")

 except Exception as e:
    print(f"Unexpected error: {e}")

    return expenses

def update_expense(expense_id, description=None, amount=None, date=None):
 try:
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()

    if description:
        c.execute("UPDATE expenses SET description=? WHERE id=?", (description, expense_id))
    if amount:
        c.execute("UPDATE expenses SET amount=? WHERE id=?", (amount, expense_id))
    if date:
        c.execute("UPDATE expenses SET date=? WHERE id=?", (date, expense_id))

    conn.commit()
    conn.close()

 except sqlite3.Error as e:
    print(f"Database error: {e}")

 except Exception as e:
    print(f"Unexpected error: {e}")

    print("Expense updated successfully!")

def delete_expense(expense_id):
 try:
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()

    c.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()
    conn.close()

 except sqlite3.Error as e:
    print(f"Database error: {e}")

 except Exception as e:
    print(f"Unexpected error: {e}")

    print("Expense deleted successfully!")

if __name__ == "__main__":
    register_user("sampleUser", "samplePassword", "sample@email.com")

from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password']
    email = data['email']

    # Call the register_user function from our previous code
    success = register_user(username, password, email)
    if success:
        return jsonify({"message": "User registered successfully!"}), 201
    else:
        return jsonify({"message": "Registration failed."}), 400

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/add_expense', methods=['POST'])
def api_add_expense():
    data = request.json
    user_id = data['user_id']
    description = data['description']
    amount = data['amount']
    date = data['date']
    try:
        add_expense(user_id, description, amount, date)
        return jsonify({"message": "Expense added successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/view_expenses/<int:user_id>', methods=['GET'])
def api_view_expenses(user_id):
    try:
        expenses = view_expenses(user_id)
        return jsonify(expenses), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
from flask_jwt_extended import JWTManager

app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this!
jwt = JWTManager(app)

from flask_jwt_extended import jwt_required

@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    return jsonify({"message": "This is a protected endpoint!"}), 200

from flask_jwt_extended import create_access_token

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']
    # Check user credentials here...
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200






