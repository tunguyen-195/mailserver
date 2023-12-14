from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from flask import redirect, url_for
from flask_login import current_user
from mailapp.models import User
from mailapp import db

class AdminModelView(ModelView):
    can_view_details = True
    can_export = True
    column_searchable_list = ['username', 'full_name', 'email_address']
    column_filters = ['role_id']
    column_list = ('username', 'full_name', 'email_address', 'role_id', 'active', 'confirmed_at')
    column_labels = {
        'full_name': 'Họ và Tên',
        'password_hash': 'Mật khẩu',
        'email_address': 'Địa chỉ Email',
        'role_id': 'Role ID',
        'active': 'Tình trạng'
    }
    column_exclude_list = ['confirmed_at']
    form_columns = ('username', 'full_name', 'email_address', 'role_id', 'active', 'confirmed_at')

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.role_id == 1
        return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('/'))

class AdminIndex(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.role_id == 1
        return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))

admin = Admin(name="T07 Mail Server Adminstration", index_view=AdminIndex(), template_mode='bootstrap4')
admin.add_view(AdminModelView(User, db.session))
admin.add_link(MenuLink(name='Email', endpoint='index'))


