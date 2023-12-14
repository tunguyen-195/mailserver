import secrets
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from sqlalchemy_json import mutable_json_type



app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app=app)
app.secret_key = secrets.token_urlsafe(16)
app.config['PERMANENT_SESSION_LIFETIME'] = 18000 #life cho session là 3h
base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, 'data', 'MailServer.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = True

db = SQLAlchemy(app=app)
# db.TypeDecorator = mutable_json_type(db.TypeDecorator)

# Initialize extensions
# db = SQLAlchemy()
# bcrypt = Bcrypt()
# login_manager = LoginManager()

# def create_app():
#     app = Flask(__name__)
#     app.config['SECRET_KEY'] = 'your_secret_key'

#     # Configure and initialize extensions
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     db.init_app(app)
#     bcrypt.init_app(app)
#     login_manager.init_app(app)
    
#     # # Import blueprints
#     # from .admin import admin_bp, admin

#     # app.register_blueprint(admin_bp)
#     # admin.init_app(app)

#     # # Import models
#     # from .models import User

#     # Rest of your code...

#     return app
# app = create_app()