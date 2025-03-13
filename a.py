from flask import Flask, render_template, request, redirect, session, flash
import mysql.connector
from mysql.connector import Error
from flask_bcrypt import Bcrypt
import re
from flask_mail import Mail, Message
import random

app = Flask(__name__, template_folder='.')
bcrypt = Bcrypt(app)
app.secret_key = "your_secret_key"


# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'muhammedtesleemolatundun.com'  # Your email address
app.config['MAIL_PASSWORD'] = 'csqv yavo jcwj bghz'  # Your email password
app.config['MAIL_DEFAULT_SENDER'] = 'projectfinodido@gmail.com'  # Default sender

mail = Mail(app)
def get_db_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="Teslim",
            password="Tesleem@123",
            database="mydatabase"
        )
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None 