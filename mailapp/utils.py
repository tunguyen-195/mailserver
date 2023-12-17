from mailapp.models import User, SentMail, ReceivedMail
from mailapp import app, db, bcrypt
from sqlalchemy.exc import SQLAlchemyError

def hashPassword(password):
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    return hashed_password

def changePassword(username, password):
    current_user = User.query.filter_by(username=username).first()
    if current_user:
        current_user.password_hash = hashPassword(password)
    db.session.commit()
    return True
 
def isAuthenticated(username, password):
    if username and password:
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
                return user
    return None

def getUserByID(user_id):
    try:
        return User.query.get(user_id)
    except Exception as e:
        app.logger.info(f"An error occurred: {e}")
        return None
    
def getUserByEmail(email):
    try:
        return User.query.filter_by(email_address = email).first()
    except Exception as e:
        app.logger.info(f"An error occurred: {e}")
        return None

def load_users(user_id = None):
    return User.query.all()

def getInbox(user_id):
    data = ReceivedMail.query.filter(ReceivedMail.user_id==user_id).all()
    json_data = [item.serialize() for item in data]
    return json_data

def getSentMail(user_id):
    data = SentMail.query.filter(SentMail.user_id==user_id).all()
    json_data = [item.serialize() for item in data]
    return json_data

def count_mail(mails):
     return {'total_mail': len(mails)}

def add_sent_mail(user_id, recipient_email, subject, content):
    try:
        sent_mail = SentMail(
            user_id=user_id,
            recipient_email=recipient_email,
            subject=subject,
            content=content,
        )
        db.session.add(sent_mail)
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        return False

def add_received_mail(user_id, sender_email, subject, content):
    try:
        received_mail = ReceivedMail(
            user_id=user_id,
            sender_email=sender_email,
            subject=subject,
            content=content,
        )
        db.session.add(received_mail)
        db.session.commit()
        return True

    except SQLAlchemyError as e:
        db.session.rollback()
        return False




