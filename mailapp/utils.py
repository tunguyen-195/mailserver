# from flask_sqlalchemy import SQLAlchemy
from mailapp.models import User, SentMail, ReceivedMail
from mailapp import app, db, bcrypt



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
        # if hasattr(user, 'role_id'):
        #     return user
        # else:
        #     app.logger.info("User object does not have 'role_id' attribute.=========",user.role_id)
        #     return None
    except Exception as e:
        app.logger.info(f"An error occurred: {e}")
        return None
    
def getUserByEmail(email):
    try:
        return User.query.filter_by(email_address = email).first()
    except Exception as e:
        app.logger.info(f"An error occurred: {e}")
        return None

def read_json(path):
        with open(path, 'r') as f:
            content = f.read()
        return json.loads(content)

def load_users(user_id = None):
    return User.query.all()

# def load_mails(user_id = None, keywords = None): 
#     return read_json(os.path.join(app.root_path, 'data/data.json'))

# def load_mails_received(user_id = None, keywords = None): 
#     mails = ReceivedMail.query.all()
#     if user_id:
#         mails = ReceivedMail.query.filter(ReceivedMail.user_id.__eq__(user_id))
#     if keywords:
#         mails = ReceivedMail.query.filter(ReceivedMail.subject.constraints(keywords))
#     return mails.all()

# def load_mails_sent(user_id = None, keywords = None): 
#     mails = SentMail.query.all()
#     if user_id:
#         mails = SentMail.query.filter(SentMail.user_id.__eq__(user_id))
#     if keywords:
#         mails = SentMail.query.filter(SentMail.subject.constraints(keywords))

#     return mails.all()


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




