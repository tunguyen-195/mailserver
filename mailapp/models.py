import sys
sys.path.insert(0, '/Users/nguyenminhtu/Workspace/Freelance/mailserver')
from mailapp import db, app
from sqlalchemy import Table, Column, Integer, String, Text, DateTime, Boolean, ForeignKey, text
from sqlalchemy.orm import relationship, backref
from flask_security import RoleMixin
from flask_login import UserMixin 
from datetime import datetime
from sqlalchemy.sql import func
import os

class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    email_address = Column(String(255), unique=True, nullable=False)
    role_id = Column(Integer, ForeignKey('role.id'))

    # Additional fields for Flask-Security
    active = Column(Boolean(), default=True)
    confirmed_at = Column(DateTime())

    # Flask-Login integration
    def get_id(self):
        return str(self.id)

    
    def __str__(self) -> str:
        return self.full_name

class Role(db.Model, RoleMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
    users = relationship('User', backref='role') 

class Mailbox(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

class SentMail(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    recipient_email = Column(String(255), nullable=False)
    subject = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    sent_at = Column(DateTime, default= datetime.now(), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'recipient_email': self.recipient_email,
            'subject': self.subject,
            'content': self.content,
            'sent_at': self.sent_at.strftime('%Y-%m-%d %H:%M:%S') if self.sent_at else None
        }

class ReceivedMail(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    sender_email = Column(String(255), nullable=False)
    subject = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    received_at = Column(DateTime, default= datetime.now(), nullable=False)
    is_read = Column(Integer, default=0, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'sender_email': self.sender_email,
            'subject': self.subject,
            'content': self.content,
            'received_at': self.received_at.strftime('%Y-%m-%d %H:%M:%S') if self.received_at else None,
            'is_read': self.is_read,
        }

class MailboxEmail(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    mailbox_id = Column(Integer, ForeignKey('mailbox.id'), nullable=False)
    email_id = Column(Integer, nullable=False) 
    is_archived = Column(Integer, default=0, nullable=False)
    is_trash = Column(Integer, default=0, nullable=False)

class EmailAccount(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    email_address = Column(String(255), unique=True, nullable=False)
    incoming_server = Column(String(255), nullable=False)
    outgoing_server = Column(String(255), nullable=False)
    incoming_port = Column(Integer, nullable=False)
    outgoing_port = Column(Integer, nullable=False)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    is_default = Column(Integer, default=0, nullable=False)

class SecurityOption(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    use_ssl = Column(String(5), default="no", nullable=False)
    use_tls = Column(String(5), default="no", nullable=False)

class Session(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    token = Column(String(255), unique=True, nullable=False)
    expiry = Column(DateTime, nullable=False)

class PasswordResetToken(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    token = Column(String(255), unique=True, nullable=False)
    expiry = Column(DateTime, nullable=False)

if __name__ == '__main__':
    if not os.path.exists('./data/MailServer.db'):
        with app.app_context():
            db.create_all()  

        #     # Creating roles
        #     admin_role = Role(name='admin')
        #     user_role = Role(name='user')

        #     db.session.add_all([admin_role, user_role])
        #     db.session.commit()

        #     # Creating users
        #     users = [
        #         {"id": 1, "username": "admin", "password_hash": "$2b$12$oBM9KCCZQuv0D.Ec8uUbuOpiTpBJZh9R8KcDzgpI/iPR5jKItx8eK", "full_name": "Huy Hoàng", "email_address": "huyhoang@t07.com", "role_id": admin_role.id},
        #         {"id": 2, "username": "user", "password_hash": "$2b$12$.UdJbp02CgheHaLMfr6qGukxOqkmMwKPdk.8S2nlkdrTopRXC/gYi", "full_name": "Hoàng Trung", "email_address": "hoangtrung@t07.com", "role_id": user_role.id},
        #         {"id": 3, "username": "user2", "password_hash": "$2b$12$CZEuLlRnBfiWhthbljkDhOlxVCJx524hLm2smQ48sBz6drtXiOcIe", "full_name": "Regular User 2", "email_address": "user2@t07.com", "role_id": user_role.id},
        #         {"id": 4, "username": "admin2", "password_hash": "$2b$12$GAryARuYGqSVFY2Pb5XJqeLMRxNj1GB0caCnk8uhddV/fMkSXTtTK", "full_name": "Admin User 2", "email_address": "admin2@t07.com", "role_id": admin_role.id},
        #         {"id": 5, "username": "admin3", "password_hash": "$2b$12$CuUCvjWksBoQr5kt5Y4cUO7ZpOGPIKS/iIuvF/NPsm40gjwA2vA0i", "full_name": "Admin User 3", "email_address": "admin3@t07.com", "role_id": admin_role.id},
        #         {"id": 6, "username": "user3", "password_hash": "$2b$12$QV/69jV96M1MXVwNM1XbueQzD/.DLOAEokGu8aNsbsQXknZ6H0Gyy", "full_name": "Regular User 3", "email_address": "user3@t07.com", "role_id": user_role.id}
        #     ]

        #     for u in users:
        #         usr = User(
        #             username=u["username"],
        #             password_hash=u["password_hash"],
        #             full_name=u["full_name"],
        #             email_address=u["email_address"],
        #             role_id=u["role_id"]
        #         )
        #         db.session.add(usr)

        #     db.session.commit()

        #     # Tạo dữ liệu cho bảng Mailbox
        #     mailboxes_data = [
        #         {"id": 1, "user_id": 1, "name": "Inbox", "description": "Inbox for huyhoang"},
        #         {"id": 2, "user_id": 2, "name": "Inbox", "description": "Inbox for hoangtrung"},
        #         {"id": 3, "user_id": 3, "name": "Inbox", "description": "Inbox for user2"},
        #         {"id": 4, "user_id": 4, "name": "Inbox", "description": "Inbox for admin2"},
        #         {"id": 5, "user_id": 5, "name": "Inbox", "description": "Inbox for admin3"},
        #         {"id": 6, "user_id": 6, "name": "Inbox", "description": "Inbox for user3"}
        #     ]

        #     # for mailbox_data in mailboxes_data:
        #     #     mailbox = Mailbox(
        #     #         id=mailbox_data["id"],
        #     #         user_id=mailbox_data["user_id"],
        #     #         name=mailbox_data["name"],
        #     #         description=mailbox_data["description"]
        #     #     )
        #     #     db.session.add(mailbox)

        #     # db.session.commit()

        #     # Tạo dữ liệu cho bảng SentMail
        # # Tạo dữ liệu cho bảng SentMail
            # sentmails_data = [
            #     {"id": 7, "user_id": 1, "recipient_email": "admin3@t07.com", "subject": "Hello User 1", "content": "Content for User 1"},
            #     {"id": 8, "user_id": 1, "recipient_email": "user2@t07.com", "subject": "Hello User 2", "content": "Content for User 2"},
            #     {"id": 9, "user_id": 2, "recipient_email": "huyhoang@t07.com", "subject": "Hello Admin 1", "content": "Content for Admin 1"},
            #     {"id": 10, "user_id": 2, "recipient_email": "admin2@t07.com", "subject": "Hello Admin 2", "content": "Content for Admin 2"},
            #     {"id": 11, "user_id": 3, "recipient_email": "admin3@t07.com", "subject": "Hello Admin 3", "content": "Content for Admin 3"},
            #     {"id": 12, "user_id": 3, "recipient_email": "user3@t07.com", "subject": "Hello User 3", "content": "Content for User 3"},
            # ]

            # # Thêm dữ liệu vào bảng SentMail
            # for data in sentmails_data:
            #     sent_mail = SentMail(**data)
            #     db.session.add(sent_mail)

            # Commit để lưu dữ liệu vào cơ sở dữ liệu
            # db.session.commit()

        #     # Tạo dữ liệu cho bảng ReceivedMail
            # receivedmails_data = [
            #     {"id": 7, "user_id": 4, "sender_email": "huyhoang@t07.com", "subject": "Re: Hello Admin 1", "content": "Reply to Admin 1",  "is_read": 1},
            #     {"id": 8, "user_id": 1, "sender_email": "admin2@t07.com", "subject": "Re: Hello Admin 2", "content": "Reply to Admin 2", "is_read": 1},
            #     {"id": 9, "user_id": 1, "sender_email": "admin3@t07.com", "subject": "Re: Hello Admin 3", "content": "Reply to Admin 3", "is_read": 1},
            #     {"id": 10, "user_id": 1, "sender_email": "user3@t07.com", "subject": "Re: Hello User 3", "content": "Reply to User 3", "is_read": 0},
            #     {"id": 11, "user_id": 5, "sender_email": "huyhoang@t07.com", "subject": "Re: Hello Admin 1", "content": "Reply to Admin 1", "is_read": 0},
            #     {"id": 12, "user_id": 4, "sender_email": "hoangtrung@t07.com", "subject": "Re: Hello User 1", "content": "Reply to User 1", "is_read": 0}
            # ]

            # # Thêm dữ liệu vào bảng SentMail
            # for data in receivedmails_data:
            #     receive_mail = ReceivedMail(**data)
            #     db.session.add(receive_mail)

            # # Commit để lưu dữ liệu vào cơ sở dữ liệu
            # db.session.commit()



