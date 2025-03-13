from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Emmanuel:Ope12yemi@localhost/fincom_web_info'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Required for session management

db = SQLAlchemy(app) # creates a link between the app and the database
bcrypt = Bcrypt(app) # hashes passwords
login_manager = LoginManager(app) # handles the login and user authentication
login_manager.login_view = 'login'

# User Model
class users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(225), unique=True, nullable=False)
    email = db.Column(db.String(225), unique=True, nullable=False)
    password = db.Column(db.String(225), nullable=False)  
    nationality = db.Column(db.String(225), nullable=False)  
    customer_type = db.Column(db.String(225), nullable=False)  

# Test database connection
with app.app_context():
    try:
        db.session.execute("SELECT 1")  # Test connection
        print("Connected to MySQL successfully!")
    except Exception as e:
        print("Database connection failed:", e)

    # Ensure table exists
    if not db.engine.dialect.has_table(db.engine, "users"):  # Check if 'user' table exists
        db.create_all()

# Load user for authentication
@login_manager.user_loader
def load_user(user_id):
    # so what i did was use sqlalchemy to create the database and it connected to it and if its needed to 
     # use a different database just change the configurations !!

    return users.query.get(int(user_id))

if __name__ == '__main__':
    app.run(debug=True)
